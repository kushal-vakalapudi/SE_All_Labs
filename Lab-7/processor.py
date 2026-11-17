import math
import re
from typing import Optional


def parse_storage_quota(quota_str: object) -> Optional[str]:
    """
    Parse a storage quota into GB, returning None for invalid input.

    Accepted format: '<non-negative integer><unit>' where unit is MB, GB, or TB.
    """
    if not isinstance(quota_str, str):
        return None

    cleaned = quota_str.strip().upper()
    multipliers = {
        "MB": 0.001,
        "GB": 1.0,
        "TB": 1000.0
    }
    match = re.fullmatch(r"([0-9]+)(MB|GB|TB)", cleaned)
    if match is None:
        return None

    try:
        value = int(match.group(1))
    except ValueError:
        return None

    unit = match.group(2)
    gb_total = value * multipliers[unit]
    return f"Quota: {gb_total:.2f} GB"


def compute_compression_ratio(size_metric_str: object) -> Optional[float]:
    """
    Compute raw_bytes / compressed_bytes, returning None for invalid input.

    Both values must be finite and non-negative, and compressed_bytes must
    be greater than zero.
    """
    if not isinstance(size_metric_str, str):
        return None

    parts = size_metric_str.split(":")
    if len(parts) != 2:
        return None

    try:
        raw_bytes, comp_bytes = (float(part.strip()) for part in parts)
    except ValueError:
        return None

    if (
        not math.isfinite(raw_bytes)
        or not math.isfinite(comp_bytes)
        or raw_bytes < 0
        or comp_bytes <= 0
    ):
        return None

    ratio = raw_bytes / comp_bytes
    if not math.isfinite(ratio):
        return None

    return round(ratio, 2)


def lookup_bandwidth_tier_rate(tier_descriptor: object) -> Optional[float]:
    """
    Look up the egress rate by tier prefix, returning None for invalid input.
    """
    if not isinstance(tier_descriptor, str):
        return None

    prefix = tier_descriptor.strip().upper()[:3]
    tier_rates = {
        "HOT": 0.08,
        "COL": 0.05,
        "ARC": 0.02
    }
    return tier_rates.get(prefix)


def main() -> None:
    print("==== Running parse_storage_quota ====")
    q_input = input("Enter quota (e.g. 500MB, 10GB, 2TB): ")
    quota_result = parse_storage_quota(q_input)
    print(quota_result if quota_result is not None else "Invalid quota.")

    print("\n==== Running compute_compression_ratio ====")
    c_input = input("Enter raw:compressed bytes (e.g. 1024:256): ")
    ratio_result = compute_compression_ratio(c_input)
    if ratio_result is None:
        print("Invalid compression metrics.")
    else:
        print("Compression Ratio:", ratio_result)

    print("\n==== Running lookup_bandwidth_tier_rate ====")
    t_input = input("Enter tier descriptor (e.g. HOT_TIER, COLD, ARCHIVE): ")
    rate_result = lookup_bandwidth_tier_rate(t_input)
    if rate_result is None:
        print("Invalid storage tier.")
    else:
        print("Rate per GB: $", rate_result)

if __name__ == "__main__":
    main()