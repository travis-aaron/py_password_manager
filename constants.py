#!/usr/bin/env python3

import os

import sys

background_color = "#0b3142"
active_color = "#F0544F"
warning_color = "#D81E5B"
secondary_color = "#086303"
dark_color = "#1F221B"

ALLOWED_CHARS_ALPHA = {'a', 'b', 'c', 'd', 'e', 'f',
                       'g', 'h', 'i', 'j', 'k', 'l',
                       'm', 'n', 'o', 'p', 'q', 'r',
                       's', 't', 'u', 'v', 'w', 'x',
                       'y', 'z',
                       'A', 'B', 'C', 'D', 'E', 'F', 'G',
                       'H', 'I', 'J', 'K', 'L', 'M', 'N',
                       'O', 'P', 'Q', 'R', 'S', 'T', 'U',
                       'V', 'W', 'X', 'Y', 'Z'}

ALLOWED_CHARS_ALPHA_DISAMBIG = {'a', 'b', 'c', 'd', 'e', 'f',
                                'g', 'h', 'i', 'j', 'k', 'm',
                                'n', 'o', 'p', 'q', 'r', 's',
                                't', 'u', 'v', 'w', 'x', 'y', 'z',
                                'A', 'B', 'C', 'D', 'E', 'F', 'G',
                                'H', 'J', 'K', 'L', 'M',
                                'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                                'U', 'V', 'W', 'X', 'Y', 'Z'}

ALLOWED_CHARS_NUM = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

ALLOWED_CHARS_NUM_DISAMBIG = ['0', '2', '3', '4', '5', '6', '7', '8', '9']

ALLOWED_CHARS_SYMBOLS = {"!", "@", "#", "$", "%", "^", "&", "?",
                         "+", ":", ";", "-",
                         "'", ".", ",", "~"}

# For password generation
DEFAULT_SETTINGS = [0, '8', '3']

# Used to toggle password visibility
toggle = True

# Set by SignIn so other windows can place themselves in sane positions
global_x = 0
global_y = 0
table = None


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
