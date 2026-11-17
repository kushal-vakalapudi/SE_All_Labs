import pytest

from cloud_storage_tier import (
    monitor_replication_latency,
    process_storage_tenants,
)


def test_invalid_inputs_and_zero_usage():
    with pytest.raises(ValueError, match="Invalid tenants list or support fee"):
        process_storage_tenants(None, 0)

    with pytest.raises(ValueError, match="Invalid tenants list or support fee"):
        process_storage_tenants([], -1)

    assert process_storage_tenants([], 10) == {
        "total_billed": 0.0,
        "status": "ZERO_USAGE",
    }


def test_billing_lines_across_tiers_and_bucket_conditions():
    tenants = [
        {"account_active": False, "tier": "hot", "buckets": []},
        {
            "account_active": True,
            "tier": "hot",
            "has_backup_vault": True,
            "buckets": [
                {"size_gb": 100, "corrupted": False, "egress_gb": 50},
                {"size_gb": 501, "corrupted": False, "egress_gb": 120},
                {"size_gb": 0, "corrupted": False, "egress_gb": 120},
            ],
        },
        {
            "account_active": True,
            "tier": "cool",
            "buckets": [
                {"size_gb": 80, "corrupted": True, "egress_gb": 101},
                {"size_gb": 200, "corrupted": False, "egress_gb": 200},
            ],
        },
        {
            "account_active": True,
            "tier": "archive",
            "has_backup_vault": True,
            "buckets": [{"size_gb": 60, "corrupted": True, "egress_gb": 0}],
        },
        {"account_active": True, "tier": "invalid", "buckets": []},
    ]

    assert process_storage_tenants(tenants, 10) == {
        "total_billed": 46.45,
        "status": "BILLED",
    }


def test_audit_status_for_many_flagged_buckets():
    tenants = [
        {
            "account_active": True,
            "tier": "hot",
            "buckets": [{"size_gb": 0} for _ in range(5)],
        }
    ]

    assert process_storage_tenants(tenants, 0) == {
        "total_billed": 0.0,
        "status": "AUDIT_FLAGGED",
    }


def test_replication_monitor_lines():
    assert monitor_replication_latency([]) == "NO_DATA"
    assert monitor_replication_latency([[100]]) == "SYNCED"
    assert monitor_replication_latency([[201, 201]]) == "SYNC_LAG_ALERT"
