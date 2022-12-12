#!/usr/bin/env python3


from constants import DEFAULT_SETTINGS, ALLOWED_CHARS_ALPHA
from constants import ALLOWED_CHARS_ALPHA_DISAMBIG, ALLOWED_CHARS_NUM
from constants import ALLOWED_CHARS_NUM_DISAMBIG, ALLOWED_CHARS_SYMBOLS

from db import return_settings

import random


def password_gen():
    # Generate two lists, one with symbols and one with letters/numbers
    # Pop the symbols out of both lists at random and place them into new list
    db_settings = return_settings()
    if db_settings != "uninitialized":
        password_length = db_settings[0]["Password Length"]
        ambiguous_chars = db_settings[0]["Ambiguous Symbols"]
        symbol_count = db_settings[0]["Number of Symbols"]
    else:
        password_length = int(DEFAULT_SETTINGS[1])
        ambiguous_chars = DEFAULT_SETTINGS[0]
        symbol_count = int(DEFAULT_SETTINGS[2])
    pass_list = []

    for _ in range(password_length-symbol_count):
        char_type = random.randint(0, 1)
        if char_type == 0 and ambiguous_chars == 0:  # Letters
            pass_list.append(
                random.SystemRandom().choice(tuple(ALLOWED_CHARS_ALPHA)))
        elif char_type == 1 and ambiguous_chars == 0:  # Numbers
            pass_list.append(
                random.SystemRandom().choice(tuple(ALLOWED_CHARS_NUM)))
        # Letters, no ambiguous characters
        elif char_type == 0 and ambiguous_chars == 1:
            pass_list.append(
                random.SystemRandom().choice(
                    tuple(ALLOWED_CHARS_ALPHA_DISAMBIG)))
        # Numbers, no ambiguous characters
        elif char_type == 1 and ambiguous_chars == 1:
            pass_list.append(
                random.SystemRandom().choice(
                    tuple(ALLOWED_CHARS_NUM_DISAMBIG)))
    for i in range(symbol_count):
        pass_list.append(
            random.SystemRandom().choice(tuple(ALLOWED_CHARS_SYMBOLS)))
    random.shuffle(pass_list)
    pass_str = ''.join(pass_list)
    return pass_str
