# Backend

## テスト

開発環境では uv の dev 依存関係をインストールしてから pytest を実行します。

```bash
uv sync --group dev
uv run pytest
```

`conftest.py` で最低限の環境変数をセットしているため、デフォルト設定のままテストを起動できます。
