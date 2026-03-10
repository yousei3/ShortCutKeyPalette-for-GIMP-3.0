# ShortCutKeyPalette for GIMP 3.0

**ShortCutKeyPalette** is a simple, floating action palette for GIMP 3.0. It allows you to create custom buttons that execute keyboard shortcuts via `xdotool`, helping you streamline your workflow.

## Features

* **Floating & Always on Top:** The palette stays above the GIMP workspace for quick access.
* **Window Sync:** Automatically hides/shows when you minimize or restore the GIMP main window.
* **Non-Focus Stealing:** Designed to keep GIMP focused so that shortcut macros are sent correctly via `xdotool`.
* **Simple Workflow:** Add a "NEW" button and immediately customize its label and key combination via the "Edit" dialog.
* **Linux Native:** Perfect for Linux Mint (Cinnamon) and other GTK-based environments.

## Requirements

This plugin requires **xdotool** to send keyboard commands.

```bash
sudo apt install xdotool

```

## Installation

1. Download `ShortCutKey-Palette.py`.
2. Place the file in your GIMP 3.0 plug-ins directory:
* Typically: `~/.config/GIMP/3.0/plug-ins/`


3. Make the file executable:
```bash
chmod +x ShortCutKey-Palette.py

```


4. Restart GIMP.

## How to Use

1. Go to the top menu: **Windows > Open ShortCutKeyPalette**.
2. Click **＋ Add New Button** to create a placeholder button.
3. Click **Edit** next to the new button.
4. Enter a name and click the shortcut input box. Press the desired key combination (e.g., `Ctrl+Shift+A`).
5. Click **Save**. Your button is now ready!

---

## 日本語説明

**ShortCutKeyPalette** は、GIMP 3.0 用のシンプルで便利な浮動型アクションパレットです。`xdotool` を利用して任意のキーボードショートカットをボタン一つで実行でき、作業効率を大幅に向上させます。

### 特徴

* **常に最前面に表示:** GIMPの作業画面上にフローティング配置され、いつでも即座にアクセスできます。
* **ウィンドウ最小化への追従:** GIMP本体を最小化または復元すると、パレットも自動的に連動して隠れたり表示されたりします。
* **フォーカスを奪わない設計:** ボタンを押してもGIMP側のフォーカスが維持されるため、ショートカットマクロが確実に送信されます。
* **シンプルなワークフロー:** 「＋ Add New Button」でボタンを作成し、「Edit」ダイアログからラベルとキーを即座に設定できます。
* **Linux環境への最適化:** Linux Mint (Cinnamon) を含む、GTKベースのデスクトップ環境で快適に動作します。

### 必要条件

キーボードコマンドを送信するために **xdotool** が必要です。

```bash
sudo apt install xdotool

```

### 導入方法

1. `ShortCutKey-Palette.py` をダウンロードします。
2. ファイルをGIMP 3.0のプラグインディレクトリに配置します。
* 標準的なパス: `~/.config/GIMP/3.0/plug-ins/`


3. ファイルに実行権限を付与します:
```bash
chmod +x ShortCutKey-Palette.py

```


4. GIMPを再起動します。

### 使い方

1. 上部メニューの **「ウィンドウ (Windows)」 > 「Open ShortCutKeyPalette」** から起動します。
2. **「＋ Add New Button」** をクリックして、新しいボタン（プレースホルダー）を作成します。
3. 作成されたボタンの横にある **「Edit」** ボタンをクリックします。
4. ボタン名を入力し、ショートカット入力欄をクリックしてから、登録したいキー（例: `Ctrl+Shift+A`）を実際に押します。
5. **「Save」** を押せば設定完了です。

---

## License

This project is licensed under the **GPL-3.0 License**.

---
