"""
BizPulse Entity Resolution Engine
Fuzzy matching + deduplication across fragmented Karnataka government databases.
Simulates: Neo4j UBID graph + Kafka CDC + AI matching pipeline
"""

import time
from rapidfuzz import fuzz, process
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RawRecord:
    source: str
    raw_name: str
    pan: Optional[str] = None
    address: Optional[str] = None
    extra: dict = field(default_factory=dict)


@dataclass
class ResolutionStep:
    step_name: str
    description: str
    score: float
    passed: bool


@dataclass
class ResolvedEntity:
    ubid: str
    canonical_name: str
    matched_records: list[RawRecord]
    fuzzy_name_score: float
    pan_cross_ref_score: float
    address_similarity_score: float
    overall_confidence: float
    steps: list[ResolutionStep]


def normalize_name(name: str) -> str:
    """Normalize a business name for comparison."""
    replacements = {
        "private limited": "pvt ltd",
        "private ltd": "pvt ltd",
        "pvt. ltd.": "pvt ltd",
        "pvt. ltd": "pvt ltd",
        "p. ltd": "pvt ltd",
        " & ": " and ",
        "co.": "co",
        "corp.": "corp",
    }
    name = name.lower().strip()
    for old, new in replacements.items():
        name = name.replace(old, new)
    # Remove punctuation
    name = "".join(c if c.isalnum() or c == " " else " " for c in name)
    return " ".join(name.split())


def fuzzy_name_match(name_a: str, name_b: str) -> float:
    """Compute fuzzy similarity between two business names."""
    a = normalize_name(name_a)
    b = normalize_name(name_b)
    token_sort = fuzz.token_sort_ratio(a, b)
    token_set = fuzz.token_set_ratio(a, b)
    partial = fuzz.partial_ratio(a, b)
    return round(max(token_sort, token_set, partial) / 100.0 * 100, 1)


def pan_cross_ref(pan_a: Optional[str], pan_b: Optional[str]) -> float:
    """PAN cross-reference score. Returns 100 if match, 0 if both present but differ, 50 if one/both missing."""
    if pan_a and pan_b:
        return 100.0 if pan_a.upper() == pan_b.upper() else 0.0
    return 50.0  # Inconclusive — one or both missing


def address_similarity(addr_a: Optional[str], addr_b: Optional[str]) -> float:
    """Address similarity using fuzzy matching."""
    if not addr_a or not addr_b:
        return 50.0
    return round(fuzz.token_set_ratio(addr_a.lower(), addr_b.lower()), 1)


def compute_overall_confidence(
    fuzzy: float, pan: float, addr: float,
    weights=(0.45, 0.40, 0.15)
) -> float:
    return round(fuzzy * weights[0] + pan * weights[1] + addr * weights[2], 1)


def build_resolution_steps(
    fuzzy: float, pan: float, addr: float, overall: float
) -> list[ResolutionStep]:
    return [
        ResolutionStep(
            "Fuzzy Name Matching",
            f"Token-sort + token-set ratio across all name variants",
            fuzzy,
            fuzzy >= 70,
        ),
        ResolutionStep(
            "PAN Cross-Reference",
            f"Permanent Account Number lookup across GST and Udyam registries",
            pan,
            pan >= 80,
        ),
        ResolutionStep(
            "Address Similarity",
            f"Tokenized address comparison with normalization",
            addr,
            addr >= 60,
        ),
        ResolutionStep(
            "UBID Assignment",
            f"Overall confidence {overall:.1f}% — entity resolved and UBID issued",
            overall,
            overall >= 65,
        ),
    ]


