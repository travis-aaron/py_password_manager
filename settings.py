#!/usr/bin/env python3

import constants
from constants import active_color, background_color, dark_color
from constants import DEFAULT_SETTINGS
from constants import resource_path

from db import return_settings, write_settings

from errors import sanitize, CustomError

from PIL import Image, ImageTk

from tkinter import Toplevel, Label, Button, Entry, Radiobutton, IntVar
from tkinter import ttk


class Settings:
    def __init__(self, master=None):
        self.width = 350
        self.height = 200
        self.x = constants.global_x - self.width // 2
        self.y = constants.global_y - self.height // 2

        self.settings_window = Toplevel(master)
        self.settings_window.transient(master)
        self.settings_window.geometry('{}x{}+{}+{}'.format(
            self.width,
            self.height,
            self.x,
            self.y))
        self.settings_window.configure(bg=background_color)
        self.settings_window.title("Password Manager - Settings")
        self.settings_window.resizable(False, False)
        self.settings_window.grab_set()

        self.ambiguous_var = IntVar(
            self.settings_window,
            0,
            "ambiguous_enable")

        self.cancel_img = ImageTk.PhotoImage(
            Image.open(resource_path("images/cancel.png")))
        self.apply_img = ImageTk.PhotoImage(
            Image.open(resource_path("images/apply.png")))
        self.defaults_img = ImageTk.PhotoImage(
            Image.open(resource_path("images/defaults.png")))

        style = ttk.Style()
        style.configure('settings.TLabel',
                        font=('Helvetica', 9),
                        background=background_color,
                        foreground="white")

        self.passwd_generate_hdr = Label(
            self.settings_window,
            text="Password Generation",
            font=('Helvetica', 18),
            bg=background_color,
            fg=active_color)

        self.passwd_generate_bdy = ttk.Label(
            self.settings_window,
            text="Parameters to use in password generation:",
            style="settings.TLabel")

        self.passwd_len_label = ttk.Label(
            self.settings_window,
            text="Password Length:",
            style="settings.TLabel")

        self.passwd_len_entry = Entry(
            self.settings_window,
            width=4,
            bg=background_color,
            fg="white",
            highlightcolor=active_color,
            insertbackground=active_color,
            highlightbackground=active_color)

        self.passwd_symbol_label = ttk.Label(
            self.settings_window,
            text="Number of symbols to use:",
            style="settings.TLabel")

        self.passwd_symbol_entry = Entry(
            self.settings_window,
            width=4,
            bg=background_color,
            fg="white",
            highlightcolor=active_color,
            insertbackground=active_color,
            highlightbackground=active_color)

        self.ambiguous_label = ttk.Label(
            self.settings_window,
            text="Avoid ambiguous characters (1,I,l,|):",
            style="settings.TLabel")

        self.ambiguous_enable = Radiobutton(
            self.settings_window,
            value=1,
            variable=self.ambiguous_var,
            text="Enable",
            font=('Helvetica', 9),
            bg=background_color,
            fg="white",
            borderwidth=0,
            highlightthickness=0,
            activeforeground=active_color,
            activebackground=background_color,
            selectcolor=dark_color)

        self.ambiguous_disable = Radiobutton(
            self.settings_window,
            value=0,
            variable=self.ambiguous_var,
            text="Disable",
            font=('Helvetica', 9),
            bg=background_color,
            fg="white",
            borderwidth=0,
            highlightthickness=0,
            activeforeground=active_color,
            activebackground=background_color,
            selectcolor=dark_color)

        self.settings_apply = Button(
            self.settings_window,
            image=self.apply_img,
            command=self.settings_check,
            bg=background_color,
            activebackground=background_color,
            borderwidth=0,
            highlightthickness=0)

        self.settings_cancel = Button(
            self.settings_window,
            image=self.cancel_img,
            command=self.close_window,
            bg=background_color,
            activebackground=background_color,
            borderwidth=0,
            highlightthickness=0)

        self.settings_default = Button(
            self.settings_window,
            command=self.restore_defaults,
            image=self.defaults_img,
            bg=background_color,
            borderwidth=0,
            activebackground=background_color,
            highlightthickness=0)

        # TODO: single click label for quick copy ?

        self.passwd_generate_hdr.place(x=15, y=10)
        self.passwd_generate_bdy.place(x=15, y=40)
        self.passwd_len_label.place(x=15, y=65)
        self.passwd_len_entry.place(x=120, y=60)
        self.passwd_symbol_label.place(x=15, y=90)
        self.passwd_symbol_entry.place(x=165, y=85)
        self.ambiguous_label.place(x=15, y=115)
        self.ambiguous_enable.place(x=15, y=135)
        self.ambiguous_disable.place(x=80, y=135)
        self.settings_apply.place(x=15, y=160)
        self.settings_cancel.place(x=95, y=160)
        self.settings_default.place(x=175, y=160)

        self.settings = self.load_settings()

        if self.settings != "uninitialized":
            self.passwd_symbol_entry.delete(0, "end")
            self.passwd_symbol_entry.insert(0,
                                            self.settings['Number of Symbols'][0])
            self.passwd_len_entry.delete(0, "end")
            self.passwd_len_entry.insert(0, self.settings["Password Length"][0])
            self.ambiguous_var.set(self.settings["Ambiguous Symbols"])
        else:
            self.restore_defaults()

    def restore_defaults(self):
        self.ambiguous_var.set(DEFAULT_SETTINGS[0])
        self.passwd_len_entry.delete(0, "end")
        self.passwd_len_entry.insert(0, DEFAULT_SETTINGS[1])
        self.passwd_symbol_entry.delete(0, "end")
        self.passwd_symbol_entry.insert(0, DEFAULT_SETTINGS[2])

    def load_settings(self, settings=None):
        settings_db = return_settings()
        return settings_db

    def settings_check(self):
        pass_length = sanitize(
            self.settings_window,
            "number",
            self.passwd_len_entry.get())
        if int(pass_length) > 15:
            raise CustomError(
                self.settings_window,
                "Max password length is 15")
        symbol_count = sanitize(
            self.settings_window,
            "number",
            self.passwd_symbol_entry.get())
        if pass_length and symbol_count:
            if int(symbol_count) > int(pass_length):
                raise CustomError(
                    self.settings_window,
                    "Number of symbols cannot exceed password length.")
            else:
                ambiguous_char = self.ambiguous_var.get()
                write_settings(symbol_count, pass_length, ambiguous_char)

            self.settings_window.destroy()
        else:
            raise CustomError(
                self.settings_window,
                "Please fill in all fields.")

    def close_window(self):
        self.settings_window.destroy()
