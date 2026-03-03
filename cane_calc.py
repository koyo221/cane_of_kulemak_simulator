"""Cane of Kulemak veiled mod probability calculator (all variants)"""
from math import comb, log
from functools import lru_cache

SHOWN = 3  # choices per unveil
CAT_WEIGHT = 2  # Cat-exclusive mod weight in Catarina pool
GEN_WEIGHT = 1  # Generic mod weight in Catarina pool

# --- Mod pools ---
CATARINA_PREFIXES = [
    "+2 to Level of Socketed Support Gems\n     +(5-8)% to Quality of Socketed Support Gems",
    "Socketed Gems are supported by Level 1 Cast On Critical Strike\n     (80-89)% increased Spell Damage",
    "Enemies you Kill have a (15-25)% chance to Explode,\n     dealing a quarter of their maximum Life as Chaos Damage",
    "Socketed Gems are Supported by Level 1 Cast While Channelling\n     (80-89)% increased Spell Damage",
    "Socketed Gems are Supported by Level 1 Arcane Surge\n     (80-89)% increased Spell Damage",
]

GENERIC_PREFIXES = [
    "(120-139)% increased Physical Damage\n     (21-25)% chance to Impale Enemies on Hit with Attacks",
    "(120-139)% increased Physical Damage\n     (21-25)% chance to cause Bleeding on Hit",
    "(120-139)% increased Physical Damage\n     (21-25)% chance to Blind Enemies on hit",
    "(120-139)% increased Physical Damage\n     (21-25)% chance to Poison on Hit",
    "Attacks with this Weapon Penetrate (14-16)% Elemental Resistances",
    "Attacks with this Weapon Penetrate (14-16)% Chaos Resistance",
    "(100-109)% increased Fire Damage, (35-40)% chance to Ignite",
    "(100-109)% increased Cold Damage, (35-40)% chance to Freeze",
    "(100-109)% increased Lightning Damage, (35-40)% chance to Shock",
    "(90-99)% increased Chaos Damage\n     Chaos Skills have (26-30)% increased Skill Effect Duration",
    "(100-109)% increased Spell Damage\n     (36-40)% increased Mana Regeneration Rate",
    "(90-99)% increased Spell Damage\n     Gain (9-10)% of Non-Chaos Damage as extra Chaos Damage",
    "Minions deal (50-59)% increased Damage\n     Minions have (50-59)% increased maximum Life",
]

SUFFIX_MODS = [
    "(12-14)% chance to deal Double Damage",
    "Minions have (34-38)% increased Attack Speed\n     Minions have (34-38)% increased Cast Speed",
    "+(44-48)% to Chaos Damage over Time Multiplier",
    "+(44-48)% to Physical Damage over Time Multiplier",
    "+(44-48)% to Cold Damage over Time Multiplier",
    "+(44-48)% to Fire Damage over Time Multiplier",
    "(7-8)% increased Damage per Endurance Charge",
    "(7-8)% increased Damage per Frenzy Charge",
    "(7-8)% increased Damage per Power Charge",
    "+(54-60)% Critical Strike Multiplier while a Rare or Unique Enemy is Nearby",
    "(27-30)% increased Attack Speed while a Rare or Unique Enemy is Nearby",
    "(36-40)% chance to deal Double Damage while Focused",
    "(18-22)% increased Attack Speed\n     15% chance to Trigger Level 1 Blood Rage when you Kill an Enemy",
    "(26-31)% increased Cast Speed\n     15% chance to gain Arcane Surge when you Kill an Enemy",
    "(18-22)% increased Attack Speed, +(25-28) to Dexterity and Intelligence",
    "(28-32)% increased Critical Strike Chance, +(25-28) to Strength and Intelligence",
    "+(311-350) to Accuracy Rating, +(25-28) to Strength and Dexterity",
]

# Pool sizes (derived)
CATARINA_EXCLUSIVE = len(CATARINA_PREFIXES)
GENERIC_PREFIX_COUNT = len(GENERIC_PREFIXES)
CATARINA_POOL = CATARINA_EXCLUSIVE + GENERIC_PREFIX_COUNT
VEILED_POOL = GENERIC_PREFIX_COUNT
SUFFIX_POOL = len(SUFFIX_MODS)

