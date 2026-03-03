# Cane of Kulemak Simulator

A probability calculator for obtaining desired veiled mods on the unique staff "Cane of Kulemak" in Path of Exile 1.

## Supported Variants

| Variant | Slots |
|---------|-------|
| 1 | Prefix x2 + Suffix x1 |
| 2 | Prefix x1 + Suffix x2 |
| 3 | Prefix x2 + Suffix x2 |

## Assumptions

- Prefix pool: 18 mods
- Suffix pool: 17 mods
- Choices shown per unveil: 3

## Usage

```
python cane_calc.py
```

Select a variant, then enter the number of desired prefixes / suffixes to see the probability and estimated number of attempts.

```
=== Cane of Kulemak Probability Calculator ===
Prefix pool: 18  Suffix pool: 17

  1: Prefix 2 + Suffix 1
  2: Prefix 1 + Suffix 2
  3: Prefix 2 + Suffix 2

Variant (1/2/3): 1

Selected: Prefix 2 + Suffix 1
Desired prefixes (p, 2 slots): 2
Desired suffixes (s, 1 slot):  1

--- Result (Prefix 2 + Suffix 1) ---
Prefix 2/2 slots: 5.5363%  (1/18.1)
Suffix 1/1 slots: 17.6471%  (1/5.7)
Total:            0.9770%  (1/102.4)

--- Estimated attempts ---
  50%: 71
  75%: 141
  90%: 235
  99%: 469
```

If the number of desired mods is less than the number of slots, only that many need to hit (remaining slots accept anything).

## How it works

For each unveil, 3 mods are shown from a pool of N. The probability that at least one of d desired mods appears:

```
P = 1 - C(N-d, 3) / C(N, 3)
```

For multiple slots, probabilities are calculated sequentially with the chosen mod removed from the pool after each unveil.
