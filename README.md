# My Homepage

GitHub Pagesを使用した個人ホームページプロジェクトです。

## セットアップ手順

### 1. GitHubリポジトリの作成
1. [GitHub](https://github.com)にアクセスしてログイン
2. 右上の「+」ボタンから「New repository」を選択
3. Repository name: `my-homepage`（または任意の名前）
4. Publicを選択
5. 「Create repository」をクリック

### 2. ローカルリポジトリとGitHubの連携
```bash
cd HP-Project
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/my-homepage.git
git push -u origin main
```

### 3. GitHub Pagesの有効化
1. GitHubのリポジトリページへアクセス
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: main、/(root)を選択
5. Save

数分後、`https://YOUR_USERNAME.github.io/my-homepage/`でサイトが公開されます。

## ファイル構成
- `index.html` - メインページ
- `README.md` - このファイル

## カスタマイズ
`index.html`を編集して、自分の情報に更新してください。