---
name: performance-checker
description: コードの読み込みスピードとパフォーマンスを分析・改善提案するスキル。React/TypeScript/Vite/Node.js/Expressのパフォーマンス最適化、バンドルサイズ削減、レンダリング最適化に使用。Use when checking performance, optimizing load speed, reducing bundle size, or fixing slow rendering.
---

# Performance Checker

コードベースのパフォーマンス問題を特定し、読み込みスピードを向上させるための具体的な改善提案を行います。

## When to Use This Skill

- ページの読み込みが遅いと感じる時
- バンドルサイズを削減したい時
- Reactコンポーネントの再レンダリングを最適化したい時
- APIレスポンスを高速化したい時
- パフォーマンス監査を行う時

## チェック項目

### 1. フロントエンド（React/TypeScript/Vite）

#### バンドルサイズ

```bash
# バンドル分析
npm run build -- --report
# または
npx vite-bundle-visualizer
```

**チェックポイント:**
- [ ] 未使用のimportがないか
- [ ] 大きなライブラリの部分インポート（tree shaking）
- [ ] 動的インポート（code splitting）の活用
- [ ] 画像・アセットの最適化

**悪い例:**
```typescript
// 全体をインポート（バンドルサイズ増大）
import _ from 'lodash';
import * as Icons from 'lucide-react';
```

**良い例:**
```typescript
// 必要な関数のみインポート
import debounce from 'lodash/debounce';
import { Search, Menu } from 'lucide-react';
```

#### React再レンダリング最適化

**チェックポイント:**
- [ ] `useMemo`/`useCallback`の適切な使用
- [ ] `React.memo`によるコンポーネントメモ化
- [ ] 不要なstate更新の回避
- [ ] Context分割による再レンダリング範囲の制限

**悪い例:**
```typescript
// 毎回新しいオブジェクト/関数を生成
function Parent() {
  const handleClick = () => { /* ... */ };  // 毎回新しい関数
  const options = { a: 1, b: 2 };           // 毎回新しいオブジェクト
  return <Child onClick={handleClick} options={options} />;
}
```

**良い例:**
```typescript
function Parent() {
  const handleClick = useCallback(() => { /* ... */ }, []);
  const options = useMemo(() => ({ a: 1, b: 2 }), []);
  return <Child onClick={handleClick} options={options} />;
}

const Child = React.memo(({ onClick, options }) => { /* ... */ });
```

#### 遅延読み込み

**チェックポイント:**
- [ ] ルートベースのコード分割
- [ ] 重いコンポーネントの遅延読み込み
- [ ] 画像のlazy loading

**良い例:**
```typescript
// ルートの遅延読み込み
const AdminDashboard = React.lazy(() => import('./components/admin/AdminDashboard'));
const TeacherDashboard = React.lazy(() => import('./components/teacher/TeacherDashboard'));

// 画像のlazy loading
<img src={src} loading="lazy" alt="..." />
```

### 2. バックエンド（Node.js/Express/Prisma）

#### データベースクエリ最適化

**チェックポイント:**
- [ ] N+1クエリ問題の解消（`include`の使用）
- [ ] 必要なフィールドのみ取得（`select`）
- [ ] インデックスの適切な設定
- [ ] ページネーションの実装

**悪い例:**
```typescript
// N+1問題
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({ where: { userId: user.id } });
}
```

**良い例:**
```typescript
// includeでJOIN
const users = await prisma.user.findMany({
  include: { posts: true },
  select: { id: true, name: true, posts: { select: { title: true } } }
});
```

#### キャッシュ戦略

**チェックポイント:**
- [ ] Redis/メモリキャッシュの活用
- [ ] 適切なキャッシュ有効期限
- [ ] キャッシュ無効化戦略

**良い例:**
```typescript
// Redisキャッシュの活用
async function getUser(id: string) {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  const user = await prisma.user.findUnique({ where: { id } });
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  return user;
}
```

#### API最適化

**チェックポイント:**
- [ ] レスポンス圧縮（gzip/brotli）
- [ ] 適切なHTTPキャッシュヘッダー
- [ ] 不要なミドルウェアの削減
- [ ] 並列処理の活用

**良い例:**
```typescript
// 並列処理
const [users, posts, stats] = await Promise.all([
  prisma.user.findMany(),
  prisma.post.findMany(),
  getStats()
]);
```

### 3. 画像・アセット最適化

**チェックポイント:**
- [ ] WebP/AVIF形式の使用
- [ ] 適切なサイズの画像配信
- [ ] CDN活用
- [ ] SVGの最適化

### 4. ネットワーク最適化

**チェックポイント:**
- [ ] 不要なAPIコールの削減
- [ ] リクエストのバッチ化
- [ ] プリフェッチ/プリロード
- [ ] HTTP/2の活用

## 分析手順

1. **現状把握**
   - Lighthouse/PageSpeed Insightsでスコア確認
   - Network DevToolsでリクエスト分析
   - Bundle Analyzerでサイズ確認

2. **問題特定**
   - 大きなファイル/チャンクの特定
   - 遅いAPIエンドポイントの特定
   - 不要な再レンダリングの検出

3. **改善提案**
   - 優先度順にリスト化
   - 具体的なコード例を提示
   - 期待される改善効果を説明

4. **検証**
   - 改善前後のメトリクス比較
   - 回帰テストの実施

## AI Assistant Instructions

このスキルが起動されたら:

1. **まずコードベースを分析**
   - `package.json`で依存関係を確認
   - `src/`配下のコンポーネント構造を確認
   - `api/`配下のルート・サービスを確認

2. **問題を優先度順にリスト化**
   - Critical: 即座に対応が必要
   - High: 大きな改善が見込める
   - Medium: 改善の余地あり
   - Low: 将来的に検討

3. **具体的な修正案を提示**
   - 現在のコード
   - 改善後のコード
   - 期待される効果

Always:
- 具体的なファイルパスと行番号を示す
- 修正コードは実行可能な形で提供
- 副作用やリスクがある場合は明記

Never:
- 抽象的な提案のみで終わらない
- 測定なしに最適化を行わない
- 過度な最適化（premature optimization）を推奨しない

## パフォーマンス計測コマンド

```bash
# フロントエンドビルド分析
npm run build && npx vite-bundle-visualizer

# Lighthouseレポート
npx lighthouse http://localhost:5173 --output html --output-path ./lighthouse-report.html

# バンドルサイズ確認
du -sh dist/assets/*
```

## 関連ツール

- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Bundle Analyzer](https://github.com/btd/rollup-plugin-visualizer)
- [React DevTools Profiler](https://react.dev/learn/react-developer-tools)
- [Prisma Query Analyzer](https://www.prisma.io/docs/concepts/components/prisma-client/debugging)