# Variant definitions
VARIANTS = {
    "1": {
        "name": "Catarina's Veiled x2 + of the Veil x2",
        "cat_slots": 2, "veiled_slots": 0, "suffix_slots": 2,
    },
    "2": {
        "name": "Catarina's Veiled x1 + of the Veil x2",
        "cat_slots": 1, "veiled_slots": 0, "suffix_slots": 2,
    },
    "3": {
        "name": "Catarina's Veiled x1 + Veiled x1 + of the Veil x1",
        "cat_slots": 1, "veiled_slots": 1, "suffix_slots": 1,
    },
}


def prob_hit(desired, pool, shown=SHOWN):
    """P(at least one desired mod appears in 'shown' choices from 'pool')."""
    if desired <= 0 or pool < shown or desired > pool:
        return 0.0
    return 1 - comb(pool - desired, shown) / comb(pool, shown)


@lru_cache(maxsize=None)
def prob_draws_from(cd, cn, gd, gn, k, a_cd, a_cn, a_gd, a_gn):
    """P(k weighted draws without replacement all come from allowed categories).

    cd/cn: desired/non-desired Cat-exclusive mods (weight CAT_WEIGHT each)
    gd/gn: desired/non-desired generic mods (weight GEN_WEIGHT each)
    a_*: whether each category is allowed
    """
    if k <= 0:
        return 1.0
    total_w = (cd + cn) * CAT_WEIGHT + (gd + gn) * GEN_WEIGHT
    if total_w <= 0:
        return 0.0
    result = 0.0
    if a_cd and cd > 0:
        result += (cd * CAT_WEIGHT / total_w) * prob_draws_from(
            cd - 1, cn, gd, gn, k - 1, a_cd, a_cn, a_gd, a_gn)
    if a_cn and cn > 0:
        result += (cn * CAT_WEIGHT / total_w) * prob_draws_from(
            cd, cn - 1, gd, gn, k - 1, a_cd, a_cn, a_gd, a_gn)
    if a_gd and gd > 0:
        result += (gd * GEN_WEIGHT / total_w) * prob_draws_from(
            cd, cn, gd - 1, gn, k - 1, a_cd, a_cn, a_gd, a_gn)
    if a_gn and gn > 0:
        result += (gn * GEN_WEIGHT / total_w) * prob_draws_from(
            cd, cn, gd, gn - 1, k - 1, a_cd, a_cn, a_gd, a_gn)
    return result


@lru_cache(maxsize=None)
def prob_multi(need, desired_in_pool, pool, slots):
    """P(filling at least 'need' slots with desired mods across 'slots' unveils).

    desired_in_pool: how many mods in the pool count as "desired".
    After each unveil the chosen mod is removed (pool shrinks by 1).
    If a desired mod is shown we pick it; otherwise we pick a non-desired mod.
    """
    if need <= 0:
        return 1.0
    if slots <= 0 or need > slots or pool < SHOWN or desired_in_pool < need:
        return 0.0
    p = prob_hit(desired_in_pool, pool)
    return (p * prob_multi(need - 1, desired_in_pool - 1, pool - 1, slots - 1)
            + (1 - p) * prob_multi(need, desired_in_pool, pool - 1, slots - 1))


@lru_cache(maxsize=None)
def prob_multi_cat(need, cd, cn, gd, gn, slots, prefer_cat):
    """P(filling 'need' desired across 'slots' weighted Catarina unveils).

    cd/cn: desired/non-desired Cat-exclusive (weight CAT_WEIGHT)
    gd/gn: desired/non-desired generic (weight GEN_WEIGHT)
    prefer_cat: when both Cat & generic desired shown, pick Cat desired first.
    """
    if need <= 0:
        return 1.0
    if slots <= 0 or cd + gd < need or need > slots:
        return 0.0
    if cd + cn + gd + gn < SHOWN:
        return 0.0

    # Branch probabilities via inclusion-exclusion
    p_miss = prob_draws_from(cd, cn, gd, gn, SHOWN,
                             False, True, False, True)
    p_no_cat_d = prob_draws_from(cd, cn, gd, gn, SHOWN,
                                 False, True, True, True)
    p_no_gen_d = prob_draws_from(cd, cn, gd, gn, SHOWN,
                                 True, True, False, True)
    p_miss_all_gn = prob_draws_from(cd, cn, gd, gn, SHOWN,
                                    False, False, False, True)

    p_only_cat_d = max(0.0, p_no_gen_d - p_miss)
    p_only_gen_d = max(0.0, p_no_cat_d - p_miss)
    p_both = max(0.0, 1.0 - p_no_cat_d - p_no_gen_d + p_miss)
    p_miss_cat_nd = max(0.0, p_miss - p_miss_all_gn)
    p_miss_gen_nd = p_miss_all_gn

    result = 0.0

    # Hit: only Cat desired shown → must pick Cat desired
    if cd > 0 and p_only_cat_d > 0:
        result += p_only_cat_d * prob_multi_cat(
            need - 1, cd - 1, cn, gd, gn, slots - 1, prefer_cat)

    # Hit: only generic desired shown → must pick generic desired
    if gd > 0 and p_only_gen_d > 0:
        result += p_only_gen_d * prob_multi_cat(
            need - 1, cd, cn, gd - 1, gn, slots - 1, prefer_cat)

    # Hit: both shown → pick per strategy
    if p_both > 0:
        if prefer_cat:
            result += p_both * prob_multi_cat(
                need - 1, cd - 1, cn, gd, gn, slots - 1, prefer_cat)
        else:
            result += p_both * prob_multi_cat(
                need - 1, cd, cn, gd - 1, gn, slots - 1, prefer_cat)

    # Miss: prefer removing Cat nd (weight 2 removal shrinks total more)
    if cn > 0 and p_miss_cat_nd > 0:
        result += p_miss_cat_nd * prob_multi_cat(
            need, cd, cn - 1, gd, gn, slots - 1, prefer_cat)

    # Miss: all shown are generic nd → must remove generic nd
    if gn > 0 and p_miss_gen_nd > 0:
        result += p_miss_gen_nd * prob_multi_cat(
            need, cd, cn, gd, gn - 1, slots - 1, prefer_cat)

    return result


