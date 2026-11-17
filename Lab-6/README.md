# L6_L7_12 — Cloud Storage Tier

Lab 6: Code and Branch Coverage

## About

A small Python module that computes tenant storage and network egress costs across hot, cool, and archive storage tiers, and monitors distributed cluster nodes for replication latency spikes.

## Files

| File | Description |
|------|-------------|
| `cloud_storage_tier.py` | The module under test |
| `test_cloud_storage.py` | Starter test file |
| `CodeCoverageTest_cloud_storage_tier.py` | Tests for line/code coverage |
| `BranchCoverageTest_cloud_storage_tier.py` | Additional tests for decision branches |
| `CodeCoverageTest_output.png` | Line-coverage test and report output |
| `BranchCoverageTest_output.png` | Branch-coverage test and report output |

Keep all your Lab 6 work in this `LAB6` folder. Lab 7 will be added to this repo later.

Refer to the lab handout for instructions.

## Coverage analysis

Run the line-coverage test set:

```powershell
python -m coverage erase
python -m coverage run --source=cloud_storage_tier -m pytest -q test_cloud_storage.py CodeCoverageTest_cloud_storage_tier.py
python -m coverage report -m --include=cloud_storage_tier.py
```

Run the full branch-coverage test set:

```powershell
python -m coverage erase
python -m coverage run --branch --source=cloud_storage_tier -m pytest -q test_cloud_storage.py CodeCoverageTest_cloud_storage_tier.py BranchCoverageTest_cloud_storage_tier.py
python -m coverage report -m --include=cloud_storage_tier.py
```

The line-coverage test set achieves 100% statement coverage. The complete branch
test set achieves 100% statement and branch coverage for `cloud_storage_tier.py`.
The PNG files above contain the respective test and coverage command output.