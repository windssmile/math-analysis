from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MkDocsBuildTests(unittest.TestCase):
    def test_theme_override_builds_in_strict_mode(self) -> None:
        completed = subprocess.run(
            ["mkdocs", "build", "--strict"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"mkdocs build failed:\n{completed.stdout}\n{completed.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
