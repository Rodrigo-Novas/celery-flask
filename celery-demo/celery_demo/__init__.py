from flask import Flask, get_flashed_messages, render_template, session, url_for, request, flash, redirect
import os



def create_app():
    app = Flask(__name__)

    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = "Rodri Novas"
    app.config['MAIL_PASSWORD'] = os.environ.get('CONTRASEÑA')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL')
    app.secret_key = "clave"
    return app