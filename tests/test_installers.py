"""Isolated installer contract tests. No real user skill directory is touched."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
OWNED = ("SKILL.md", "LICENSE")
MARKER = ".deal-inspector-owned"


def find_bash():
    if os.name == "nt":
        for location in ("C:/Program Files/Git/bin/bash.exe", "C:/Program Files/Git/usr/bin/bash.exe"):
            if Path(location).is_file():
                return location
        return None  # Do not accidentally invoke Windows' unrelated WSL launcher.
    return shutil.which("bash")


class InstallerContract:
    flavor = None
    executable = None

    def setUp(self):
        if not self.executable:
            if os.environ.get('GITHUB_ACTIONS') == 'true':
                self.fail(f"Required {self.flavor} runtime is missing from the CI runner")
            self.skipTest(f"{self.flavor} runtime not available")
        self.temp = tempfile.TemporaryDirectory(prefix="deal-inspector-tests-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.source = self.base / 'installer source'
        self.source.mkdir()
        for name in ('install.sh', 'uninstall.sh', 'install.ps1', 'uninstall.ps1', *OWNED):
            shutil.copyfile(REPO / name, self.source / name)
        self.root = self.base / "skills with spaces"
        self.installed = self.root / "deal-inspector"

    def run_script(self, action, *, force=False, legacy=False, root=None, extra=(), ok=True):
        target = root or self.root
        if self.flavor == "bash":
            args = [self.executable, (self.source / f"{action}.sh").as_posix(), "--target-dir", target.as_posix()]
            if force:
                args.append("--force")
            if legacy:
                args.append("--legacy")
        else:
            args = [self.executable, "-NoProfile", "-NonInteractive", "-File", str(self.source / f"{action}.ps1"), "-TargetDir", str(target)]
            if force:
                args.append("-Force")
            if legacy:
                args.append("-Legacy")
        result = subprocess.run(args + list(extra), capture_output=True, text=True, timeout=45)
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def installed_bytes(self):
        return {name: (self.installed / name).read_bytes() for name in (*OWNED, MARKER)}

    def assert_manifest(self):
        lines = (self.installed / MARKER).read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[0], "deal-inspector-v2")
        self.assertEqual(len(lines), 3)
        for name, line in zip(OWNED, lines[1:]):
            digest = hashlib.sha256((self.installed / name).read_bytes()).hexdigest()
            self.assertEqual(line, f"{digest}  {name}")

    def make_symlink(self, link, target, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except OSError as exc:
            junction_shell = shutil.which('pwsh') or shutil.which('powershell')
            if os.name == 'nt' and directory and junction_shell:
                # Directory junctions exercise Windows reparse rejection without symlink privilege.
                quote = lambda value: "'" + str(value).replace("'", "''") + "'"
                result = subprocess.run([junction_shell, '-NoProfile', '-NonInteractive', '-Command',
                    f"New-Item -ItemType Junction -Path {quote(link)} -Target {quote(target)} -ErrorAction Stop | Out-Null"],
                    capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    return
            self.skipTest(f"Symlink creation unavailable: {exc}")

    def test_fresh_install_and_clean_uninstall(self):
        self.run_script("install")
        for name in OWNED:
            self.assertEqual((self.installed / name).read_bytes(), (self.source / name).read_bytes())
        self.assert_manifest()
        self.assertFalse((self.root / "deal-inspector-SKILL.md").exists())
        self.run_script("uninstall")
        self.assertFalse(self.installed.exists())
        self.run_script("uninstall")  # Already absent is a safe no-op.

    def test_reinstall_requires_force_and_preserves_edits(self):
        self.run_script("install")
        (self.installed / "SKILL.md").write_text("local edit", encoding="utf-8")
        before = self.installed_bytes()
        self.run_script("install", ok=False)
        self.assertEqual(self.installed_bytes(), before)
        self.run_script("install", force=True)
        self.assertEqual((self.installed / "SKILL.md").read_bytes(), (self.source / "SKILL.md").read_bytes())
        self.assert_manifest()

    def test_unchanged_reinstall_also_requires_force(self):
        self.run_script("install")
        self.run_script("install", ok=False)
        self.run_script("install", force=True)
        self.assert_manifest()

    def test_modified_uninstall_checks_every_file_before_removing(self):
        self.run_script("install")
        (self.installed / "LICENSE").write_text("edited license", encoding="utf-8")
        before = self.installed_bytes()
        self.run_script("uninstall", ok=False)
        self.assertEqual(self.installed_bytes(), before)
        self.run_script("uninstall", force=True)
        self.assertFalse(self.installed.exists())

    def test_unrelated_files_survive_force_and_uninstall(self):
        self.run_script("install")
        extra = self.installed / "my notes.txt"
        extra.write_text("keep", encoding="utf-8")
        neighbor = self.root / "other-skill"
        neighbor.mkdir()
        (neighbor / "SKILL.md").write_text("unrelated", encoding="utf-8")
        self.run_script("install", force=True)
        self.run_script("uninstall", force=True)
        self.assertEqual(extra.read_text(), "keep")
        self.assertEqual((neighbor / "SKILL.md").read_text(), "unrelated")
        self.assertFalse((self.installed / "SKILL.md").exists())

    def test_custom_root_isolation(self):
        self.run_script("install")
        other = self.base / "another root"
        self.run_script("install", root=other)
        self.run_script("uninstall", root=other)
        self.assertTrue((self.installed / "SKILL.md").exists())

    def test_legacy_removal_is_explicit_and_separate(self):
        self.root.mkdir()
        legacy = self.root / "deal-inspector-SKILL.md"
        legacy.write_text("old file", encoding="utf-8")
        self.run_script("install")
        self.assertTrue(legacy.exists())
        self.run_script("uninstall", legacy=True, ok=False)
        self.assertTrue(legacy.exists())
        self.run_script("uninstall", legacy=True, force=True)
        self.assertFalse(legacy.exists())
        self.assertTrue((self.installed / "SKILL.md").exists())

    def test_unowned_directory_refused_even_with_force(self):
        self.installed.mkdir(parents=True)
        note = self.installed / "SKILL.md"
        note.write_text("not owned", encoding="utf-8")
        self.run_script("install", force=True, ok=False)
        self.run_script("uninstall", force=True, ok=False)
        self.assertEqual(note.read_text(), "not owned")

    def test_invalid_marker_never_controls_paths(self):
        self.run_script("install")
        before = (self.installed / "SKILL.md").read_bytes()
        (self.installed / MARKER).write_text("deal-inspector-v2\n" + "0" * 64 + "  ../../outside\n" + "0" * 64 + "  LICENSE\n", encoding="utf-8")
        self.run_script("uninstall", force=True, ok=False)
        self.run_script("install", force=True, ok=False)
        self.assertEqual((self.installed / "SKILL.md").read_bytes(), before)

    def test_linked_owned_file_is_refused_even_with_force(self):
        self.run_script("install")
        outside = self.base / "outside.txt"
        outside.write_text("untouched", encoding="utf-8")
        owned = self.installed / "SKILL.md"
        owned.unlink()
        self.make_symlink(owned, outside)
        self.run_script("install", force=True, ok=False)
        self.run_script("uninstall", force=True, ok=False)
        self.assertEqual(outside.read_text(), "untouched")
        self.assertTrue((self.installed / "LICENSE").exists())

    def test_linked_parent_is_refused(self):
        real = self.base / "real root"
        real.mkdir()
        linked = self.base / "linked root"
        self.make_symlink(linked, real, directory=True)
        self.run_script("install", root=linked, force=True, ok=False)
        self.assertEqual(list(real.iterdir()), [])

    def test_owned_directory_is_refused(self):
        self.run_script("install")
        owned = self.installed / "SKILL.md"
        owned.unlink()
        owned.mkdir()
        self.run_script("install", force=True, ok=False)
        self.run_script("uninstall", force=True, ok=False)
        self.assertTrue((self.installed / "LICENSE").exists())

    def test_hard_linked_file_does_not_modify_external_file(self):
        self.run_script("install")
        outside = self.base / "external-copy.md"
        outside.write_text("preserve hard link", encoding="utf-8")
        owned = self.installed / "SKILL.md"
        owned.unlink()
        try:
            os.link(outside, owned)
        except OSError as exc:
            self.skipTest(f"Hard links unavailable: {exc}")
        self.run_script("install", force=True)
        self.assertEqual(outside.read_text(), "preserve hard link")

    def test_unknown_option_is_rejected(self):
        flag = "--not-a-real-option" if self.flavor == "bash" else "-NotARealOption"
        self.run_script("install", extra=(flag,), ok=False)
        self.assertFalse(self.installed.exists())


class BashInstallers(InstallerContract, unittest.TestCase):
    flavor = "bash"
    executable = find_bash()


class PowerShellInstallers(InstallerContract, unittest.TestCase):
    flavor = "powershell"
    executable = shutil.which("pwsh") or (shutil.which("powershell") if os.name == "nt" else None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
