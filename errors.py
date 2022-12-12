#!/usr/bin/env python3

import constants
from constants import ALLOWED_CHARS_ALPHA, ALLOWED_CHARS_NUM
from constants import ALLOWED_CHARS_SYMBOLS
from constants import background_color
from constants import resource_path

from PIL import Image, ImageTk

from tkinter import Toplevel, Label, Button
from tkinter import CENTER


class Error(object):
    def __init__(self, window_object, message: str):
        self.width = 400
        self.height = 150
        self.x = constants.global_x - self.width // 2
        self.y = constants.global_y - self.height - 100

        self.btn_img_file = Image.open(
            resource_path('images/ok.png'))
        self.btn_img = ImageTk.PhotoImage(self.btn_img_file)

        self.object = window_object
        self.error_window = Toplevel(self.object)
        self.error_window.geometry('{}x{}+{}+{}'.format(
            self.width,
            self.height,
            self.x,
            self.y))
        self.error_window.configure(bg=background_color)
        self.error_window.title("Error")
        self.error_window.resizable(False, False)
        self.error_window.transient(self.object)

        self.err_message = Label(
            self.error_window,
            text=message,
            bg=background_color,
            fg="white")

        self.accept_button = Button(
            self.error_window,
            highlightthickness=0,
            borderwidth=0,
            background=background_color,
            highlightcolor=background_color,
            activebackground=background_color,
            image=self.btn_img,
            command=self.error_window.destroy)

        self.err_message.place(relx=.5, rely=.4, anchor=CENTER)
        self.accept_button.image = self.btn_img
        self.accept_button.place(x=165, y=100)
        # Prevents other Tkinter windows from being used
        self.error_window.grab_set()
        self.error_window.lift()  # Puts Window on top


def sanitize(window, string_type: str, eval_string: str) -> str:
    match string_type:
        case "title":
            for c in eval_string:
                char_in_set = c not in ALLOWED_CHARS_ALPHA, ALLOWED_CHARS_NUM
                if char_in_set is True:
                    raise ForbiddenChar(window, c, "Service Name")
            return eval_string
        case "url":
            for c in eval_string:
                char_in_set = c not in ALLOWED_CHARS_ALPHA, ALLOWED_CHARS_NUM
                if char_in_set is True:
                    raise ForbiddenChar(window, c, "Service URL")
            return eval_string
        case "username":
            for c in eval_string:
                char_in_set = c not in ALLOWED_CHARS_ALPHA, ALLOWED_CHARS_NUM
                if char_in_set is True:
                    raise ForbiddenChar(window, c, "Username")
            return eval_string
        case "password":
            for c in eval_string:
                char_in_set = c not in ALLOWED_CHARS_ALPHA, ALLOWED_CHARS_NUM,
                ALLOWED_CHARS_SYMBOLS
                if char_in_set is True:
                    raise ForbiddenChar(window, c, "Password")
            return eval_string
        case "number":
            for c in eval_string:
                char_in_set = c not in ALLOWED_CHARS_NUM
                if char_in_set is True:
                    raise ForbiddenChar(window, c, "number field")
            return eval_string


class ForbiddenChar(Exception):
    def __init__(self, window, forbidden_char, string_type):
        call_error_window(
            window,
            f"{forbidden_char} character not allowed in {string_type}")


class CustomError(Exception):
    def __init__(self, window, message: str):
        self.window = window
        self.message = message
        call_error_window(window, message)


def call_error_window(window, message: str):
    Error(window, message)
