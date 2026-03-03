# Cane of Kulemak Simulator

Path of Exile 1 のユニーク杖「Cane of Kulemak」で、望む veiled mod を引ける確率を計算するツール。

## 対応 Variant

| Variant | 構成 |
|---------|------|
| 1 | Prefix 2枠 + Suffix 1枠 |
| 2 | Prefix 1枠 + Suffix 2枠 |
| 3 | Prefix 2枠 + Suffix 2枠 |

## 前提

- Prefix pool: 18種
- Suffix pool: 17種
- アンベール時の選択肢: 3つ

## 使い方

```
python cane_calc.py
```

Variant を選び、当たり Prefix / Suffix の数を入力すると確率と試行回数の目安を表示します。

```
=== Cane of Kulemak 確率計算 ===
Prefix pool: 18  Suffix pool: 17

  1: Prefix 2 + Suffix 1
  2: Prefix 1 + Suffix 2
  3: Prefix 2 + Suffix 2

Variant (1/2/3): 1

選択: Prefix 2 + Suffix 1
当たりPrefixの数 (p, 2枠中): 2
当たりSuffixの数 (s, 1枠中): 1

--- 結果 (Prefix 2 + Suffix 1) ---
Prefix 2/2枠成功: 5.5363%  (1/18.1)
Suffix 1/1枠成功: 17.6471%  (1/5.7)
合計:            0.9770%  (1/102.4)

--- 試行回数目安 ---
  50%到達: 71回
  75%到達: 141回
  90%到達: 235回
  99%到達: 469回
```

当たり数が枠数より少ない場合は「その数だけ引ければ成功」として計算します（残り枠はどれでもOK）。

## 計算方法

各アンベールで N 個のプールから 3 つが表示され、当たり d 個のうち 1 つ以上含まれる確率:

```
P = 1 - C(N-d, 3) / C(N, 3)
```

複数枠は、選択済み mod がプールから除外される前提で逐次計算しています。
