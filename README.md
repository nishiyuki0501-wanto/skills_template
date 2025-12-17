# Skills Template

Claude CodeおよびCodexのSKILLSテンプレートプロジェクトです。このテンプレートを使用して、スキルを効率的に作成・管理できます。

## 概要

このプロジェクトは、Claude CodeとCodexの両方で使用可能な、実績のあるスキル集を含むテンプレートです。以下の特徴があります:

- **事前構成されたスキル**: 7つの実用的なスキルがすぐに使用可能
- **両プラットフォーム対応**: `.claude`と`.codex`フォルダにそれぞれのスキルを用意
- **スキルジェネレーター**: 新しいスキルを自動生成するためのスキルガイドを付属
- **ベストプラクティス**: スキル開発の標準化されたアプローチを採用

## ディレクトリ構造

```
skills_template/
├── .claude/                          # Claude Code スキル
│   ├── skills/
│   │   ├── claude-skill-generator/   # スキル作成ガイド
│   │   ├── technical-writing/        # 技術文書作成スキル
│   │   ├── app-analyzer/             # アプリ分析スキル
│   │   ├── performance-checker/      # パフォーマンス検証スキル
│   │   ├── error-analyzer/           # エラー分析スキル
│   │   ├── python-analysis/          # Python分析スキル
│   │   └── mext-education-ai-compliance/  # MEXT教育AI準拠スキル
│   ├── CLAUDE.md
│   └── settings.local.json
│
├── .codex/                           # Codex スキル
│   ├── skills/
│   │   ├── codex-skill-generator/    # スキル作成ガイド（Codex版）
│   │   ├── writing-skill/            # 文書作成スキル
│   │   ├── app-analyzer/             # アプリ分析スキル
│   │   ├── performance-checker/      # パフォーマンス検証スキル
│   │   ├── error-analyzer/           # エラー分析スキル
│   │   ├── python-analysis/          # Python分析スキル
│   │   └── mext-education-ai-compliance/  # MEXT教育AI準拠スキル
│   └── README.md
│
└── README.md                          # このファイル
```

## 含まれるスキル

### Claude Code スキル (`.claude/skills/`)

| スキル名 | 説明 | 用途 |
|---------|------|------|
| **claude-skill-generator** | スキル作成のための完全ガイド | 新しいスキルを作成する時、スキル構造を学ぶ時 |
| **technical-writing** | 技術文書作成ガイド | ドキュメント、技術記事、API仕様を作成する時 |
| **app-analyzer** | アプリケーション分析 | コード品質、構造、依存関係を分析する時 |
| **performance-checker** | パフォーマンス検証 | アプリケーションのパフォーマンスを測定・改善する時 |
| **error-analyzer** | エラーメッセージ分析 | エラーの原因追跡とデバッグを行う時 |
| **python-analysis** | Python コード分析 | Pythonコードを分析・最適化する時 |
| **mext-education-ai-compliance** | MEXT教育AI準拠 | 教育AI関連のプロジェクトで準拠確認が必要な時 |

### Codex スキル (`.codex/skills/`)

Codeスキルと同様の機能を提供するCodexプラットフォーム用スキル群です。

## 使用方法

### 1. テンプレートを複製する

```bash
git clone https://github.com/nishiyuki0501-wanto/skills_template.git my-skills-project
cd my-skills-project
```

### 2. Claude Codeで使用する

```bash
# Claude Codeでプロジェクトを開く
claude-code .
```

Claude Codeが起動すると、`.claude/skills/`以下のすべてのスキルが自動的に読み込まれます。

### 3. 新しいスキルを作成する

スキル作成ガイドを使用して新しいスキルを生成します:

```bash
# Claude Code内で以下を実行
/skill claude-skill-generator
```

または、Claude Codeに「新しいスキルを作成したい」と伝えると、スキル作成スキルが自動的に有効化されます。

## スキル作成のベストプラクティス

スキルを作成する際は、以下のポイントに注意してください:

### 1. ディレクトリ構造
```
skills/my-new-skill/
├── SKILL.md              # スキル定義ファイル (必須)
├── reference.md          # 参考ドキュメント (オプション)
├── templates/            # テンプレートファイル (オプション)
│   └── template1.txt
└── scripts/              # スクリプト (オプション)
    └── setup.sh
```

### 2. SKILL.md の必須要素

