import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

from settings.common import Settings

SETTINGS_MODULE = 'settings.deployed'

app = Flask(
    __name__,
    static_folder=Settings.STATIC_DIRECTORY,
    template_folder=Settings.TEMPLATE_DIRECTORY
)
app.config.from_object(SETTINGS_MODULE)

from app import views

def main():
    app.run()

