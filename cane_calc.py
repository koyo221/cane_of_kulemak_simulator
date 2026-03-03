"""Cane of Kulemak 確率計算 (全Variant対応)"""
from math import comb, log

PREFIX_POOL = 18
SUFFIX_POOL = 17
SHOWN = 3

VARIANTS = {
    "1": ("Prefix 2 + Suffix 1", 2, 1),
    "2": ("Prefix 1 + Suffix 2", 1, 2),
    "3": ("Prefix 2 + Suffix 2", 2, 2),
}


def prob_hit(desired, pool, shown=SHOWN):
    """pool個の中からshown個表示されたとき、desired個の当たりが1つ以上含まれる確率"""
    if desired <= 0 or pool < shown:
        return 0.0
    return 1 - comb(pool - desired, shown) / comb(pool, shown)


def calc_slots(desired, pool, slots):
    """slots回のアンベールでslots個の当たりを引く確率"""
    prob = 1.0
    for i in range(slots):
        prob *= prob_hit(desired - i, pool - i)
    return prob


def fmt(prob):
    if prob <= 0:
        return "不可能"
    return f"{prob:.4%}  (1/{1/prob:.1f})"


def main():
    print("=== Cane of Kulemak 確率計算 ===")
    print(f"Prefix pool: {PREFIX_POOL}  Suffix pool: {SUFFIX_POOL}\n")
    for k, (name, _, _) in VARIANTS.items():
        print(f"  {k}: {name}")
    v = input("\nVariant (1/2/3): ").strip()
    if v not in VARIANTS:
        print("無効な選択です"); return
    name, p_slots, s_slots = VARIANTS[v]
    print(f"\n選択: {name}")

    p = int(input(f"当たりPrefixの数 (p, {p_slots}枠中): "))
    s = int(input(f"当たりSuffixの数 (s, {s_slots}枠中): "))

    p_need = min(p, p_slots)  # 当たりが枠より少なければ、その数だけ引ければOK
    s_need = min(s, s_slots)

    prefix_prob = calc_slots(p, PREFIX_POOL, p_need) if p_need > 0 else 1.0
    suffix_prob = calc_slots(s, SUFFIX_POOL, s_need) if s_need > 0 else 1.0
    total = prefix_prob * suffix_prob

    print(f"\n--- 結果 ({name}) ---")
    print(f"Prefix {p_need}/{p_slots}枠成功: {fmt(prefix_prob)}")
    print(f"Suffix {s_need}/{s_slots}枠成功: {fmt(suffix_prob)}")
    print(f"合計:            {fmt(total)}")

    if total > 0:
        print(f"\n--- 試行回数目安 ---")
        for pct in [50, 75, 90, 99]:
            n = log(1 - pct / 100) / log(1 - total)
            print(f"  {pct}%到達: {n:.0f}回")


if __name__ == "__main__":
    main()