def prefix_prob(vid, d_cat, d_gen):
    """Calculate prefix probability for a given variant."""
    v = VARIANTS[vid]
    cat_slots = v["cat_slots"]
    veiled_slots = v["veiled_slots"]
    d_total = d_cat + d_gen
    total_slots = cat_slots + veiled_slots
    need = min(d_total, total_slots)

    if need == 0:
        return 1.0

    cd = d_cat
    cn = CATARINA_EXCLUSIVE - d_cat
    gd = d_gen
    gn = GENERIC_PREFIX_COUNT - d_gen

    # Variants 1 & 2: all prefix slots are Catarina (weighted pool)
    if veiled_slots == 0:
        return prob_multi_cat(need, cd, cn, gd, gn, cat_slots, False)

    # Variant 3: mixed pools (1 Cat weighted + 1 Veiled uniform)
    return _prefix_mixed(cd, cn, gd, gn)


def _prefix_mixed(cd, cn, gd, gn):
    """Prefix probability for variant 3 (1 weighted Cat slot + 1 uniform Veiled slot)."""
    need = min(cd + gd, 2)

    if need == 0:
        return 1.0

    # Cat slot miss/hit probabilities (weighted)
    p_miss = prob_draws_from(cd, cn, gd, gn, SHOWN,
                             False, True, False, True)

    if need == 1:
        # Cat hit → done; Cat miss → Veiled must hit (generic desired only)
        p_miss_all_gn = prob_draws_from(cd, cn, gd, gn, SHOWN,
                                        False, False, False, True)
        p_miss_cat_nd = max(0.0, p_miss - p_miss_all_gn)
        p_miss_gen_nd = p_miss_all_gn

        # After Cat nd removed: Veiled pool unchanged
        p_v_after_cat_nd = prob_hit(gd, VEILED_POOL)
        # After generic nd removed: Veiled pool shrinks by 1
        p_v_after_gen_nd = prob_hit(gd, VEILED_POOL - 1)

        return ((1.0 - p_miss)
                + p_miss_cat_nd * p_v_after_cat_nd
                + p_miss_gen_nd * p_v_after_gen_nd)

    # need == 2: both slots must hit desired
    if gd == 0:
        return 0.0  # Veiled slot can never hit Cat-exclusive

    # Cat slot hit breakdown (prefer_cat=True: save generic desired for Veiled)
    p_no_cat_d = prob_draws_from(cd, cn, gd, gn, SHOWN,
                                 False, True, True, True)
    p_no_gen_d = prob_draws_from(cd, cn, gd, gn, SHOWN,
                                 True, True, False, True)

    p_only_cat_d = max(0.0, p_no_gen_d - p_miss)
    p_only_gen_d = max(0.0, p_no_cat_d - p_miss)
    p_both = max(0.0, 1.0 - p_no_cat_d - p_no_gen_d + p_miss)

    # prefer_cat=True: when both shown, pick Cat desired
    p_pick_cat_d = p_only_cat_d + p_both
    p_pick_gen_d = p_only_gen_d

    # After Cat desired picked: Veiled pool unchanged, gd desired remain
    p_v_after_cat = prob_hit(gd, VEILED_POOL)
    # After generic desired picked: Veiled pool - 1, gd - 1 desired remain
    p_v_after_gen = prob_hit(gd - 1, VEILED_POOL - 1)

    return p_pick_cat_d * p_v_after_cat + p_pick_gen_d * p_v_after_gen


