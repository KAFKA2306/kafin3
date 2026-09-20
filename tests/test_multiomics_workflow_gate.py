import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class MultiomicsWorkflowGateTest(unittest.TestCase):
    def test_source_verifies_before_commit(self):
        workflow = Path('.github/workflows/multiomics-source.yml').read_text()
        unit_tests = workflow.index('python -m unittest discover -s tests -v')
        verify = workflow.index('python scripts/verify_multiomics.py')
        commit = workflow.index('git commit -m')
        push = workflow.index('git push')
        self.assertLess(unit_tests, commit)
        self.assertLess(verify, commit)
        self.assertLess(commit, push)

    def test_ci_and_source_share_verifier(self):
        source = Path('.github/workflows/multiomics-source.yml').read_text()
        ci = Path('.github/workflows/ci.yml').read_text()
        command = 'python scripts/verify_multiomics.py'
        self.assertIn(command, source)
        self.assertIn(command, ci)

    def test_shared_verifier_rejects_contract_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'multiomics'
            shutil.copytree('api/v1/multiomics', root)
            summary_path = root / 'summary.json'
            summary = json.loads(summary_path.read_text())
            summary['clinical_trials']['study_count'] = -1
            summary_path.write_text(json.dumps(summary))

            result = subprocess.run(
                [sys.executable, 'scripts/verify_multiomics.py', '--root', str(root)],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
