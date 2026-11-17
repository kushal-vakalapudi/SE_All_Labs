from cloud_storage_tier import (
    monitor_replication_latency,
    process_storage_tenants,
)


def test_default_fields_and_empty_buckets():
    tenants = [
        {},
        {"account_active": True},
        {
            "account_active": True,
            "tier": "cool",
            "buckets": [{"size_gb": 10}],
        },
        {
            "account_active": True,
            "tier": "hot",
            "buckets": [{"egress_gb": 120}],
        },
    ]

    assert process_storage_tenants(tenants, 0) == {
        "total_billed": 0.15,
        "status": "BILLED",
    }


def test_replication_latency_boundaries_and_streak_reset():
    assert monitor_replication_latency([[]]) == "SYNCED"
    assert monitor_replication_latency([[200, 201], [200, 201]]) == "SYNCED"
    assert monitor_replication_latency([[201, 201]]) == "SYNC_LAG_ALERT"
