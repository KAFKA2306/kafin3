# KaFin2: AI搭載ファイナンスダッシュボード 🤖📊

KaFin2は、最先端のAI技術と包括的な金融データ分析を組み合わせた革新的なオープンソースプロジェクトです。自然言語コマンドを使用して金融データを分析・可視化します。

## 主な機能 ✨

- AI駆動の自然言語インターフェース（OpenAI GPT-4）
- 動的ダッシュボード生成
- 包括的な金融データ分析
- 自動データ更新
- マルチデバイス対応
- クラウドネイティブアーキテクチャ
- 無料でオープンソース

## 技術スタック 🛠

- バックエンド: Python, FastAPI, Pandas, NumPy, yfinance, FRED API, Google Drive API
- AI/ML: OpenAI API (GPT-4), scikit-learn
- フロントエンド: React, Recharts, Tailwind CSS
- インフラ: GitHub, GitHub Actions

## クイックスタート 🚀

### バックエンドセットアップ

1. リポジトリをクローン:
   ```
   git clone https://github.com/KAFKA2306/savvy-dashboard-ai.git
   cd savvy-dashboard-ai
   ```

2. Conda環境を作成してアクティブ化:
   ```
   conda create -n kafin2 python=3.9
   conda activate kafin2
   ```

3. 依存関係をインストール:
   ```
   pip install -r requirements.txt
   ```

4. 環境変数を設定:
   - `.env.example` ファイルを `.env` にコピー
   - OpenAIとFREDのAPIキーを入力

5. FastAPIサーバーを実行:
   ```
   uvicorn src.backend.main:app --reload
   ```

### フロントエンドセットアップ

1. プロジェクトルートディレクトリにいることを確認

2. 依存関係をインストール:
   ```
   npm install
   ```

3. 開発サーバーを起動:
   ```
   npm run dev
   ```

4. ブラウザで表示されたローカルアドレスにアクセス（通常 `http://localhost:8080`）

## 使用方法 💡

1. 自然言語で金融分析リクエストを入力
2. AIがリクエストを解釈し、関連データを取得
3. 生成されたダッシュボードでチャートと分析を表示
4. 様々な可視化とデータポイントを探索
