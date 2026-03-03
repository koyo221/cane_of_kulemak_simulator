# Cane of Kulemak Simulator

A probability calculator for obtaining desired veiled mods on the unique staff "Cane of Kulemak" in Path of Exile 1.

> Based on mod pools and weights as of **patch 3.28**.

## Supported Variants

| Variant | Prefixes | Suffixes |
|---------|----------|----------|
| 1 | Catarina's Veiled x2 | of the Veil x2 |
| 2 | Catarina's Veiled x1 | of the Veil x2 |
| 3 | Catarina's Veiled x1 + Veiled x1 | of the Veil x1 |

## Mod Pools

### Catarina-exclusive prefixes (5)

| # | Mod |
|---|-----|
| 1 | +2 Support Gems Level, +Quality of Support Gems |
| 2 | CoC Support, Spell Damage |
| 3 | Chaos Explode |
| 4 | CWC Support, Spell Damage |
| 5 | Arcane Surge Support, Spell Damage |

### Generic veiled prefixes (13)

| # | Mod |
|---|-----|
| 6 | Phys Damage, Impale Chance |
| 7 | Phys Damage, Bleed Chance |
| 8 | Phys Damage, Blind Chance |
| 9 | Phys Damage, Poison Chance |
| 10 | Elemental Penetration |
| 11 | Chaos Resistance Penetration |
| 12 | Fire Damage, Ignite Chance |
| 13 | Cold Damage, Freeze Chance |
| 14 | Lightning Damage, Shock Chance |
| 15 | Chaos Damage, Chaos Skill Duration |
| 16 | Spell Damage, Mana Regen |
| 17 | Spell Damage, Non-Chaos as extra Chaos |
| 18 | Minion Damage, Minion Life |

### of the Veil suffixes (17)

| # | Mod |
|---|-----|
| 1 | Double Damage Chance |
| 2 | Minion Attack/Cast Speed |
| 3 | Chaos DoT Multiplier |
| 4 | Physical DoT Multiplier |
| 5 | Cold DoT Multiplier |
| 6 | Fire DoT Multiplier |
| 7 | Damage per Endurance Charge |
| 8 | Damage per Frenzy Charge |
| 9 | Damage per Power Charge |
| 10 | Crit Multi (Rare/Unique nearby) |
| 11 | Attack Speed (Rare/Unique nearby) |
| 12 | Double Damage while Focused |
| 13 | Attack Speed, Blood Rage on Kill |
| 14 | Cast Speed, Arcane Surge on Kill |
| 15 | Attack Speed, Dex+Int |
| 16 | Crit Chance, Str+Int |
| 17 | Accuracy, Str+Dex |

- **Catarina's Veiled** slot: draws from 18 mods (5 exclusive + 13 generic). Catarina-exclusive mods have weight **2**, generic mods have weight **1** (weighted sampling without replacement)
- **Veiled** slot: draws from 13 mods (generic only, uniform weight)
- **of the Veil** slot: draws from 17 suffix mods (uniform weight)
- Each unveil shows **3** candidates; the player picks one

## Usage

```
python cane_calc.py
```

Select a variant, then choose desired prefix and suffix mods from the displayed list. The tool outputs the success probability and estimated attempts needed.

## How It Works

### Uniform-weight pools (Veiled / of the Veil)

When 3 mods are shown from a pool of N, the probability that at least one of d desired mods appears:

```
P = 1 - C(N-d, 3) / C(N, 3)
```

For multiple slots, probabilities are computed recursively. After each unveil, only the chosen mod is removed from the pool (the 2 unchosen mods return to the pool):

```
P(need, d, N, slots) = P_hit * P(need-1, d-1, N-1, slots-1)
                      + P_miss * P(need, d, N-1, slots-1)
```

### Weighted pool (Catarina's Veiled)

The Catarina slot contains Catarina-exclusive mods (weight 2) and generic mods (weight 1). The 3 candidates are drawn via weighted sampling without replacement.

On miss, the optimal strategy is to remove a Catarina-exclusive non-desired mod first. Removing the higher-weight non-desired mod maximizes the proportion of desired weight in the remaining pool.

### Variant 3: mixed pools

Variant 3 spans two pools: one weighted Catarina slot and one uniform Veiled slot. Generic mods are shared between both pools, so selecting a generic mod from the Catarina slot also removes it from the Veiled pool. Inclusion-exclusion is used to compute branch probabilities, and the Veiled slot probability is calculated conditionally on the Catarina slot outcome.

## References

- [Cane of Kulemak - PoE Wiki](https://www.poewiki.net/wiki/Cane_of_Kulemak) — item overview, drop source (Catarina), base stats
- [List of veiled modifiers - PoE Wiki](https://www.poewiki.net/wiki/List_of_veiled_modifiers) — full veiled mod list with weights and spawn conditions
- [Veiled modifier - PoE Wiki](https://www.poewiki.net/wiki/Veiled_modifier) — unveil mechanics (candidate count, pool composition, Catarina-exclusive mod behavior)
- [Crafting - PoE Wiki](https://www.poewiki.net/wiki/Crafting#Veiled_modifiers) — general veiled mod crafting reference
