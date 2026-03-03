"""Cane of Kulemak veiled mod probability calculator (all variants)"""
from math import comb, log

PREFIX_POOL = 18
SUFFIX_POOL = 17
SHOWN = 3  # choices shown per unveil

VARIANTS = {
    "1": ("Prefix 2 + Suffix 1", 2, 1),
    "2": ("Prefix 1 + Suffix 2", 1, 2),
    "3": ("Prefix 2 + Suffix 2", 2, 2),
}


def prob_hit(desired, pool, shown=SHOWN):
    """Probability that at least one of 'desired' mods appears in 'shown' choices from 'pool'."""
    if desired <= 0 or pool < shown:
        return 0.0
    return 1 - comb(pool - desired, shown) / comb(pool, shown)


def calc_slots(desired, pool, slots):
    """Probability of hitting a desired mod in each of 'slots' sequential unveils."""
    prob = 1.0
    for i in range(slots):
        prob *= prob_hit(desired - i, pool - i)
    return prob


def fmt(prob):
    if prob <= 0:
        return "impossible"
    return f"{prob:.4%}  (1/{1/prob:.1f})"


def main():
    print("=== Cane of Kulemak Probability Calculator ===")
    print(f"Prefix pool: {PREFIX_POOL}  Suffix pool: {SUFFIX_POOL}\n")
    for k, (name, _, _) in VARIANTS.items():
        print(f"  {k}: {name}")
    v = input("\nVariant (1/2/3): ").strip()
    if v not in VARIANTS:
        print("Invalid selection"); return
    name, p_slots, s_slots = VARIANTS[v]
    print(f"\nSelected: {name}")

    p = int(input(f"Desired prefixes (p, {p_slots} slots): "))
    s = int(input(f"Desired suffixes (s, {s_slots} slots): "))

    p_need = min(p, p_slots)  # if desired < slots, only that many need to hit
    s_need = min(s, s_slots)

    prefix_prob = calc_slots(p, PREFIX_POOL, p_need) if p_need > 0 else 1.0
    suffix_prob = calc_slots(s, SUFFIX_POOL, s_need) if s_need > 0 else 1.0
    total = prefix_prob * suffix_prob

    print(f"\n--- Result ({name}) ---")
    print(f"Prefix {p_need}/{p_slots} slots: {fmt(prefix_prob)}")
    print(f"Suffix {s_need}/{s_slots} slots: {fmt(suffix_prob)}")
    print(f"Total:            {fmt(total)}")

    if total > 0:
        print(f"\n--- Estimated attempts ---")
        for pct in [50, 75, 90, 99]:
            n = log(1 - pct / 100) / log(1 - total)
            print(f"  {pct}%: {n:.0f}")


if __name__ == "__main__":
    main()
