---
name: python-analysis
description: CSV/TSV/JSONを要約して洞察を返すスキル。必要に応じて同梱スクリプトを実行して数値サマリを取得する。Use when analyzing data, summarizing CSV files, or working with tabular data.
---

# Python Analysis - データ分析スキル

ユーザーから「データを分析して」「このCSVを要約して」などの依頼があった場合、以下を実行してください。

## When to Use This Skill

- CSVファイルを分析・要約する時
- TSV/JSONデータを解析する時
- データの概要を把握したい時
- 統計サマリが必要な時

---

## 分析プロセス

### Step 1: 入力確認

- 入力ファイルのパス、形式、分析目的（何を知りたいか）を確認する
- 不明なら質問

### Step 2: スクリプト実行

同梱スクリプト `scripts/analyze.py` を実行して概要を取得:

```bash
python3 scripts/analyze.py <path>
```

取得できる情報:
- 行数・列数
- 欠損値
- 数値統計（min, max, mean, stddev）
- サンプルデータ

### Step 3: 結果の解釈

- 結果を解釈し、結論と追加で有用な分析案を提案する
- 分布、相関、外れ値、可視化などの追加分析を提案

---

## スクリプトオプション

```bash
# 基本実行
python3 scripts/analyze.py data.csv

# 最大行数を指定
python3 scripts/analyze.py data.csv --max-rows 50000

# サンプルサイズを指定
python3 scripts/analyze.py data.csv --sample-size 10
```

---

## 出力フォーマット

```json
{
  "file": "/path/to/file.csv",
  "format": "csv",
  "rows": 1000,
  "columns": ["col1", "col2", "col3"],
  "missing": {"col1": 0, "col2": 5, "col3": 0},
  "numeric": {
    "col1": {"count": 1000, "min": 0, "max": 100, "mean": 50.5, "stddev": 15.2}
  },
  "sample": [...]
}
```

---

## Context

- 実行は読み取り専用で行い、入力ファイルを変更しない
- 個人情報が含まれる場合は、出力を集計中心にして生データの露出を避ける

---

## AI Assistant Instructions

このスキルが起動されたら:

1. **まずファイル情報を確認**
   - ファイルパスと形式を把握
   - 分析目的を確認

2. **スクリプトを実行**
   - analyze.py でサマリを取得
   - エラーがあれば対処

3. **結果を解釈・提案**
   - 統計サマリを分かりやすく説明
   - 追加分析の提案

Always:
- 数値は適切にフォーマット
- 外れ値や異常値を指摘
- 次のアクションを提案

Never:
- 個人情報を不用意に出力しない
- 入力ファイルを変更しない
