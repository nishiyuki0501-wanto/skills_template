---
name: mext-education-ai-compliance
description: 文部科学省の教育AI・情報セキュリティガイドラインに準拠した開発・セキュリティチェックを行うスキル。生成AIガイドライン(Ver.2.0)、教育情報セキュリティポリシーガイドライン(令和7年3月版)に基づく。Use when checking MEXT compliance, education security, student data protection, or AI safety in school applications.
---

# 文部科学省 教育AI準拠チェッカー

学校向けアプリケーションが文部科学省のガイドラインに準拠しているかをチェックし、必要な修正を提案します。

## 参照ガイドライン

1. **初等中等教育段階における生成AIの利活用に関するガイドライン（Ver.2.0）** - 令和6年12月26日
2. **教育情報セキュリティポリシーに関するガイドライン** - 令和7年3月版
3. **教育データの利活用に係る留意事項（第1版）**

## When to Use This Skill

- 学校向けアプリケーションの開発時
- 教育データを扱うシステムのセキュリティレビュー
- 生成AI機能の実装時
- 児童生徒の個人情報を扱う機能の開発時
- 文科省ガイドライン準拠の確認が必要な時

---

## 1. 生成AI利活用の5原則

文部科学省ガイドラインが定める基本原則：

| 原則 | 内容 | 実装要件 |
|------|------|----------|
| **人間中心** | AIは手段であり目的ではない | ユーザーの最終判断を尊重するUI設計 |
| **安全性** | 適正利用・セキュリティ確保 | 入力検証、出力フィルタリング |
| **個人情報保護** | プライバシー・著作権保護 | データ匿名化、入力制限 |
| **公平性** | バイアスのない公正な利用 | 出力の検証、多様性配慮 |
| **透明性** | 説明責任の確保 | AI利用の明示、ログ記録 |

---

## 2. セキュリティチェックリスト

### 2.1 情報資産の分類

学校の情報資産は3分類で管理：

```
┌─────────────┬────────────────────────────────────┐
│  分類        │  含まれる情報                        │
├─────────────┼────────────────────────────────────┤
│  校務系      │  成績、出欠、指導要録、健康診断結果    │
│  学習系      │  ポートフォリオ、課題、学習履歴        │
│  公開系      │  学校HP、お知らせ、公開資料           │
└─────────────┴────────────────────────────────────┘
```

**重要性分類（4段階）:**
- **Ⅰ類**: 漏洩で重大な権利侵害（成績、健康情報）
- **Ⅱ類**: 漏洩で権利侵害の可能性（氏名、連絡先）
- **Ⅲ類**: 漏洩で業務に支障（時間割、カリキュラム）
- **Ⅳ類**: 漏洩しても影響軽微（公開情報）

### 2.2 必須セキュリティ要件

#### 認証・アクセス制御

```typescript
// 必須: 多要素認証の実装
interface AuthConfig {
  mfa: {
    enabled: true;
    methods: ('email' | 'sms' | 'authenticator')[];
  };
  sessionTimeout: number;  // 推奨: 30分以下
  passwordPolicy: {
    minLength: 12;
    requireUppercase: true;
    requireNumber: true;
    requireSymbol: true;
  };
}
```

**チェック項目:**
- [ ] 多要素認証（MFA）が実装されているか
- [ ] セッションタイムアウトが適切か（推奨30分以下）
- [ ] パスワードポリシーが十分か（12文字以上推奨）
- [ ] 失敗時のアカウントロックがあるか
- [ ] ロールベースアクセス制御（RBAC）が実装されているか

#### データ暗号化

```typescript
// 必須: 通信・保存時の暗号化
const securityConfig = {
  transport: {
    protocol: 'TLS 1.3',
    hsts: true,
    certificatePinning: true
  },
  storage: {
    algorithm: 'AES-256-GCM',
    keyManagement: 'Azure Key Vault',
    fieldLevelEncryption: ['grade', 'healthInfo', 'address']
  }
};
```

**チェック項目:**
- [ ] HTTPS（TLS 1.2以上）が強制されているか
- [ ] 機密データが暗号化保存されているか
- [ ] 暗号鍵の管理が適切か
- [ ] データベース接続が暗号化されているか

#### 監査ログ

```typescript
// 必須: 操作ログの記録
interface AuditLog {
  timestamp: Date;
  userId: string;
  userRole: 'student' | 'teacher' | 'admin';
  action: string;
  resource: string;
  ipAddress: string;
  result: 'success' | 'failure';
  details?: Record<string, unknown>;
}
```

**チェック項目:**
- [ ] 全てのデータアクセスがログ記録されているか
- [ ] ログに必要な情報が含まれているか
- [ ] ログの改ざん防止措置があるか
- [ ] ログの保存期間が適切か（推奨: 1年以上）

---

## 3. 生成AI機能のチェックリスト

### 3.1 入力制限

```typescript
// 必須: 個人情報のフィルタリング
const sensitivePatterns = [
  /\d{3}-\d{4}-\d{4}/,        // 電話番号
  /\d{3}-\d{4}/,              // 郵便番号
  /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}/,  // メールアドレス
  /\d{4}年\d{1,2}月\d{1,2}日/, // 生年月日パターン
];

function sanitizePrompt(input: string): string {
  let sanitized = input;
  for (const pattern of sensitivePatterns) {
    sanitized = sanitized.replace(pattern, '[REDACTED]');
  }
  return sanitized;
}
```