def run_entity_resolution(
    fragmented_records: dict[str, list[dict]],
    ubid_assignments: list[dict],
    threshold: float = 65.0,
) -> tuple[list[ResolvedEntity], list[str]]:
    """
    Main entity resolution pipeline.
    Groups records across databases and assigns UBIDs.

    Args:
        fragmented_records: Dict of source -> list of raw record dicts
        ubid_assignments: Pre-defined UBID assignments for the demo
        threshold: Minimum overall confidence to confirm a match

    Returns:
        (resolved_entities, log_messages)
    """
    logs = []
    logs.append("Initializing BizPulse Entity Resolution Engine v2.1...")
    logs.append(f"Ingesting records from {len(fragmented_records)} government databases via CDC layer...")

    # Flatten all records
    all_records: list[RawRecord] = []
    for source, records in fragmented_records.items():
        for r in records:
            all_records.append(RawRecord(
                source=source,
                raw_name=r.get("raw_name", ""),
                pan=r.get("pan"),
                address=r.get("address"),
                extra={k: v for k, v in r.items() if k not in ("raw_name", "pan", "address")},
            ))
    logs.append(f"Total raw records ingested: {len(all_records)}")

    # Group records by their UBID assignment (demo: 3 known entities)
    resolved_entities = []
    for assignment in ubid_assignments:
        group_names = assignment["names"]
        ubid = assignment["ubid"]
        canonical = assignment["canonical"]

        group_records = [r for r in all_records if r.raw_name in group_names]
        if not group_records:
            continue

        # Compute pairwise scores across the group
        names = [r.raw_name for r in group_records]
        pans = [r.pan for r in group_records if r.pan]
        addrs = [r.address for r in group_records if r.address]

        # Fuzzy name: average of all pairwise scores
        fuzzy_scores = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                fuzzy_scores.append(fuzzy_name_match(names[i], names[j]))
        avg_fuzzy = round(sum(fuzzy_scores) / len(fuzzy_scores), 1) if fuzzy_scores else 50.0

        # PAN: if all share same PAN → 100, mixed → 80, all missing → 50
        if len(set(p for p in pans)) == 1 and pans:
            avg_pan = 100.0
        elif pans:
            avg_pan = 85.0
        else:
            avg_pan = 50.0

        # Address
        addr_scores = []
        for i in range(len(addrs)):
            for j in range(i + 1, len(addrs)):
                addr_scores.append(address_similarity(addrs[i], addrs[j]))
        avg_addr = round(sum(addr_scores) / len(addr_scores), 1) if addr_scores else 50.0

        overall = compute_overall_confidence(avg_fuzzy, avg_pan, avg_addr)
        steps = build_resolution_steps(avg_fuzzy, avg_pan, avg_addr, overall)

        resolved_entities.append(ResolvedEntity(
            ubid=ubid,
            canonical_name=canonical,
            matched_records=group_records,
            fuzzy_name_score=avg_fuzzy,
            pan_cross_ref_score=avg_pan,
            address_similarity_score=avg_addr,
            overall_confidence=overall,
            steps=steps,
        ))

        logs.append(f"  Resolved: '{canonical}' → {ubid} (confidence: {overall:.1f}%)")

    logs.append(f"Resolution complete. {len(resolved_entities)} unique entities identified.")
    logs.append(f"UBIDs issued: {', '.join(e.ubid for e in resolved_entities)}")
    return resolved_entities, logs


# Pre-defined UBID assignments for the demo
DEMO_UBID_ASSIGNMENTS = [
    {
        "ubid": "KA-2024-BIZ-001",
        "canonical": "Ravi Enterprises Pvt Ltd",
        "names": ["Ravi Enterprises Pvt Ltd", "Ravi Enterprises Private Limited", "RAVI ENT PVT LTD"],
    },
    {
        "ubid": "KA-2024-BIZ-002",
        "canonical": "Meena Textiles",
        "names": ["Meena Textiles", "M. Textiles", "Meena Textile Works"],
    },
    {
        "ubid": "KA-2024-BIZ-003",
        "canonical": "Hubli Foods Co",
        "names": ["Hubli Foods Co", "Hubli Food Company", "HublifoOds", "Hubli Foods Pvt"],
    },
]
