#!/usr/bin/env python3

import datetime

from errors import CustomError

import os
from os.path import exists

from peewee import Model, CharField, DateTimeField, IntegerField, BooleanField
from peewee import DatabaseError, OperationalError

from playhouse.sqlcipher_ext import SqlCipherDatabase

import sys

database = SqlCipherDatabase(None)


class Entry(Model):
    serv_name = CharField(unique=True, max_length=15)
    serv_url = CharField()
    user_entry = CharField(max_length=15)
    pass_entry = CharField(max_length=15)
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database


class Settings(Model):

    num_of_symbols = IntegerField()
    pass_length = IntegerField()
    ambiguous_symbols = BooleanField()

    class Meta:
        database = database


def write_settings(symbols, length, ambiguous):
    Settings.select()
    Settings.delete().execute()
    Settings.create(
        num_of_symbols=symbols,
        pass_length=length,
        ambiguous_symbols=ambiguous)


def return_settings():
    settings = {}
    try:
        query = Settings.select().order_by(Settings.num_of_symbols)
        for entry in query:
            settings["Number of Symbols"] = entry.num_of_symbols,
            settings["Password Length"] = entry.pass_length,
            settings["Ambiguous Symbols"] = entry.ambiguous_symbols
        return settings
    except Exception:
        return "uninitialized"


# Create a new database and initial entry after registration
def initialize(window, user, password, password2):
    try:
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            os.mkdir(application_path+'/data', mode=0o777)
        elif __file__:
            application_path = os.path.dirname(__file__)
        if not exists(f'data/{user}.db') and user and password:
            if password == password2:
                database.init(
                              f'data/{user}.db',
                              passphrase=password,
                              pragmas={'kdf_iter': 64000})
                Entry.create_table()
                Entry.create(
                    serv_name="PasswordDB",
                    serv_url="http://localhost",
                    user_entry=user,
                    pass_entry=password)
                Settings.create_table()
                window.destroy()
            else:
                raise CustomError(
                    window,
                    message="The provided passwords don't match")
        elif not user or not password:
            raise CustomError(window, "Please fill in all fields.")
        else:
            print("File exists")
    except OperationalError as e:
        raise CustomError(window, f"Unable to create database: {e}")


def sign_in(user, password, window):
    try:
        if os.path.exists(f'data/{user}.db'):
            database.init(
                          f'data/{user}.db',
                          passphrase=password,
                          pragmas={'kdf_iter': 64000})
            database.connect()
            database.get_tables()
            window.destroy()
            return "create_table"
        else:
            raise CustomError(window, "Account does not exist.")
    except DatabaseError:
        raise CustomError(window, "Incorrect username or password")


def add_password(serv_name, serv_url, user_entry, pass_entry):
    entry_array = []
    Entry.create(
        serv_name=serv_name,
        serv_url=serv_url,
        user_entry=user_entry,
        pass_entry=pass_entry)
    query = Entry.select().order_by(Entry.date.desc())
    for entry in query:
        entry_array.append({
            "Date": entry.date.strftime('%b %d, %Y'),
            "Service Name": entry.serv_name,
            "Username": entry.user_entry,
            "Password": entry.pass_entry,
            "URL": entry.serv_url})
    return entry


def log_out():
    database.close()


def delete_entry(service):
    Entry.delete().where(Entry.serv_name == service).execute()


def return_entry(service):
    query = Entry.select().where(Entry.serv_name == service).execute()
    entry_fields = {}
    for entry in query:
        entry_fields["Date"] = entry.date.strftime('%b %d, %Y')
        entry_fields["Service Name"] = entry.serv_name
        entry_fields["Username"] = entry.user_entry
        entry_fields["Password"] = entry.pass_entry
        entry_fields["URL"] = entry.serv_url
    return entry_fields


def retrieve_all_entries(filter=None):
    entries = []
    query = Entry.select().order_by(Entry.date.desc())
    for entry in query:
        entries.append({
            "Date": entry.date.strftime('%b %d, %Y'),
            "Service Name": entry.serv_name,
            "Username": entry.user_entry,
            "Password": entry.pass_entry,
            "URL": entry.serv_url})
    return entries


def sort_entries(field):
    entries = []
    match field:
        case "serv_name+":
            rows = Entry.select().order_by(Entry.serv_name)
            for row in rows:
                entries.append({
                    "Date": row.date.strftime('%b %d, %Y'),
                    "Service Name": row.serv_name,
                    "Username": row.user_entry,
                    "Password": row.pass_entry,
                    "URL": row.serv_url})
            return entries
        case "serv_name-":
            rows = Entry.select().order_by(Entry.serv_name.desc())
            for row in rows:
                entries.append({
                    "Date": row.date.strftime('%b %d, %Y'),
                    "Service Name": row.serv_name,
                    "Username": row.user_entry,
                    "Password": row.pass_entry,
                    "URL": row.serv_url})
            return entries
        case "date+":
            rows = Entry.select().order_by(Entry.date)
            for row in rows:
                entries.append({
                    "Date": row.date.strftime('%b %d, %Y'),
                    "Service Name": row.serv_name,
                    "Username": row.user_entry,
                    "Password": row.pass_entry,
                    "URL": row.serv_url})
            return entries
        case "date-":
            rows = Entry.select().order_by(Entry.date.desc())
            for row in rows:
                entries.append({
                    "Date": row.date.strftime('%b %d, %Y'),
                    "Service Name": row.serv_name,
                    "Username": row.user_entry,
                    "Password": row.pass_entry,
                    "URL": row.serv_url})
            return entries
        case "username+":
            rows = Entry.select().order_by(Entry.user_entry)
            for row in rows:
                entries.append({
                    "Date": row.date.strftime('%b %d, %Y'),
                    "Service Name": row.serv_name,
                    "Username": row.user_entry,
                    "Password": row.pass_entry,
                    "URL": row.serv_url})
            return entries
        case "username-":
            rows = Entry.select().order_by(Entry.user_entry.desc())
            for row in rows:
                entries.append({
                    "Date": row.date.strftime('%b %d, %Y'),
                    "Service Name": row.serv_name,
                    "Username": row.user_entry,
                    "Password": row.pass_entry,
                    "URL": row.serv_url})
            return entries


def update_entry(update, service_name):
    try:
        Entry.update(
            serv_name=update['Service Name'],
            serv_url=update['URL'],
            user_entry=update['Username'],
            pass_entry=update['Password'],
            date=datetime.datetime.now()
        ).where(Entry.serv_name == service_name).execute()

        update['Date'] = datetime.datetime.now().strftime('%b %d, %Y')
        return update
    except Exception:
        return "failed!"
