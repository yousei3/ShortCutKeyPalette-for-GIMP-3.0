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
        procedure.add_menu_path('<Image>/Windows/') # ウィンドウメニューへ配置
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

        # --- メインパレットウィンドウの設定 ---
        self.window = Gtk.Window(title="GIMP Palette")
        self.window.set_default_size(240, 400)
        self.window.set_position(Gtk.WindowPosition.MOUSE)
        self.window.set_keep_above(True)
        self.window.set_accept_focus(False)
        self.window.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.window.connect("destroy", Gtk.main_quit)

        # GIMP本体と最小化を連動させる
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

        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        main_vbox.pack_start(sep, False, False, 5)

        # 直接追加するボタン（サブメニューなし）
        btn_add = Gtk.Button(label="＋ Add New Button")
        btn_add.connect("clicked", self.add_new_action)
        main_vbox.pack_start(btn_add, False, False, 0)

        btn_close = Gtk.Button(label="Close")
        btn_close.connect("clicked", lambda w: self.window.destroy())
        main_vbox.pack_start(btn_close, False, False, 0)

        self.window.show_all()
        Gtk.main()
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

    def refresh_buttons(self):
        for child in self.buttons_vbox.get_children():
            self.buttons_vbox.remove(child)

        for action in self.actions:
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            
            btn_del = Gtk.Button(label="🗑️")
            btn_del.connect("clicked", lambda w, a=action: self.remove_action(a))
            hbox.pack_start(btn_del, False, False, 0)

            btn_exec = Gtk.Button(label=action.get("label", "Unknown"))
            btn_exec.connect("clicked", lambda w, a=action: self.execute_action(a))
            hbox.pack_start(btn_exec, True, True, 0)
            
            btn_edit = Gtk.Button(label="Edit")
            btn_edit.connect("clicked", lambda w, a=action: self.edit_action(a))
            hbox.pack_start(btn_edit, False, False, 0)

            self.buttons_vbox.pack_start(hbox, False, False, 0)
        self.buttons_vbox.show_all()

    def add_new_action(self, widget):
        # ボタンを押した瞬間に「NEW」を追加して即座に反映
        self.actions.append({"label": "NEW", "keys": "", "type": "key"})
        self.save_config(self.actions)
        self.refresh_buttons()

    def remove_action(self, action):
        if action in self.actions:
            self.actions.remove(action)
            self.save_config(self.actions)
            self.refresh_buttons()

    def execute_action(self, action):
        keys = action.get("keys")
        if not keys: return
        try:
            subprocess.Popen(['xdotool', 'key', keys])
        except Exception as e:
            print(f"Key Macro Error: {e}")

    def edit_action(self, action):
        # 編集ダイアログもメインパレットを手前に保持する設定
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
        
        entry_keys = Gtk.Entry()
        entry_keys.set_text(action.get("keys", ""))
        entry_keys.set_placeholder_text("Click here & press keys")
        entry_keys.connect("key-press-event", self.on_shortcut_key_press)
        box.pack_start(entry_keys, True, True, 0)

        dialog.show_all()
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            new_label = entry_label.get_text().strip()
            if new_label: action["label"] = new_label
            action["keys"] = entry_keys.get_text().strip()
            action["type"] = "key"
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