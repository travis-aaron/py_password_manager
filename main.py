#!/usr/bin/env python3

from addnewpassword import AddNewPassword

from constants import background_color, dark_color
from constants import resource_path


from PIL import Image, ImageTk

from settings import Settings

from signin import SignIn


from tkinter import Frame, Button, Tk


class MainWindow:
    def main(self):
        master = Tk()
        master.title("Password Manager")

        width = 750
        height = 620
        x = master.winfo_screenwidth() // 2 - width // 2
        y = master.winfo_screenheight() // 2 - height // 2

        # Ensures window is placed in the center of the screen
        master.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        master.configure(bg=background_color)
        master.resizable(False, False)

        toolbar_frame = Frame(master, width=750, height=100, bg=dark_color)

        new_pass_img = Image.open(resource_path(
            'images/plus.png'))
        settings_img = Image.open(resource_path(
            'images/settings-gear-icon.png'))
        logout_img = Image.open(resource_path(
            'images/door.png'))

        newpassimg_resize = new_pass_img.resize(
            (64, 64),
            Image.Resampling.LANCZOS)

        settingsimg_resize = settings_img.resize(
            (64, 64),
            Image.Resampling.LANCZOS)

        logoutimg_resize = logout_img.resize(
            (64, 64),
            Image.Resampling.LANCZOS)

        newpass_button_img = ImageTk.PhotoImage(newpassimg_resize)
        settings_button_img = ImageTk.PhotoImage(settingsimg_resize)
        logout_button_img = ImageTk.PhotoImage(logoutimg_resize)

        new_pass = Button(
            toolbar_frame,
            image=newpass_button_img,
            borderwidth=0,
            highlightthickness=0,
            activebackground=dark_color,
            command=AddNewPassword)

        new_pass.configure(bg=dark_color)

        settings = Button(
            toolbar_frame,
            image=settings_button_img,
            borderwidth=0,
            highlightthickness=0,
            activebackground=dark_color,
            command=Settings)

        settings.configure(bg=dark_color)

        logout = Button(
            toolbar_frame,
            image=logout_button_img,
            borderwidth=0,
            highlightthickness=0,
            activebackground=dark_color,
            # The string argument here tells SignIn to make sure
            # all widgets are destroyed
            command=lambda: SignIn(x=x, y=y, master=master, logout="logout"))

        logout.configure(bg=dark_color)

        toolbar_frame.place(x=0, y=0)
        new_pass.place(x=225, y=20)
        settings.place(x=325, y=20)
        logout.place(x=425, y=20)

        SignIn(
            master=master,
            x=master.winfo_screenwidth() // 2,
            y=master.winfo_screenheight() // 2)

        master.mainloop()


if __name__ == "__main__":
    window = MainWindow()
    window.main()
