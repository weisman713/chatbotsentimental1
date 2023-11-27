# chatbotsentimental1
chatbot de recomendacion de anime
para la compilacion de la aplicacion tener en cuenta instalar las herramientas utilizadas:
import json,
from flask import Flask, render_template, request, redirect, url_for, session, jsonify,
from flask_sqlalchemy import SQLAlchemy,
from flask_bcrypt import Bcrypt,
import nltk,
from nltk.chat.util import Chat, reflections,
from spellchecker import SpellChecker,
import unidecode  # Para quitar las tildes,
import datetime,
from AnilistPython import Anilist,
from mastodon import Mastodon,
from bs4 import BeautifulSoup,
from pysentimiento import create_analyzer,
from translate import Translator,

pruebas realizadas por los estudiantes robinson lopez sanclemente y juan camilo morales fernandez

https://drive.google.com/drive/folders/19vAxJ3ZM2oErphm1zCiYMXwnzNzJNjfm?usp=drive_link
