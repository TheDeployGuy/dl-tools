# DL Subs Back-end application

The back-end application will be developed in Python. 

Reasons for choosing Python:

* Easy to get started
* Flask is an easy to use quick start server library we can use to get first version done quickly
* Dive deeper into Python3 and its changes.

[Hello World in Flask](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
# Getting Started

Python uses the concept of virtual environments. A virtual environment is a complete copy of the Python interpreter. When you install packages in a virtual environment, the system-wide Python interpreter is not affected, only the copy is.

Create a virtual environment by running: `python3 -m venv venv`

This will create a Virtual Environment called venv.

Activate your virtual environment by running: `source venv/bin/activate`

Install the dependencies by running: `pip install -r requirements.txt`

# Project setup

In Python, a sub-directory that includes a __init__.py file is considered a package, and can be imported. When you import a package, the __init__.py executes and defines what symbols the package exposes to the outside world.

