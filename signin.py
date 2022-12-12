#!/usr/bin/env python3

import constants
from constants import dark_color, background_color, active_color
from constants import resource_path

from db import sign_in, log_out

from entries import Table

from PIL import Image, ImageTk

from register import Register

from tkinter import Toplevel, Canvas, Label, Entry, Button
from tkinter import ttk


class SignIn(object):
    def __init__(self, x, y, master, logout=None):
        self.sign_in_win = Toplevel(master)
        self.x = x
        self.y = y
        constants.global_x = self.x
        constants.global_y = self.y

        self.sign_in_win.transient(master)
        self.sign_in_win.geometry("400x260")
        self.sign_in_win.title("Sign In")
        self.sign_in_win.configure(bg=dark_color)
        # Disable the X in the top right corner
        self.sign_in_win.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.sign_in_win.resizable(False, False)
        self.sign_in_win.grab_set()
        self.sign_in_win.attributes("-alpha", "1")

        # Login page entry boxes using Canvas objects and images
        self.p_image = ImageTk.PhotoImage(
            Image.open(resource_path("images/entry4.png")))

        self.profile_entry_canvas = Canvas(
            self.sign_in_win,
            width=150,
            height=50,
            bd=0,
            borderwidth=0,
            highlightthickness=0,
            bg=background_color)

        self.profile_entry_canvas.pack(fill="both", expand=True)
        self.profile_entry_canvas.create_image(196, 85, image=self.p_image)
        self.profile_entry_canvas.create_image(196, 145, image=self.p_image)

        self.button_image = ImageTk.PhotoImage(
            Image.open(resource_path("images/signin.png")))

        style = ttk.Style()
        style.configure('signInLabel.TLabel',
                        background=background_color,
                        foreground=active_color,
                        font=('Helvetica', 9),
                        borderwidth=0,
                        highlightthickness=0)

        self.sign_in_continue = Label(
            self.sign_in_win,
            text="Sign in to continue",
            font=('Helvetica', 18),
            fg="white",
            bg=background_color)

        self.sign_in_name_lbl = ttk.Label(
            self.sign_in_win,
            text="Profile name",
            style="signInLabel.TLabel")

        self.sign_in_pass_lbl = ttk.Label(
            self.sign_in_win,
            text="Password",
            style="signInLabel.TLabel")

        self.sign_in_user_entry = Entry(
            self.sign_in_win,
            bg=background_color,
            fg=active_color,
            highlightcolor=active_color,
            insertbackground=active_color,
            borderwidth=0,
            highlightthickness=0)

        self.sign_in_pass_entry = Entry(
            self.sign_in_win,
            show="*",
            bg=background_color,
            fg=active_color,
            highlightcolor=active_color,
            insertbackground=active_color,
            borderwidth=0,
            highlightthickness=0)

        self.sign_in_btn = Button(
            self.sign_in_win,
            command=self.sign_in_user,
            image=self.button_image,
            background=background_color,
            borderwidth=0,
            highlightthickness=0,
            activebackground=background_color)

        self.register_label = Label(
            self.sign_in_win,
            font=('Helvetica', 9),
            text="Need a new profile?",
            bg=background_color,
            fg="white")

        self.register_hyperlink = ttk.Label(
            self.sign_in_win,
            text="Click here",
            cursor="hand2",
            style="signInLabel.TLabel")

        self.master_window = master
        self.table = None

        self.sign_in_continue.place(x=95, y=20)
        self.sign_in_name_lbl.place(x=130, y=67, height=12)
        self.sign_in_user_entry.place(x=130, y=77, width=140, height=27)
        self.sign_in_pass_lbl.place(x=130, y=127, height=12)
        self.sign_in_pass_entry.place(x=130, y=137, width=140, height=27)
        self.sign_in_btn.place(x=155, y=185)
        self.register_label.place(x=110, y=220)
        self.register_hyperlink.place(x=224, y=222)
        self.register_hyperlink.bind(
            "<Button-1>",
            lambda e: self.clicked_register(self.sign_in_win))
        if constants.table and logout:
            self.logout()

    def sign_in_user(self):
        user_entry = self.sign_in_user_entry.get()
        pass_entry = self.sign_in_pass_entry.get()
        sign_in(user_entry, pass_entry, self.sign_in_win)
        status = sign_in(user_entry, pass_entry, self.sign_in_win)

        if status == "create_table":
            self.table = Table()
            constants.table = self.table

    # Necessary to prevent sign in window from being closed prematurely
    def disable_event(self):
        pass

    def logout(self):
        constants.table.delete_all_widgets()
        log_out()

    def clicked_register(self, window_object: object):
        Register(window_object)
