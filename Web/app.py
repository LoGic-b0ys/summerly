from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from Core.Database import Database
from Core.Crawler import Crawler
# from Tools.Article import Article

class WebApp:
	def __init__(self, db_name):
		app = Flask(__name__)

		@app.route('/')
		def index():
			db = Database(db_name)
			row = db.read('anime_list', ['id', 'judul'])
			return render_template('index.html', data_title = row)

		@app.route('/anime/<int:id>')
		def anime(id):
			db = Database(db_name)
			title = db.read('anime_list', ['judul'], ' WHERE id='+str(id))[0][0]
			opinion = db.read('opinion_orientation', ['feature_name', 'good', 'bad'], ' WHERE id_anime='+str(id))
			return render_template('opinion.html', title = title, opinions = opinion)

		Bootstrap(app)

		self.webapp = app

	def get_app(self):
		return self.webapp