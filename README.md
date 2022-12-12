# Py Password Manager
## About
A Python password manager with a Tkinter GUI and encryption with SQLCipher.


### Features
- Multiple accounts
- Password generation
- Encryption with SQLCipher
- Shortcut button to open website for each account

## Installation
### Binaries

Windows and Linux binaries are provided and are the recommended way to try out the application. Please place in a directory where you have write permissions, the program will create a `data` directory to store each created `*.db` file.

### Source

- Clone the project using  `git clone https://github.com/travis-aaron/py_password_manager.git`
- A `pyproject.toml` is included for poetry and a `requirements.txt` for pip. Use `poetry install` or `pip install -r requirements.txt` depending on which you use.

#### Building SQLCipher

**SQLCipher** will need to be compiled.

##### Linux

- View the instructions on the [sqlcipher3](https://github.com/coleifer/sqlcipher3) page under the _[Building a statically linked library](https://github.com/coleifer/sqlcipher3#building-a-statically-linked-library)_ heading.
- A compiled version of SQLCipher for Python 3.11 on Linux is included in the `sqlcipher3` directory, it's recommended to use this only as a last resort. 

##### Windows

Compiling SQLCipher on Windows is trickier and not recommended. However, if you must, I recommend the excellent guide by [Dylan L Jones](https://github.com/dylanljones) included in his Pyrekordbox project: [SQLCipher Windows Instructions](https://github.com/dylanljones/pyrekordbox/blob/master/INSTALLATION.md#windows) 