```yaml
---
name: my-skill-name          # 小文字・ハイフンのみ、64文字以内
description: 何ができるのか、いつ使うのか # 1024文字以内
---

# スキルタイトル

[スキルの詳細説明]
```

### 3. スキルの説明に含めるべき要素

- **何ができるのか**: 具体的な機能説明
- **いつ使うのか**: トリガーキーワード、使用シーン
- **ユースケース**: 実際の利用例

### 4. スキル内容の構成

- When to Use This Skill: 使用シーン
- Core Concepts: コア概念
- Instructions: 手順
- Examples: 具体例
- Best Practices: ベストプラクティス
- AI Assistant Instructions: Claude向けの指示

詳細は `./claude/skills/claude-skill-generator/SKILL.md` を参照してください。

## スキルの構成要素の詳細

### SKILL.md ファイル

各スキルは `SKILL.md` ファイルで定義されます。このファイルは以下で構成されます:

1. **YAML フロントマター**
   ```yaml
   ---
   name: スキル識別子
   description: スキルの説明
   allowed-tools: [読み取り専用スキルの場合]
   ---
   ```

2. **マークダウンコンテンツ**
   - スキル説明
   - 使用方法
   - 具体例
   - トラブルシューティング

### 補助ファイル (オプション)

- `reference.md`: 詳細リファレンス
- `templates/`: 再利用可能なテンプレート
- `scripts/`: ヘルパースクリプト (Python/Shell)

## スキル開発のワークフロー

### 1. スキルの計画

どのような問題を解決するのか、どのような場面で使うのかを明確にします。

### 2. スキル作成

`claude-skill-generator` を使用して、スキル構造を生成します。

### 3. コンテンツ作成

- 明確な説明文を作成
- 具体例を追加
- ベストプラクティスを記述

### 4. テスト

- キーワードトリガーのテスト
- スキルの有効化確認
- 指示の実行確認

### 5. 反復改善

実際の使用フィードバックをもとに改善します。

## スキル生成のトリガー

Claude Codeは以下のようなプロンプトでスキルを自動認識します:

- "新しいスキルを作成したい"
- "スキルのテンプレートを作成して"
- "コードを分析するスキルを作りたい"

スキルを使用させたい場合は、スキルの説明に含まれるキーワードを含むプロンプトを使用してください。

## 既存スキルの拡張

既存スキルを拡張するには:

1. スキルフォルダを開く: `.claude/skills/skill-name/`
2. `SKILL.md` を編集して内容を追加
3. 必要に応じて補助ファイルを追加
4. `git add` / `git commit` / `git push` で変更を保存

## チームでの使用

### プロジェクトスキルの共有

1. スキルを `.claude/skills/` に作成
2. Git にコミット
   ```bash
   git add .claude/skills/
   git commit -m "feat: add new skill"
   git push
   ```
3. チームメンバーが `git pull` で取得

### 個人スキルとプロジェクトスキル

- **プロジェクトスキル** (`.claude/skills/`): プロジェクト内で共有
- **個人スキル** (`~/.claude/skills/`): ユーザー個人のみ

## トラブルシューティング

### スキルが認識されない

- [ ] `SKILL.md` ファイルが存在するか確認
- [ ] ディレクトリ名が小文字とハイフンのみか確認
- [ ] YAML フロントマターが正しいか確認
- [ ] Claude Code を再起動

### スキルが想定外のタイミングで有効化される

- [ ] 説明文のキーワードが過度に広くないか確認
- [ ] トリガーキーワードをより具体的にする
- [ ] 他のスキルとのキーワード重複を確認

## サンプルスキル

このテンプレートには以下のサンプルスキルが含まれています:

1. **claude-skill-generator**: スキル作成のための完全ガイド
2. **technical-writing**: 技術文書作成スキル
3. **app-analyzer**: アプリケーション分析スキル

これらを参考にして、新しいスキルを作成できます。

## ドキュメントリンク

- [Claude Code 公式ドキュメント](https://claude.com/claude-code)
- [Codex スキル ドキュメント](https://www.anthropic.com)
- [スキル作成ガイド](`.claude/skills/claude-skill-generator/SKILL.md`)

## ライセンス

このテンプレートプロジェクトはMITライセンスの下で公開されています。

## コントリビューション

スキルの改善提案やバグ報告は GitHub Issues でお願いします。

---

**最後に更新**: 2025-12-17
