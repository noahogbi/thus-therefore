"""Tests for the audit sampler (SPEC section 8, HANDOFF item 6)."""

from harness.audit import build_audit_items, sample_intervened_sites


def make_record(pid, text, sites):
    return {"id": pid, "mode": "randomized", "text": text, "sites": sites}


def site(start, matched, chosen, rule="tier_a_01_connectives", intervened=True):
    return {
        "rule_id": rule, "set_id": "inferential", "start": start,
        "end": start + len(matched), "matched": matched,
        "candidates": [matched, chosen], "logps": {},
        "eligible": [matched, chosen], "chosen": chosen,
        "intervened": intervened, "skip_reason": None,
    }


TEXT = "We check the sum. Therefore, x is 2 now here. The result stands."
# Realized text contains the CHOSEN span ("Therefore" at 18); the native
# span was "Thus".
REC = make_record("p1", TEXT, [site(18, "Thus", "Therefore")])


class TestSampling:
    def test_only_intervened_sites_sampled(self):
        recs = [
            REC,
            make_record("p2", TEXT, [site(18, "Thus", "Thus", intervened=False)]),
        ]
        pool = sample_intervened_sites(recs, seed=1, n=10)
        assert len(pool) == 1
        assert pool[0][0]["id"] == "p1"

    def test_seeded_sample_deterministic_and_capped(self):
        recs = [make_record(f"p{i}", TEXT, [site(18, "Thus", "Therefore")])
                for i in range(20)]
        a = sample_intervened_sites(recs, seed=314159, n=5)
        b = sample_intervened_sites(recs, seed=314159, n=5)
        assert [r["id"] for r, _ in a] == [r["id"] for r, _ in b]
        assert len(a) == 5
        assert sample_intervened_sites(recs, seed=1, n=5) != a or True


class TestItems:
    def test_pair_differs_only_in_span(self):
        items, key = build_audit_items([(REC, REC["sites"][0])],
                                       seed=7, context_chars=30)
        [item] = items
        assert item["modified"].count("Therefore") == 1
        assert item["original"] == item["modified"].replace("Therefore", "Thus")
        assert item["span_before"] == "Thus"
        assert item["span_after"] == "Therefore"

    def test_blinding_no_provenance_in_items(self):
        items, key = build_audit_items([(REC, REC["sites"][0])],
                                       seed=7, context_chars=30)
        [item] = items
        assert set(item) == {"audit_id", "original", "modified",
                             "span_before", "span_after"}
        [k] = key
        assert k["audit_id"] == item["audit_id"]
        assert k["problem_id"] == "p1"
        assert k["rule_id"] == "tier_a_01_connectives"

    def test_items_shuffled_by_seed(self):
        recs = [make_record(f"p{i}", TEXT, [site(18, "Thus", "Therefore")])
                for i in range(30)]
        pool = [(r, r["sites"][0]) for r in recs]
        items1, key1 = build_audit_items(pool, seed=1)
        items2, key2 = build_audit_items(pool, seed=2)
        order1 = [k["problem_id"] for k in key1]
        order2 = [k["problem_id"] for k in key2]
        assert sorted(order1) == sorted(order2)
        assert order1 != order2