def fmt(prob):
    if prob <= 0:
        return "impossible"
    return f"{prob:.4%}  (1/{1/prob:.1f})"


def show_mods(mods, offset=1):
    """Display numbered mod list and return next offset."""
    for i, mod in enumerate(mods, offset):
        print(f"  {i:>2}. {mod}")
    return offset + len(mods)


def parse_selection(text, valid_range):
    """Parse comma-separated numbers, return set of valid indices."""
    if not text.strip():
        return set()
    indices = set()
    for tok in text.split(","):
        tok = tok.strip()
        if tok.isdigit():
            n = int(tok)
            if n in valid_range:
                indices.add(n)
    return indices


def main():
    print("=== Cane of Kulemak Probability Calculator ===\n")

    for k, v in VARIANTS.items():
        print(f"  {k}: {v['name']}")

    vid = input("\nVariant (1/2/3): ").strip()
    if vid not in VARIANTS:
        print("Invalid selection")
        return

    v = VARIANTS[vid]
    total_prefix_slots = v["cat_slots"] + v["veiled_slots"]

    # --- prefix selection ---
    print(f"\n--- Prefix mods (select desired, {total_prefix_slots} slot(s)) ---")
    print("[Catarina-exclusive]")
    next_offset = show_mods(CATARINA_PREFIXES, 1)
    print("[Generic]")
    show_mods(GENERIC_PREFIXES, next_offset)
    total_prefix_mods = CATARINA_EXCLUSIVE + GENERIC_PREFIX_COUNT

    sel_text = input("\nDesired prefix mod numbers (comma-separated, empty=none): ")
    sel_prefix = parse_selection(sel_text, range(1, total_prefix_mods + 1))

    d_cat = len([i for i in sel_prefix if i <= CATARINA_EXCLUSIVE])
    d_gen = len([i for i in sel_prefix if i > CATARINA_EXCLUSIVE])

    # --- suffix selection ---
    print(f"\n--- Suffix mods (select desired, {v['suffix_slots']} slot(s)) ---")
    show_mods(SUFFIX_MODS, 1)

    sel_text = input("\nDesired suffix mod numbers (comma-separated, empty=none): ")
    sel_suffix = parse_selection(sel_text, range(1, SUFFIX_POOL + 1))
    d_suffix = len(sel_suffix)

    # --- show selections ---
    print("\n--- Selected mods ---")
    all_prefixes = CATARINA_PREFIXES + GENERIC_PREFIXES
    if sel_prefix:
        print("Prefix:")
        for i in sorted(sel_prefix):
            cat_mark = " [Cat]" if i <= CATARINA_EXCLUSIVE else ""
            print(f"  - {all_prefixes[i - 1]}{cat_mark}")
    else:
        print("Prefix: (none)")

    if sel_suffix:
        print("Suffix:")
        for i in sorted(sel_suffix):
            print(f"  - {SUFFIX_MODS[i - 1]}")
    else:
        print("Suffix: (none)")

    # --- calculate ---
    d_total = d_cat + d_gen
    need_suf = min(d_suffix, v["suffix_slots"])

    p_pre = prefix_prob(vid, d_cat, d_gen)
    p_suf = prob_multi(need_suf, d_suffix, SUFFIX_POOL, v["suffix_slots"])
    total = p_pre * p_suf

    print(f"\n--- Result ({v['name']}) ---")
    if vid == "3" and d_total > 0:
        print(f"Prefix {d_total} desired -> {total_prefix_slots} slots"
              f" (Cat: {d_cat}, generic: {d_gen}): {fmt(p_pre)}")
    else:
        print(f"Prefix {d_total} desired -> {total_prefix_slots} slots: {fmt(p_pre)}")
    print(f"Suffix {d_suffix} desired -> {v['suffix_slots']} slots: {fmt(p_suf)}")
    print(f"Total:  {fmt(total)}")

    if total > 0:
        print(f"\n--- Estimated attempts ---")
        for pct in [50, 75, 90, 99]:
            n = log(1 - pct / 100) / log(1 - total)
            print(f"  {pct}%: {n:.0f}")


if __name__ == "__main__":
    main()
