import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.verify_multiomics import verify


class MultiomicsVerificationTest(unittest.TestCase):
    def test_current_canonical_artifacts_pass(self):
        verify(Path("api/v1/multiomics"))

    def test_contract_failure_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "multiomics"
            shutil.copytree("api/v1/multiomics", root)
            summary = root / "summary.json"
            text = summary.read_text(encoding="utf-8")
            summary.write_text(text.replace('"study_count": ', '"study_count": 0, "ignored_study_count": ', 1), encoding="utf-8")
            with self.assertRaises((AssertionError, ValueError)):
                verify(root)

    def test_source_workflow_verifies_before_commit(self):
        workflow = Path(".github/workflows/multiomics-source.yml").read_text(encoding="utf-8")
        unit = workflow.index("python -m unittest discover -s tests -v")
        verify_step = workflow.index("python scripts/verify_multiomics.py --root api/v1/multiomics")
        commit = workflow.index("git commit -m 'data: update multiomics primary evidence'")
        push = workflow.index("git push")
        self.assertLess(unit, verify_step)
        self.assertLess(verify_step, commit)
        self.assertLess(commit, push)


if __name__ == "__main__":
    unittest.main()
