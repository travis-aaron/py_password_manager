#!/usr/bin/env python3

from constants import background_color, active_color, warning_color
from constants import resource_path

from db import initialize

from tkinter import Toplevel, Canvas, Label, Entry, Button
from tkinter import NW

from PIL import Image, ImageTk


class Register(object):
    def __init__(self, window_object):
        self.register = Toplevel(window_object)
        self.register.transient(window_object)
        self.register.geometry("300x300")
        self.register.title("Register")
        self.register.configure(bg=background_color)
        self.register.wait_visibility()
        self.register.grab_set_global()

        self.warning_text = """Your account will be unchangeable
        after submittal. Please write down your
        details, and keep them somewhere safe."""

        self.frame_image = ImageTk.PhotoImage(
            Image.open(resource_path('images/entry4.png')))
        self.register_btn = ImageTk.PhotoImage(
            Image.open(resource_path('images/register.png')))

        self.entry_canvas = Canvas(
            self.register,
            width=150,
            height=50,
            bd=0,
            borderwidth=0,
            highlightthickness=0,
            bg=background_color)

        self.pass_warning = Label(
            self.register,
            text=self.warning_text,
            anchor=NW,
            width=50,
            fg=warning_color,
            font=("Helvetica", 9),
            bg=background_color)

        self.username_lbl = Label(
            self.register,
            text="Username",
            font=("Helvetica", 9),
            bg=background_color,
            fg=active_color)

        self.username_entry = Entry(
            self.register,
            width=15,
            bg=background_color,
            fg=active_color,
            highlightcolor=active_color,
            insertbackground=active_color,
            borderwidth=0,
            highlightthickness=0)

        self.passwd_lbl = Label(
            self.register,
            text="Password",
            font=("Helvetica", 9),
            bg=background_color,
            fg=active_color)

        self.passwd_entry = Entry(
            self.register,
            width=15,
            bg=background_color,
            fg=active_color,
            show="*",
            highlightcolor=active_color,
            insertbackground=active_color,
            borderwidth=0,
            highlightthickness=0)

        self.confirm_passwd_lbl = Label(
            self.register,
            text="Confirm Password",
            font=("Helvetica", 9),
            bg=background_color,
            fg=active_color)

        self.confirm_passwd_entry = Entry(
            self.register,
            width=15,
            bg=background_color,
            fg=active_color,
            highlightcolor=active_color,
            insertbackground=active_color,
            show="*",
            borderwidth=0,
            highlightthickness=0)

        self.apply_btn = Button(
            self.register,
            image=self.register_btn,
            command=lambda: initialize(
                self.register,
                self.username_entry.get(),
                self.passwd_entry.get(),
                self.confirm_passwd_entry.get()),
            bg=background_color,
            borderwidth=0,
            highlightthickness=0,
            activebackground=background_color)

        self.pass_warning.place(x=20, y=10)

        self.entry_canvas.pack(fill="both", expand=True)

        self.entry_canvas.create_image(150, 90, image=self.frame_image)
        self.entry_canvas.create_image(150, 150, image=self.frame_image)
        self.entry_canvas.create_image(150, 210, image=self.frame_image)

        self.username_lbl.place(x=85, y=72)
        self.username_entry.place(x=85, y=85)
        self.passwd_lbl.place(x=85, y=132)
        self.passwd_entry.place(x=85, y=145)
        self.confirm_passwd_lbl.place(x=85, y=192)
        self.confirm_passwd_entry.place(x=85, y=205)
        self.apply_btn.place(x=110, y=245)
        self.apply_btn.configure(image=self.register_btn)
