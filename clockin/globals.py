
"""globals.py"""
from decouple import config

DB_URL = config("DB_URL")
DB_NAME = config("DATABASE")