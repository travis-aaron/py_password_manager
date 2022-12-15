#!/usr/bin/env python3

import constants
from constants import active_color, background_color
from constants import resource_path

from db import add_password, update_entry, return_entry

from errors import sanitize, CustomError

from password_gen import password_gen

from PIL import Image, ImageTk

from tkinter import Toplevel, Canvas, Entry, Button
from tkinter import ttk

from validator_collection import checkers


class AddNewPassword:
    def __init__(self, master=None, row_number=None, service=None):
        self.width = 300
        self.height = 330
        self.x = constants.global_x - self.width // 2
        self.y = constants.global_y - self.height // 2

        self.password_window = Toplevel(master)
        self.password_window.transient(master)
        self.password_window.geometry('{}x{}+{}+{}'.format(
                                                    self.width, self.height,
                                                    self.x, self.y))
        self.password_window.title("Password Manager - Edit")
        self.password_window.configure(bg=background_color)
        self.password_window.resizable(False, False)
        self.password_window.grab_set()

        self.cancel_img = ImageTk.PhotoImage(
            Image.open(resource_path("images/cancel.png")))
        self.apply_img = ImageTk.PhotoImage(
            Image.open(resource_path("images/apply.png")))
        self.generate_img = ImageTk.PhotoImage(
            Image.open(resource_path("images/generate.png")))

        self.frame_image = ImageTk.PhotoImage(
            Image.open(resource_path('images/entry5.png')))

        self.entry_canvas = Canvas(
            self.password_window,
            width=200,
            height=300,
            bd=0,
            borderwidth=0,
            highlightthickness=0,
            bg=background_color)

        self.entry_canvas.create_image(100, 60, image=self.frame_image)
        self.entry_canvas.create_image(100, 120, image=self.frame_image)
        self.entry_canvas.create_image(100, 180, image=self.frame_image)
        self.entry_canvas.create_image(100, 240, image=self.frame_image)

        style = ttk.Style()
        style.configure('addPassLabel.TLabel',
                        background=background_color,
                        foreground=active_color,
                        font=('Helvetica', 9))

        self.service_name_lbl = ttk.Label(
            self.password_window,
            text="Account",
            style="addPassLabel.TLabel")

        self.service_name_entry = Entry(
            self.password_window, width=20,
            bg=background_color,
            fg=active_color,
            highlightcolor=active_color,
            insertbackground=active_color,
            borderwidth=0,
            highlightthickness=0)

        self.service_url_lbl = ttk.Label(
            self.password_window,
            text="URL",
            style="addPassLabel.TLabel")

        self.service_url_entry = Entry(
            self.password_window,
            width=20,
            bg=background_color,
            fg=active_color,
            highlightcolor=active_color,
            insertbackground=active_color,
            borderwidth=0,
            highlightthickness=0)

        self.username_lbl = ttk.Label(
            self.password_window,
            text="Username",
            style="addPassLabel.TLabel")

        self.username_entry = Entry(
            self.password_window,
            width=20,
            bg=background_color,
            fg=active_color,
            highlightcolor=active_color,
            insertbackground=active_color,
            borderwidth=0,
            highlightthickness=0)

        self.passwd_lbl = ttk.Label(
            self.password_window,
            text="Password",
            style="addPassLabel.TLabel")

        self.passwd_entry = Entry(
            self.password_window,
            width=15,
            bg=background_color,
            fg=active_color,
            highlightcolor=active_color,
            insertbackground=active_color,
            borderwidth=0,
            highlightthickness=0)

        self.generate_passwd = Button(
            self.password_window,
            image=self.generate_img,
            bg=background_color,
            activebackground=background_color,
            borderwidth=0,
            highlightthickness=0,
            command=self.generate)

        self.apply_button = Button(
            self.password_window,
            image=self.apply_img,
            bg=background_color,
            activebackground=background_color,
            borderwidth=0,
            highlightthickness=0,
            command=self.add_entry)

        self.cancel_button = Button(
            self.password_window,
            image=self.cancel_img,
            bg=background_color,
            activebackground=background_color,
            borderwidth=0,
            highlightthickness=0,
            command=self.password_window.destroy)

        self.table = constants.table
        print(self.table)

        self.entry_canvas.pack()
        self.service_name_lbl.place(x=60, y=40)
        self.service_name_entry.place(x=60, y=55)
        self.service_url_lbl.place(x=60, y=100)
        self.service_url_entry.place(x=60, y=115)
        self.username_lbl.place(x=60, y=160)
        self.username_entry.place(x=60, y=175)
        self.passwd_lbl.place(x=60, y=220)
        self.passwd_entry.place(x=60, y=235)
        self.apply_button.place(x=30, y=275)
        self.apply_button.configure(image=self.apply_img)
        self.cancel_button.place(x=115, y=275)
        self.cancel_button.configure(image=self.cancel_img)
        self.generate_passwd.place(x=195, y=275)
        if row_number and service:
            self.edit_entry(row_number, service)

    def generate(self):
        self.passwd_entry.delete(1, "end")
        generated_pass = password_gen()
        self.passwd_entry.insert(0, generated_pass)

    def add_entry(self):
        serv_name = sanitize(
            self.password_window,
            "title",
            self.service_name_entry.get())
        serv_url = self.parse_url(self.service_url_entry.get())
        user_entry = sanitize(
            self.password_window,
            "username",
            self.username_entry.get())
        pass_entry = sanitize(
            self.password_window,
            "password",
            self.passwd_entry.get())
        if serv_url != "Invalid URL":
            add_password(
                str(serv_name),
                str(serv_url),
                str(user_entry),
                str(pass_entry))
            constants.table.refresh()
            self.password_window.destroy()
        elif not serv_name or serv_url or user_entry or pass_entry:
            raise CustomError(
                self.password_window,
                "Please fill in all fields.")
        else:
            raise CustomError(
                self.password_window,
                "Please insert a valid URL (with http://)")

    def edit_entry(self, row_number, service):
        entry = return_entry(service)
        self.service_name_entry.insert(0, entry['Service Name'])
        self.service_url_entry.insert(0, entry['URL'])
        self.username_entry.insert(0, entry['Username'])
        self.passwd_entry.insert(0, entry['Password'])

        self.apply_button.configure(
            command=lambda: self.update_entry(service))

    def update_entry(self, service):
        entry = {}
        entry['Service Name'] = self.service_name_entry.get()
        serv_url = self.parse_url(self.service_url_entry.get())
        if serv_url != "Invalid URL":
            entry['URL'] = serv_url
        else:
            raise CustomError(
                self.password_window,
                "Please insert a valid URL (with http://)")
        entry['Username'] = self.username_entry.get()
        entry['Password'] = self.passwd_entry.get()
        try:
            update_entry(entry, service)
        except Exception as e:
            print(e)
        constants.table.refresh()
        self.password_window.destroy()

    def parse_url(self, url):
        if checkers.is_url(url):
            return url
        return "Invalid URL"
