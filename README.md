# ペンプロッター Gコード送信ツール

GRBL-Servoベースのペンプロッターにマークシート塗りつぶし用のGコードを送信するPythonツールです。

## 機能

- GRBL-Servoとのシリアル通信
- マークシートの指定位置への自動マーク塗りつぶし
- 行・列番号に基づく座標オフセット計算
- ホーミング、リセット、ステータス確認機能

## 必要な環境

- Python 3.x
- pyserial ライブラリ
- GRBL-Servo対応のArduino/ペンプロッター

## インストール

```bash
pip install pyserial
```

## 使用方法

### 基本的な使用

1. シリアルポートを確認・設定
2. `main.py`を実行

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