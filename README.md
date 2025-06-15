# ペンプロッター Gコード送信ツール

GRBL-Servoベースのペンプロッターにマークシート塗りつぶし用のGコードを送信するPythonツールです。

## 機能

- GRBL-Servoとのシリアル通信
- マークシートの指定位置への自動マーク塗りつぶし
- 行・列番号に基づく座標オフセット計算
- ホーミング、リセット、ステータス確認機能
- FastAPIベースのWebAPI提供

## 必要な環境

- Python 3.x
- pyserial ライブラリ
- FastAPI
- uvicorn
- GRBL-Servo対応のArduino/ペンプロッター

## インストール

```bash
# uvパッケージマネージャーを使用
uv sync

# または従来のpipを使用
pip install pyserial fastapi uvicorn[standard]
```

## 使用方法

### WebAPI サーバーの起動

```bash
python main.py
```

サーバーは `http://localhost:8080` で起動します。

### API エンドポイント

#### 1. ペンプロッタでマーク描画
```
GET /mark?row={行番号}&column={列番号}
```

**パラメータ:**
- `row` (int): 行番号（0から開始）
- `column` (int): 列番号（0から開始）

**使用例:**
```bash
curl "http://localhost:8080/mark?row=4&column=4"
```

**レスポンス例:**
```json
{
  "message": "行 4, 列 4 にマークしました"
}
```

#### 2. プロッタステータス確認
```
GET /status
```

**使用例:**
```bash
curl "http://localhost:8080/status"
```

**レスポンス例:**
```json
{
  "status": "<Idle|MPos:0.000,0.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>"
}
```

#### 3. API情報
```
GET /
```

**レスポンス例:**
```json
{
  "message": "Pen Plotter API"
}
```

### 基本的なスタンドアロン使用

シリアルポートを設定して直接実行する場合：

```python
# ポート設定例
PORT = '/dev/cu.usbmodem2201'  # Mac/Linux
# PORT = 'COM3'  # Windows
```

### マーク位置の指定

```python
sender.mark_position(row, column)
```

- `row`: 行番号（0から開始）
- `column`: 列番号（0から開始）

### 座標オフセット

- **X方向（行）**: 1行につき0.26mmオフセット
- **Y方向（列）**: 1列につき0.5mmオフセット

## 主要なメソッド

- `connect()`: デバイスとの接続
- `send_command(command)`: 単一Gコード送信
- `mark_position(row, column)`: 指定位置マーク塗りつぶし
- `home()`: ホーミング実行
- `get_status()`: ステータス確認
- `reset()`: ソフトリセット
- `disconnect()`: 接続終了

## Gコードファイル送信

```python
sender.send_gcode_file("path/to/file.gcode")
```

## 注意事項

- 使用前にシリアルポート名を正しく設定してください
- ホーミング実行後、座標系を初期化してから使用してください
- エラー発生時は適切に処理してください