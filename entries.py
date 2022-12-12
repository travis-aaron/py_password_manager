#!/usr/bin/env python3

from addnewpassword import AddNewPassword

from constants import active_color, background_color, dark_color
from constants import toggle  # noqa: F401
from constants import resource_path

from db import retrieve_all_entries, return_entry, sort_entries, delete_entry

from PIL import Image, ImageTk

from tkinter import Canvas, Frame, Scrollbar, Label, Menubutton, Menu
from tkinter import TOP, LEFT, BOTH
from tkinter import ttk

import webbrowser


# Class that displays widgets + data in root window
class Table:
    def __init__(self, master=None):
        self.rows = 1

        self.passvis_img = Image.open(
            resource_path("images/eye-icon.png"))
        self.passhid_img = Image.open(
            resource_path("images/eye-blind-icon.png"))

        self.passvis_resized = self.passvis_img.resize(
                                                      (15, 13),
                                                      Image.Resampling.LANCZOS)
        self.passhid_resized = self.passhid_img.resize(
                                                      (15, 13),
                                                      Image.Resampling.LANCZOS)

        self.passwd_visible = ImageTk.PhotoImage(self.passvis_resized)
        self.passwd_hidden = ImageTk.PhotoImage(self.passhid_resized)

        self.openurl_image = ImageTk.PhotoImage(
            Image.open(resource_path("images/openurl.png")))
        self.edit_image = ImageTk.PhotoImage(
            Image.open(resource_path("images/edit.png")))
        self.delete_image = ImageTk.PhotoImage(
            Image.open(resource_path("images/delete.png")))

        self.pass_frame = Frame(master, height=500, width=750)
        self.pass_frame.place(x=0, y=120)

        # Canvas/frame for creating scrollbar
        self.canvas = Canvas(
            self.pass_frame,
            height=500,
            width=750,
            highlightthickness=0,
            borderwidth=0)

        self.column_header_frame = Frame(
            master,
            width=750,
            height=25,
            borderwidth=0,
            highlightthickness=0,
            bg=dark_color)

        # Placed after column header to avoid overlap
        self.scroll_bar = Scrollbar(
            master,
            orient='vertical',
            bg=dark_color,
            troughcolor=dark_color,
            activebackground=active_color,
            borderwidth=1,
            highlightthickness=0,
            highlightbackground=active_color,
            command=self.canvas.yview)

        # Menus to sort columns
        self.column_mb_date = Menubutton(
            self.column_header_frame,
            width=5,
            text="Date",
            font=('Helvetica', 12),
            bg=dark_color,
            fg=active_color,
            activeforeground=dark_color,
            activebackground=active_color,
            highlightcolor=active_color)

        self.column_mb_serv = Menubutton(
            self.column_header_frame,
            width=10,
            text="Service",
            font=('Helvetica', 12),
            bg=dark_color,
            fg=active_color,
            activeforeground=dark_color,
            activebackground=active_color,
            highlightcolor=active_color)

        self.column_mb_user = Menubutton(
            self.column_header_frame,
            width=8,
            text="Username",
            font=('Helvetica', 12),
            bg=dark_color,
            fg=active_color,
            activeforeground=dark_color,
            activebackground=active_color,
            highlightcolor=active_color)

        self.column_l4 = Label(
            self.column_header_frame,
            width=12,
            text="Password",
            relief="flat",
            font=('Helvetica', 12),
            bg=dark_color,
            fg=active_color)

        # Configuration to allow scrolling
        self.scrollable_frame = Frame(self.canvas)
        self.scrollable_frame.configure(bg=background_color)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw")

        self.canvas.configure(
            yscrollcommand=self.scroll_bar.set,
            bg=background_color, border=0)

        self.canvas.pack(side="left", fill="both")

        self.column_header_frame.place(y=100)
        self.column_mb_date.place(x=0)
        self.column_mb_serv.place(x=103)
        self.column_mb_user.place(x=225)
        self.column_l4.place(x=317, y=4)

        self.column_mb_date.menu = Menu(
            self.column_mb_date,
            tearoff=0,
            background=dark_color,
            foreground=active_color,
            activeforeground=dark_color,
            activebackground=active_color)

        self.column_mb_date["menu"] = self.column_mb_date.menu

        self.column_mb_date.menu.add_command(
            label="Ascending",
            command=lambda: self.sort("date+"))

        self.column_mb_date.menu.add_command(
            label="Descending",
            command=lambda: self.sort("date-"))

        self.column_mb_serv.menu = Menu(
            self.column_mb_serv,
            tearoff=0,
            background=dark_color,
            foreground=active_color,
            activeforeground=dark_color,
            activebackground=active_color)

        self.column_mb_serv["menu"] = self.column_mb_serv.menu

        self.column_mb_serv.menu.add_command(
            label="Ascending",
            command=lambda: self.sort("serv_name+"))

        self.column_mb_serv.menu.add_command(
            label="Descending",
            command=lambda: self.sort("serv_name-"))

        self.column_mb_user.menu = Menu(
            self.column_mb_user,
            tearoff=0,
            background=dark_color,
            foreground=active_color,
            activeforeground=dark_color,
            activebackground=active_color)

        self.column_mb_user["menu"] = self.column_mb_user.menu

        self.column_mb_user.menu.add_command(
            label="Ascending",
            command=lambda: self.sort("username+"))

        self.column_mb_user.menu.add_command(
            label="Descending",
            command=lambda: self.sort("username-"))

        self.scroll_bar.pack(side="right", fill="y")

        self.widgets: list = []
        self.row_frame_list: list = []
        retrieve_all_entries()
        entries = retrieve_all_entries()
        self.populate(entries)

    # Receives [{}] array, dict with db entries to
    # turn to widgets. Used on login, and also
    # when adding a single row
    def populate(self, entries):
        style = ttk.Style()
        style.configure('passFrameLabel.TLabel',
                        width=15,
                        font=('Helvetica', 9),
                        background=background_color,
                        foreground="white",
                        borderwidth=0,
                        highlightthickness=0,
                        anchor='w')

        style.configure('passFrameButton.TButton',
                        highlightthickness=0,
                        borderwidth=0,
                        background=background_color,
                        focuscolor="none")

        style.map('passFrameButton.TButton',
                  background=[('active', background_color)])

        # Establish # of already existing widgets
        # If none, there'll be no effect
        # Otherwise, we populate AFTER them
        widget_count = len(self.widgets)

        for i, entry in enumerate(entries):
            self.row_frame = Frame(
                self.scrollable_frame,
                width=730,
                height=20,
                borderwidth=0,
                highlightthickness=0,
                bg=background_color)
            self.row_frame.pack(side=TOP, fill=None, expand=False, pady=5)
            self.row_frame_list.append(self.row_frame)

            if 'Date' in entry:
                widget = widget_count+i*8
                self.e = ttk.Label(
                    self.row_frame,
                    style='passFrameLabel.TLabel')
                self.widgets.append(self.e)
                self.set(widget, entry['Date'])
                self.e.pack(side=LEFT, fill=BOTH, padx=(12, 0))

            if 'Service Name' in entry:
                widget = widget_count+i*8+1
                self.e2 = ttk.Label(
                    self.row_frame,
                    style='passFrameLabel.TLabel')
                self.widgets.append(self.e2)
                self.set(widget, entry['Service Name'])
                self.e2.pack(side=LEFT, fill=BOTH, padx=(11, 0))

            if 'Username' in entry:
                widget = widget_count+i*8+2
                self.e3 = ttk.Label(
                    self.row_frame,
                    style='passFrameLabel.TLabel')
                self.widgets.append(self.e3)
                self.set(widget, entry['Username'])
                self.e3.pack(side=LEFT, fill=BOTH)

            if 'Password' in entry:
                widget = widget_count+i*8+3
                self.e4 = ttk.Label(
                    self.row_frame,
                    style='passFrameLabel.TLabel')
                self.b = ttk.Button(
                    self.row_frame,
                    width=15,
                    image=self.passwd_visible,
                    style='passFrameButton.TButton')
                self.widgets.append(self.e4)
                self.widgets.append(self.b)
                password = ["*" for char in range(len(entry['Password']))]
                flattened_password = flattened_password = ''.join(password)
                self.set(widget, flattened_password)
                self.e4.pack(side=LEFT, fill=BOTH)
                self.b.pack(side=LEFT, fill=BOTH, padx=5)

            if 'URL' in entry:
                widget = widget_count+i*8+2
                self.b2 = ttk.Button(
                    self.row_frame,
                    image=self.openurl_image,
                    style='passFrameButton.TButton')
                self.b3 = ttk.Button(
                    self.row_frame,
                    image=self.edit_image,
                    style='passFrameButton.TButton')
                self.b4 = ttk.Button(
                    self.row_frame,
                    image=self.delete_image,
                    style='passFrameButton.TButton')
                self.widgets.append(self.b2)
                self.widgets.append(self.b3)
                self.widgets.append(self.b4)
                self.b2.pack(side=LEFT, fill=BOTH, padx=3)
                self.b3.pack(side=LEFT, fill=BOTH, padx=3)
                self.b4.pack(side=LEFT, fill=BOTH, padx=3)
                self.b.configure(
                                command=lambda button=self.b:
                                self.find_widget(button))
                self.b2.configure(
                                command=lambda button=self.b2:
                                self.find_widget(button))
                self.b3.configure(
                                command=lambda button=self.b3:
                                self.find_widget(button))
                self.b4.configure(
                                command=lambda button=self.b4:
                                self.find_widget(button))

    def refresh(self):
        self.pass_frame.destroy()
        self.scroll_bar.destroy()
        self.scrollable_frame.destroy()
        self.canvas.destroy()
        self.row_frame_list.clear()
        self.widgets.clear()
        self.__init__()

    # For deleting a single row of widgets only
    def delete_row(self, widget_index):
        service = self.widgets[widget_index - 6]
        # Remove from the Database
        delete_entry(service.cget("text"))
        self.refresh()

    # Deletes everything in the middle instead of
    # reinitializing like refresh would
    def delete_all_widgets(self):
        for row in self.row_frame_list:
            row.destroy()
        for widget in self.widgets:
            widget.destroy()
        self.pass_frame.destroy()
        self.scrollable_frame.destroy()
        self.scroll_bar.destroy()
        self.canvas.destroy()

    def delete_entry_widgets(self):
        for row in self.row_frame_list:
            row.destroy()
        for widget in self.widgets:
            widget.destroy()

    def set(self, cell: int, value: str):
        widget = self.widgets[cell]
        widget.configure(text=value)

    def open_url(self, widget_index):
        service = self.widgets[widget_index - 4].cget("text")
        entry = return_entry(service)
        webbrowser.open(entry["URL"], new=2, autoraise=True)

    def toggle_password_visible(self, widget_index):
        global toggle
        toggle_widget = widget_index-1
        service = self.widgets[widget_index-3].cget("text")
        return_entry(service)

        res = return_entry(service)
        password = res['Password']
        if toggle:
            self.widgets[toggle_widget+1].configure(image=self.passwd_hidden)
            self.widgets[toggle_widget+1].photo = self.passwd_hidden
            self.set(toggle_widget, password)
            toggle = False
        else:
            self.set(toggle_widget, password)
            char_length = self.widgets[widget_index-1].cget("text")
            hidden_pass_list = ["*" for i in char_length]
            # Get rid of the spaces in hidden_pass_list
            hidden_pass = ''.join(hidden_pass_list)
            self.widgets[toggle_widget+1].configure(image=self.passwd_visible)
            self.widgets[toggle_widget+1].photo = self.passwd_visible
            self.set(toggle_widget, hidden_pass)
            toggle = True

    # The lambda function on each button passes
    # the id for which button was pressed.
    # Here we can use Modulo to find which function to call.
    def find_widget(self, widget):
        widget_index = self.widgets.index(widget)
        if widget_index % 8 == 7:
            self.delete_row(widget_index)
        elif widget_index % 8 == 6:
            AddNewPassword(
                row_number=int(widget_index/7+1),
                service=self.widgets[widget_index-5].cget("text"))
        elif widget_index % 8 == 5:
            self.open_url(widget_index)
        elif widget_index % 8 == 4:
            self.toggle_password_visible(widget_index)

    def sort(self, direction):
        self.delete_entry_widgets()
        sort_entries(direction)
        entries = sort_entries(direction)
        self.populate(entries)
