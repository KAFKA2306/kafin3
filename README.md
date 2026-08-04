# kafin3 — 2024年のAI金融分析prototype

> **状態: legacy / 動作未確認**  
> FastAPIを使った金融データ取得・要約の試作コードは存在しますが、現在のdefault branchをそのままセットアップして利用できる状態ではありません。稼働中のサービス、検証済みの投資分析基盤、現行OpenAI API対応製品ではありません。

## 目的

株価またはFRED系列を取得し、基本統計とLLMによる短い説明を返すAPIを試作したリポジトリです。Google DriveへのCSV保存も試行しています。

## 現在確認できる実装

`src/backend/main.py`には次の処理があります。

- FastAPIの`/analyze` endpoint
- yfinanceによる株価取得
- FRED APIによる経済系列取得
- 平均、標準偏差、最小値、最大値、期間騰落率の計算
- OpenAI APIを使った文章生成の試行
- Google DriveへのCSV uploadの試行

依存候補はrootの`requirements.txt`に記載されています。

## そのまま利用できない理由

| 項目 | 現在の状態 |
|---|---|
| OpenAI | `text-davinci-002`と旧Completion APIを使用しており、現行構成への移行が必要 |
| setup | 旧READMEが案内した`src/backend/requirements.txt`は存在しない |
| frontend | 旧READMEが案内した`frontend/`と`package.json`を確認できない |
| Google Drive | 実行directoryの`token.json`に依存し、credential管理契約が未整備 |
| version固定 | lock fileなし。依存versionの再現性なし |
| test | 自動testを確認できない |
| CI/CD | 検証・deployment workflowを確認できない |
| 公開環境 | 稼働中deploymentのcommit・URL対応を確認できない |

したがって、旧READMEにあった「GPT-4を使う高度なdashboard」「React frontend」「利用可能な自然言語分析」などの現在形の説明は撤回します。

## セキュリティ

- `.env`、`credentials.json`、`token.json`をcommitしない
- Google Drive tokenを共有環境で使い回さない
- API error本文へcredentialや内部pathを含めない
- 任意ticker・任意FRED seriesの入力制限とrate limitを設計する
- CORSは実際のfrontend originだけを許可する

## 金融データ上の制約

現在の実装は、価格・経済系列の定義や品質を十分に管理していません。

- yfinanceの`Close`が調整済み価格かを契約化していない
- 配当、分割、通貨、timezoneを結果へ保存していない
- FRED series ID、単位、季節調整、改訂状態を結果へ保存していない
- LLM生成文に引用・根拠chunk・棄却規則がない
- 出力は投資助言、売買推奨、将来予測ではない

## 再開する場合

1. 現行OpenAI Responses API等へ移行するか、LLM機能を削除する
2. backendとfrontendの正準構成を決める
3. `pyproject.toml`またはlock付き依存管理へ移行する
4. credentialを環境変数・secret storeへ分離する
5. data provenance、as-of、単位、通貨をschema化する
6. unit test、API contract test、external API mockを追加する
7. deployment URLとcommit SHAを対応付ける

## 関連する監査

- README監査Issue: https://github.com/KAFKA2306/kafin3/issues/3
- 全repository README監査: https://github.com/KAFKA2306/com/issues/3

**README監査日:** 2026年8月5日
