# KaFin2: AI-Powered Finance Dashboard 🤖📊

## 概要

KaFin2は、最先端のAI技術と包括的な金融データ分析を組み合わせた革新的なオープンソースプロジェクトです。自然言語でコマンドを入力するだけで、金融データの分析や可視化を瞬時に実行できます。クラウドベースのソリューションとして、PCだけでなくモバイルデバイスからもアクセス可能で、常に最新の金融データとAI分析を提供します。

## 主な特徴 ✨

- AI駆動の自然言語インターフェース: OpenAI GPT-4による高度な言語理解と処理
- 動的ダッシュボード生成: ユーザーリクエストに基づくリアルタイムダッシュボード作成
- 包括的な金融データ: 複数のデータソースを統合した広範な金融データ分析
- 自動データ更新: クラウドサービスを活用した効率的なデータパイプライン
- 履歴管理: ユーザーリクエストとダッシュボードの永続化と再利用
- 最近使用したダッシュボードへの簡単アクセス: ホーム画面からワンクリックで過去の分析に再アクセス
- マルチデバイス対応: PCとモバイルデバイスの両方で利用可能
- クラウドネイティブ: スケーラブルでコスト効率の高いアーキテクチャ
- 完全無料: オープンソースツールと無料サービスによるコストゼロの運用

## アーキテクチャと技術スタック 🛠

### バックエンド
- 言語: Python 3.9+
- Webフレームワーク: Streamlit
- データ処理: Pandas, NumPy
- データ取得:
  - yfinance: 株式データ
  - FRED API: 経済指標
  - Google Drive API: データストレージと同期
- AI/ML: OpenAI API (GPT-4): 自然言語処理
- データベース: SQLite (ローカル開発), PostgreSQL (本番環境)

### フロントエンド
- Streamlitによる動的UIジェネレーション
- Plotly: インタラクティブな可視化
- Tailwind CSS: レスポンシブデザイン

### インフラストラクチャ
- ホスティング: Streamlit Cloud
- バージョン管理: GitHub
- CI/CD: GitHub Actions
- データストレージ: Google Drive
- スケジューリング: GitHub Actions (定期的なデータ更新用)

## フォルダ構成

```
kafin2/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── data_manager.py
│   ├── analysis.py
│   ├── visualization.py
│   └── ai_interface.py
│
├── data/
│   └── tickers.json
│
├── tests/
│   ├── __init__.py
│   ├── test_data_manager.py
│   ├── test_analysis.py
│   └── test_ai_interface.py
│
├── .github/
│   └── workflows/
│       └── update_data.yml
│
├── requirements.txt
└── README.md
```

## OpenAI Function Call

KaFin2は、OpenAI APIのfunction calling機能を活用して、ユーザーの自然言語入力を具体的な分析タスクに変換します。主要なfunction definitionの例:

```python
functions = [
    {
        "name": "get_stock_data",
        "description": "指定された銘柄の株価データを取得します",
        "parameters": {
            "type": "object",
            "properties": {
                "tickers": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "株式銘柄のリスト"
                },
                "start_date": {"type": "string", "format": "date"},
                "end_date": {"type": "string", "format": "date"}
            },
            "required": ["tickers"]
        }
    },
    {
        "name": "create_price_chart",
        "description": "株価チャートを作成します",
        "parameters": {
            "type": "object",
            "properties": {
                "tickers": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "株式銘柄のリスト"
                },
                "chart_type": {
                    "type": "string",
                    "enum": ["line", "candle"],
                    "description": "チャートのタイプ"
                }
            },
            "required": ["tickers", "chart_type"]
        }
    }
]
```

## 使用例 💡

1. "トヨタ自動車とホンダの株価を過去3ヶ月間比較して、ラインチャートで表示してください。"
2. "日経平均とS&P500の2023年のパフォーマンスを比較し、月次リターンの棒グラフを作成してください。"
3. "FRBのバランスシートと10年国債利回りの推移を過去5年分表示し、その相関関係を説明してください。"
4. "ドル円為替レートと日経平均の関係を示す散布図を作成し、直近1年間のデータポイントを表示してください。"
5. "GAFA（Google, Apple, Facebook, Amazon）の株価パフォーマンスを年初来で比較し、各社の騰落率をテーブルで表示してください。"

これらの例は、複雑な金融分析を必要とせず、基本的なデータ取得と可視化に焦点を当てています。

## クイックスタート 🚀

1. アプリにアクセス: https://kafin2.streamlit.app
2. GitHubアカウントでログイン
3. 自然言語で金融分析リクエストを入力
4. AIが生成したダッシュボードを閲覧・共有

## デプロイ方法 (開発者向け) 🖥

1. リポジトリをフォーク & クローン:
   ```
   git clone https://github.com/yourusername/kafin2.git
   cd kafin2
   ```

2. 仮想環境の作成と依存関係のインストール:
   ```
   python -m venv venv
   source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. 環境変数の設定:
   ```
   export OPENAI_API_KEY=your_openai_api_key
   export FRED_API_KEY=your_fred_api_key
   export GOOGLE_DRIVE_CREDENTIALS='{your_google_drive_credentials_json}'
   ```

4. ローカルでの実行:
   ```
   streamlit run app/main.py
   ```

5. Streamlit Cloudでのデプロイ:
   - GitHubリポジトリをStreamlit Cloudに接続
   - 環境変数を設定
   - デプロイボタンをクリック

6. GitHub Actionsの設定:
   - `.github/workflows/update_data.yml` を確認し、必要に応じて調整
   - リポジトリの Secrets に必要な環境変数を追加

KaFin2は、金融データの分析と可視化を簡単かつ直感的に行えるプラットフォームです。AIの力を借りて、複雑な金融情報を誰もが理解しやすい形で提供します。ぜひKaFin2を使って、あなたの金融分析を次のレベルに引き上げてください！

## 今後の改善点

- 言語入力インターフェースではガイド機能やカスタムルールを追加し、ユーザーの意図を正確に理解する仕組みを作る。
- キャッシュやconcurrentの処理を追加し、データ取得を効率化する。
- シンプルなデフォルト設定を進め、ユーザーフレンドリーなUIを提供する。
- チュートリアルを追加する。
- 自動テストを強化する。
