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
   # need token.json for google drive

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

1. Enter your financial analysis request in natural language.
2. The AI will interpret your request and fetch relevant data.
3. View the generated dashboard with charts and analysis.
4. Explore different visualizations and data points.

## Contributing 🤝

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- OpenAI for providing the GPT-4 API
- Federal Reserve Economic Data (FRED) for economic data
- Yahoo Finance for stock data
- The open-source community for various libraries and tools used in this project
