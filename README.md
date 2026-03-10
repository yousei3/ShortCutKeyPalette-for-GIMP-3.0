# ShortCutKeyPalette for GIMP 3.0

**ShortCutKeyPalette** is a simple, floating action palette for GIMP 3.0. It allows you to create custom buttons that execute keyboard shortcuts via `xdotool`, helping you streamline your workflow.

## Features

- **Floating & Always on Top:** The palette stays above the GIMP workspace for quick access.
- **Window Sync:** Automatically hides/shows when you minimize or restore the GIMP main window.
- **Non-Focus Stealing:** Designed to keep GIMP focused so that shortcut macros are sent correctly.
- **Simple Workflow:** Add a "NEW" button and immediately customize its label and key combination via the "Edit" dialog.
- **Linux Native:** Perfect for Linux Mint (Cinnamon) and other GTK-based environments.


## Requirements

This plugin requires **xdotool** to send keyboard commands.

Bash

```
sudo apt install xdotool
```

## Installation

1. Download `ShortCutKey-Palette.py`.
2. Place the file in your GIMP 3.0 plug-ins directory:
- Typically: `~/.config/GIMP/3.0/plug-ins/`
3. Make the file executable:

Bash

```
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
#### Japanese
## 日本語説明

GIMP 3.0 用の、シンプルでカスタマイズ可能なショートカットパレットです。

### 特徴

- **常に最前面:** 作業の邪魔にならないサイズで、常に手前に表示されます。
- **最小化連動:** GIMP本体を最小化するとパレットも一緒に隠れます。
- **簡単登録:** 「＋ Add New Button」でボタンを作り、「Edit」から好きな名前とキー（xdotool形式）を割り当てるだけ。
- **フォーカスを奪わない:** ボタンを押してもGIMP側のフォーカスが維持されるため、確実にショートカットが実行されます。


### 導入方法

1. `ShortCutKey-Palette.py` を `~/.config/GIMP/3.0/plug-ins/` に配置します。
2. ファイルに実行権限を与えます。
3. GIMPのメニュー **「ウィンドウ (Windows)」 > 「Open ShortCutKeyPalette」** から起動してください。


---

## License

This project is licensed under the GPL-3.0 License

---
