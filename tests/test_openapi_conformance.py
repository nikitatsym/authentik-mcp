"""All public operations must match the single supported API schema."""
import subprocess
import sys
from pathlib import Path


def test_public_request_contract():
    result = subprocess.run(
        [sys.executable, "codegen/check_contract.py"],
        cwd=Path(__file__).resolve().parent.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