**チェック項目:**
- [ ] 個人情報の入力を検出・ブロックしているか
- [ ] 入力内容がAI学習に使用されない設定（オプトアウト）か
- [ ] プロンプトインジェクション対策があるか
- [ ] 入力文字数の制限があるか

### 3.2 出力制御

```typescript
// 必須: AI出力のフィルタリング
interface OutputFilter {
  contentFilter: {
    violence: boolean;
    adult: boolean;
    hate: boolean;
    selfHarm: boolean;
  };
  educationalValidation: boolean;
  disclaimer: string;
}

const outputConfig: OutputFilter = {
  contentFilter: {
    violence: true,
    adult: true,
    hate: true,
    selfHarm: true
  },
  educationalValidation: true,
  disclaimer: 'この回答はAIによる参考情報です。最終的な判断は教員が行ってください。'
};
```

**チェック項目:**
- [ ] 不適切コンテンツのフィルタリングがあるか
- [ ] AI生成であることが明示されているか
- [ ] 教育的観点での検証プロセスがあるか
- [ ] 誤情報リスクへの注意喚起があるか

---

## 4. 個人情報保護チェックリスト

### 4.1 取得・利用

**チェック項目:**
- [ ] 利用目的が明示されているか
- [ ] 必要最小限のデータのみ取得しているか
- [ ] 保護者への同意取得プロセスがあるか（未成年の場合）
- [ ] プライバシーポリシーが適切か

### 4.2 保管・管理

```typescript
// データ保持ポリシーの実装
interface DataRetentionPolicy {
  category: string;
  retentionPeriod: string;
  disposalMethod: 'encryption_delete' | 'physical_destruction';
}

const retentionPolicies: DataRetentionPolicy[] = [
  { category: '学習履歴', retentionPeriod: '卒業後5年', disposalMethod: 'encryption_delete' },
  { category: 'ポートフォリオ', retentionPeriod: '卒業後10年', disposalMethod: 'encryption_delete' },
  { category: '成績データ', retentionPeriod: '卒業後20年', disposalMethod: 'encryption_delete' },
  { category: 'ログデータ', retentionPeriod: '1年', disposalMethod: 'encryption_delete' },
];
```

**チェック項目:**
- [ ] データ保持期間が明確か
- [ ] 不要データの削除プロセスがあるか
- [ ] 暗号化消去が実装されているか
- [ ] アクセス権限が最小限に設定されているか

---

## 5. コードレビューチェックリスト

### 5.1 フロントエンド

```typescript
// 悪い例: クライアントに機密情報を露出
const StudentProfile = ({ student }) => {
  return <div data-student-id={student.id} data-grade={student.grade}>...</div>;
};

// 良い例: 必要な情報のみ表示
const StudentProfile = ({ student }) => {
  return <div>{student.displayName}</div>;
};
```

**チェック項目:**
- [ ] 機密データがHTMLに埋め込まれていないか
- [ ] コンソールに機密情報が出力されていないか
- [ ] ローカルストレージに機密データを保存していないか
- [ ] API レスポンスに不要な情報が含まれていないか

### 5.2 バックエンド

```typescript
// 悪い例: SQLインジェクション脆弱性
const query = `SELECT * FROM students WHERE name = '${name}'`;

// 良い例: パラメータ化クエリ
const student = await prisma.student.findMany({
  where: { name: name }
});

// 良い例: 権限チェック付き
app.get('/api/students/:id', authMiddleware, async (req, res) => {
  const user = req.user;
  const student = await prisma.student.findUnique({ where: { id: req.params.id } });

  if (!canAccessStudent(user, student)) {
    return res.status(403).json({ error: 'Access denied' });
  }

  res.json(sanitizeStudentData(student, user.role));
});
```

**チェック項目:**
- [ ] SQLインジェクション対策があるか
- [ ] 全APIに認証・認可チェックがあるか
- [ ] エラーメッセージに機密情報が含まれていないか
- [ ] レート制限が実装されているか
- [ ] 入力バリデーションが適切か

---

## AI Assistant Instructions

このスキルが起動されたら:

1. **まずプロジェクト構造を確認**
   - セキュリティ関連の設定ファイルを確認
   - 認証・認可の実装を確認
   - 個人情報を扱う箇所を特定

2. **チェックリストに沿って検証**
   - 各チェック項目を順番に確認
   - 問題点を優先度順にリスト化
   - 具体的な修正案を提示

3. **レポート形式で報告**
   ```
   ## 準拠状況サマリー
   - 準拠: X項目
   - 要改善: Y項目
   - 重大な問題: Z項目

   ## 重大な問題
   1. [問題の詳細と修正案]

   ## 要改善項目
   1. [問題の詳細と修正案]
   ```

Always:
- 具体的なファイルパスと行番号を示す
- ガイドラインの該当箇所を引用する
- 修正コードは実行可能な形で提供
- 優先度（Critical/High/Medium/Low）を明示

Never:
- 抽象的な指摘のみで終わらない
- セキュリティリスクを過小評価しない
- 個人情報の具体例をログに出力しない

---

## 参考リンク

- [生成AIの利活用に関するガイドライン（Ver.2.0）](https://www.mext.go.jp/content/20241226-mxt_shuukyo02-000030823_001.pdf)
- [教育情報セキュリティポリシーに関するガイドライン](https://www.mext.go.jp/content/20250325-mxt_jogai01-100003157_1.pdf)
- [教育データの利活用に係る留意事項](https://www.mext.go.jp/content/20230322-mxt_syoto01-195246_2.pdf)
