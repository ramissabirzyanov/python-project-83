from flask import Flask, render_template, redirect, request, flash, url_for
from dotenv import load_dotenv
from page_analyzer.url import normalize_url
from .data_base import URL_DB
import os
import validators


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def add_url():
    url = normalize_url(request.form.get('url'))
    if not validators.url(url) or len(url) > 255:
        flash('Некорректный URL', category='danger')
        return render_template('index.html'), 422
    bd = URL_DB()
    data_urls = bd.get_data_by_name(url)
    if data_urls:
        id = data_urls['id']
        flash('Страница уже существует', category='info')
        return redirect(url_for('url_page', id=id))
    bd.save_to_db(url)
    id = bd.get_id_by_name(url)
    flash('Страница успешно добавлена', category='success')
    return redirect(url_for('url_page', id=id))


@app.route('/urls', methods=['GET'])
def get_urls():
    bd = URL_DB()
    urls = bd.get_urls()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:id>')
def url_page(id):
    bd = URL_DB()
    url = bd.get_url_by_id(id)
    return render_template('url.html', url=url)
