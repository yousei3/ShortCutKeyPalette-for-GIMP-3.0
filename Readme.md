# ShortCutKey Palette for GIMP 3.0

A Python-based plugin for GIMP 3.0 that creates a floating palette of customizable on-screen buttons. 
Each button can be configured to trigger a specific keyboard shortcut, making it ideal for tablet users or anyone who wants quick access to their favorite tools and actions.

## Cross-Platform Support & Requirements

This plugin now supports Windows, Linux (X11), and has experimental support for Linux (Wayland).

- Windows: Works out of the box! No additional software is required (it uses native ctypes).
- Linux (X11): Requires "xdotool" to simulate keyboard strokes.
  For Debian/Ubuntu/Mint users: sudo apt install xdotool
- Linux (Wayland): Experimental support. Due to Wayland's strict security model regarding simulated inputs, you must install one of the following tools:
  1. python3-dogtail (UI testing framework - Recommended)
  2. ydotool
  3. wtype

## Installation
1. Extract the downloaded ZIP file.
2. You will get a folder named "shortcutkey-palette".
3. Place this ENTIRE FOLDER into your GIMP 3.0 plug-ins directory.
   Typically located at:
   - Windows: C:\Users\[Your Username]\AppData\Roaming\GIMP\3.0\plug-ins\
   - Linux: ~/.config/GIMP/3.0/plug-ins/
4. Ensure the python script "shortcutkey-palette.py" inside the folder has executable permissions (Linux only).
5. Restart GIMP.

## How to Use
1. Launch the plugin from the GIMP menu: Image > Windows > Open ShortCutKeyPalette.
2. A sample palette will open (loaded from the included palette_config.json).
3. Click the gear icon (Edit) on any button to change its label, shortcut key, or background color.
   - You can choose from several preset dark colors to keep the white text readable.
4. Click "＋ Add" at the bottom to create a new button.
5. Click "↕ Reorder" to enter sorting mode. Use the Up/Down arrows to organize your palette, then click "✓ Done Reorder" to finish.
6. Click the trash can icon to delete a button.

## Files Included
- shortcutkey-palette.py : The main Python plugin script.
- palette_config.json : A sample configuration file with default buttons.
- readme.md : This instruction file.