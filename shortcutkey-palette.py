#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gimp, GimpUi, Gtk, Gdk, GObject, GLib
import sys
import os
import json
import subprocess
import platform
import time

# Windows環境の場合はctypesを読み込む
if platform.system() == "Windows":
    import ctypes

# 設定ファイルの保存場所
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "palette_config.json")

class PaletteLauncher(Gimp.PlugIn):
    def do_query_procedures(self):
        return ["python-palette-launcher-v12"]

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run, None)
        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
        procedure.set_menu_label("Open ShortCutKeyPalette")
        procedure.add_menu_path('<Image>/Windows/')
        return procedure

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print("Config load error:", e)
        return []

    def save_config(self, actions):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(actions, f, indent=4)
        except Exception as e:
            print("Failed to save config:", e)

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        self.actions = self.load_config()
        GimpUi.init("python-palette-launcher")

        self.window = Gtk.Window(title="Shortcut Palette")
        self.window.set_default_size(300, 600)
        self.window.set_position(Gtk.WindowPosition.MOUSE)
        self.window.set_keep_above(True)
        self.window.set_accept_focus(False)
        self.window.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.window.connect("destroy", Gtk.main_quit)

        try:
            GimpUi.window_set_transient(self.window)
        except Exception as e:
            print(f"Transient Error: {e}")

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        main_vbox.set_border_width(8)
        self.window.add(main_vbox)

        scroll_palette = Gtk.ScrolledWindow()
        scroll_palette.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_vbox.pack_start(scroll_palette, True, True, 0)

        self.buttons_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        scroll_palette.add(self.buttons_vbox)

        self.refresh_buttons()

        self.is_reorder_mode = False

        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_vbox.pack_start(sep, False, False, 5)

        hbox_bottom = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        main_vbox.pack_start(hbox_bottom, False, False, 0)

        self.btn_add = Gtk.Button(label="＋ Add")
        self.btn_add.connect("clicked", self.add_new_action)
        hbox_bottom.pack_start(self.btn_add, True, True, 0)

        self.btn_reorder_toggle = Gtk.Button(label="↕ Reorder")
        self.btn_reorder_toggle.connect("clicked", self.toggle_reorder_mode)
        hbox_bottom.pack_start(self.btn_reorder_toggle, True, True, 0)

        self.window.show_all()
        Gtk.main()
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

    def toggle_reorder_mode(self, widget):
        self.is_reorder_mode = not getattr(self, 'is_reorder_mode', False)
        
        if self.is_reorder_mode:
            self.btn_reorder_toggle.set_label("✓ Done Reorder")
            self.btn_add.hide()
        else:
            self.btn_reorder_toggle.set_label("↕ Reorder")
            self.btn_add.show()
            
        self.refresh_buttons()

    def apply_button_color(self, button, color_str):
        if not color_str:
            return
            
        btn_id = f"custom-btn-{id(button)}"
        button.set_name(btn_id)

        css = f"""
        #{btn_id} {{
            background-image: none;
            background-color: {color_str};
            color: #ffffff;
        }}
        #{btn_id} label {{
            color: #ffffff;
        }}
        """
        
        provider = Gtk.CssProvider()
        try:
            provider.load_from_data(css.encode('utf-8'))
            button.get_style_context().add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        except Exception as e:
            print(f"CSS Error: {e}")

    def refresh_buttons(self):
        for child in self.buttons_vbox.get_children():
            self.buttons_vbox.remove(child)

        is_reorder = getattr(self, 'is_reorder_mode', False)

        for action in self.actions:
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
            
            if is_reorder:
                btn_up = Gtk.Button(label="▲")
                btn_up.connect("clicked", lambda w, a=action: self.move_up(a))
                if self.actions.index(action) == 0:
                    btn_up.set_sensitive(False)
                hbox.pack_start(btn_up, False, False, 0)

                btn_label = Gtk.Button(label=action.get("label", "Unknown"))
                btn_label.set_sensitive(False)
                self.apply_button_color(btn_label, action.get("color"))
                hbox.pack_start(btn_label, True, True, 0)

                btn_down = Gtk.Button(label="▼")
                btn_down.connect("clicked", lambda w, a=action: self.move_down(a))
                if self.actions.index(action) == len(self.actions) - 1:
                    btn_down.set_sensitive(False)
                hbox.pack_start(btn_down, False, False, 0)

            else:
                btn_del = Gtk.Button(label="🗑️")
                btn_del.connect("clicked", lambda w, a=action: self.remove_action(a))
                hbox.pack_start(btn_del, False, False, 0)

                btn_exec = Gtk.Button(label=action.get("label", "Unknown"))
                btn_exec.connect("clicked", lambda w, a=action: self.execute_action(a))
                self.apply_button_color(btn_exec, action.get("color"))
                hbox.pack_start(btn_exec, True, True, 0)
                
                btn_edit = Gtk.Button(label="⚙️")
                btn_edit.connect("clicked", lambda w, a=action: self.edit_action(a))
                hbox.pack_start(btn_edit, False, False, 0)

            self.buttons_vbox.pack_start(hbox, False, False, 0)
        self.buttons_vbox.show_all()

    def move_up(self, action):
        idx = self.actions.index(action)
        if idx > 0:
            self.actions[idx - 1], self.actions[idx] = self.actions[idx], self.actions[idx - 1]
            self.save_config(self.actions)
            self.refresh_buttons()

    def move_down(self, action):
        idx = self.actions.index(action)
        if idx < len(self.actions) - 1:
            self.actions[idx + 1], self.actions[idx] = self.actions[idx], self.actions[idx + 1]
            self.save_config(self.actions)
            self.refresh_buttons()

    def add_new_action(self, widget):
        self.actions.append({"label": "NEW", "keys": "", "type": "key", "color": None})
        self.save_config(self.actions)
        self.refresh_buttons()

    def remove_action(self, action):
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text="Delete Action"
        )
        action_name = action.get("label", "Unknown")
        dialog.format_secondary_text(f"Are you sure you want to delete '{action_name}'?")
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            if action in self.actions:
                self.actions.remove(action)
                self.save_config(self.actions)
                self.refresh_buttons()
        dialog.destroy()

    def execute_action(self, action):
        keys = action.get("keys")
        if not keys: return
        
        system = platform.system()
        
        if system == "Windows":
            self.send_keys_windows(keys)
        elif system == "Linux":
            # 環境変数 WAYLAND_DISPLAY が存在すればWayland環境と判定
            if os.environ.get("WAYLAND_DISPLAY"):
                self.send_keys_wayland(keys)
            else:
                self.send_keys_x11(keys)
        else:
            # その他のOS (Mac等) はとりあえずxdotoolをフォールバックとして試す
            self.send_keys_x11(keys)

    def send_keys_windows(self, keys_str):
        if platform.system() != "Windows": return
        
        VK_CODE = {
            'ctrl': 0x11, 'shift': 0x10, 'alt': 0x12, 'super': 0x5B,
            'enter': 0x0D, 'space': 0x20, 'backspace': 0x08, 'tab': 0x09,
            'escape': 0x1B, 'comma': 0xBC, 'minus': 0xBD, 'period': 0xBE,
            'slash': 0xBF, 'plus': 0xBB, 'equal': 0xBB
        }

        parts = keys_str.lower().split('+')
        vk_list = []

        for part in parts:
            if part in VK_CODE:
                vk_list.append(VK_CODE[part])
            elif len(part) == 1:
                vk_list.append(ord(part.upper()))

        for vk in vk_list:
            ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
        
        time.sleep(0.01)

        for vk in reversed(vk_list):
            ctypes.windll.user32.keybd_event(vk, 0, 2, 0)

    def send_keys_x11(self, keys_str):
        try:
            subprocess.Popen(['xdotool', 'key', keys_str])
        except Exception as e:
            print(f"X11 Key Macro Error: {e}")

    def send_keys_wayland(self, keys_str):
        # アプローチ1: フォーラムで提案された dogtail (UIテストツール) を試す
        try:
            from dogtail.rawinput import pressKey
            # dogtail向けにキー名の調整が必要な場合がありますが、まずはそのまま渡す
            pressKey(keys_str)
            return
        except ImportError:
            print("dogtail is not installed. Trying fallback tools.")
        except Exception as e:
            print(f"dogtail error: {e}")

        # アプローチ2: 汎用の ydotool を試す (xdotoolと互換性が高いため)
        try:
            subprocess.run(['ydotool', 'key', keys_str], check=True)
            return
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        # アプローチ3: wtype を試す
        try:
            # 簡易的な実装: 複雑なモディファイアのパースは省略
            subprocess.run(['wtype', keys_str])
            return
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("Wayland key injection failed. Please install python3-dogtail, ydotool, or wtype.")

    def edit_action(self, action):
        dialog = Gtk.Dialog(title="Edit Action", transient_for=self.window, flags=Gtk.DialogFlags.MODAL)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Save", Gtk.ResponseType.OK)
        
        box = dialog.get_content_area()
        box.set_spacing(10)
        box.set_border_width(10)
        
        lbl_name = Gtk.Label(label="New Button Label:")
        lbl_name.set_xalign(0)
        box.pack_start(lbl_name, False, False, 0)

        entry_label = Gtk.Entry()
        entry_label.set_text(action.get("label", ""))
        box.pack_start(entry_label, True, True, 0)
        
        lbl_keys = Gtk.Label(label="Shortcut Keys:")
        lbl_keys.set_xalign(0)
        box.pack_start(lbl_keys, False, False, 5)

        lbl_desc = Gtk.Label(label="Click the text box and press your shortcut keys.")
        lbl_desc.set_xalign(0)
        box.pack_start(lbl_desc, False, False, 0)
        
        hbox_keys = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        box.pack_start(hbox_keys, True, True, 0)

        entry_keys = Gtk.Entry()
        entry_keys.set_text(action.get("keys", ""))
        entry_keys.set_placeholder_text("Click here & press keys")
        entry_keys.connect("key-press-event", self.on_shortcut_key_press)
        hbox_keys.pack_start(entry_keys, True, True, 0)

        btn_clear = Gtk.Button(label="Clear")
        btn_clear.connect("clicked", lambda w: entry_keys.set_text(""))
        hbox_keys.pack_start(btn_clear, False, False, 0)

        lbl_color = Gtk.Label(label="Button Color:")
        lbl_color.set_xalign(0)
        box.pack_start(lbl_color, False, False, 5)

        PRESET_COLORS = ["#8b0000", "#006400", "#00008b", "#b8860b", "#800080", "#008080", "#444444"]
        
        dialog_color_state = {"color": action.get("color", None)}

        hbox_palette = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        box.pack_start(hbox_palette, False, False, 0)

        preview_chip = Gtk.Button()
        preview_chip.set_size_request(40, 24)
        preview_chip.set_sensitive(False)

        def update_preview(color_str):
            if color_str:
                css = f"#preview-chip {{ background-image: none; background-color: {color_str}; }}"
            else:
                css = f"#preview-chip {{ background-image: none; background-color: #2a2a2a; }}"
            
            provider = Gtk.CssProvider()
            provider.load_from_data(css.encode('utf-8'))
            preview_chip.set_name("preview-chip")
            preview_chip.get_style_context().add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        update_preview(dialog_color_state["color"])

        for color_code in PRESET_COLORS:
            btn_chip = Gtk.Button()
            btn_chip.set_size_request(24, 24)
            
            css = f"#chip-{color_code[1:]} {{ background-image: none; background-color: {color_code}; border-radius: 3px; }}"
            provider = Gtk.CssProvider()
            provider.load_from_data(css.encode('utf-8'))
            btn_chip.set_name(f"chip-{color_code[1:]}")
            btn_chip.get_style_context().add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            
            def on_chip_clicked(widget, c=color_code):
                dialog_color_state["color"] = c
                update_preview(c)
                
            btn_chip.connect("clicked", on_chip_clicked)
            hbox_palette.pack_start(btn_chip, False, False, 0)

        hbox_reset = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        box.pack_start(hbox_reset, False, False, 5)
        
        hbox_reset.pack_start(preview_chip, False, False, 0)
        
        btn_reset_color = Gtk.Button(label="Reset to Default")
        def on_reset_color(widget):
            dialog_color_state["color"] = None
            update_preview(None)
        btn_reset_color.connect("clicked", on_reset_color)
        hbox_reset.pack_start(btn_reset_color, False, False, 0)

        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            new_label = entry_label.get_text().strip()
            if new_label: action["label"] = new_label
            action["keys"] = entry_keys.get_text().strip()
            action["type"] = "key"
            
            if dialog_color_state["color"]:
                action["color"] = dialog_color_state["color"]
            else:
                if "color" in action:
                    del action["color"]

            self.save_config(self.actions)
            self.refresh_buttons()
        dialog.destroy()

    def on_shortcut_key_press(self, widget, event):
        keyval = event.keyval
        state = event.state
        keyname = Gdk.keyval_name(keyval)
        if not keyname: return True
        if keyname in ['Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R', 'Super_L', 'Super_R']:
            return True
        if keyname == 'BackSpace':
            widget.set_text("")
            return True

        mods = []
        if state & Gdk.ModifierType.CONTROL_MASK: mods.append("ctrl")
        if state & Gdk.ModifierType.MOD1_MASK: mods.append("alt")
        if state & Gdk.ModifierType.SHIFT_MASK: mods.append("shift")
        if state & Gdk.ModifierType.SUPER_MASK: mods.append("super")

        if len(keyname) == 1: keyname = keyname.lower()
        keys = mods + [keyname]
        widget.set_text("+".join(keys))
        return True

if __name__ == '__main__':
    Gimp.main(PaletteLauncher.__gtype__, sys.argv)