# Refactor this after match

# Untuk selenium webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Database import Database
from Review import Review

class Crawler:
	def __init__(self, file_name, url) :

		self.conn = Database(file_name)

		# Penggunaan webdriver path
		webdriver_path = './chromedriver'

		# Untuk browser tanpa windows
		chrome_options = Options()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--window-size=1920x1080')
		self.url = url
		url_part = url.split('/')
		self.browser = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)

		self.id_anime = url_part[4]
		self.title_anime = url_part[5]

	def setURL(self, url):
		self.url = url
		url_part = url.split('/')
		self.id_anime = url_part[4]
		self.title_anime = url_part[5]

	def process(self):
		# Buka browser tanpa windows dan menuju ke url dibawah
		self.browser.get(self.url)

		# Ambil list div kemudian detail dari search
		list_div = self.browser.find_element_by_class_name("js-scrollfix-bottom-rel")
		details_divs = list_div.find_elements_by_class_name("borderDark")

		# Fetch hasilnya dan kemudian simpan ke file
		for detail_div in details_divs:
			try :
				read_more = detail_div.find_element_by_class_name("js-toggle-review-button")
				self.browser.execute_script("arguments[0].click();", read_more)
			except :
				pass
			review = detail_div.find_element_by_class_name("textReadability").text.strip()
			review = review.split('\n')
			while("" in review) : 
				review.remove("")
			for line in review :
				sentences = line.split('.')
				while("" in sentences) :
					sentences.remove("")
				for sentence in sentences :
					stripped = sentence.strip()
					stripped = stripped.replace('"', '')
					review_data = (stripped, self.id_anime)
					self.conn.insert('sentences', ['sentences', 'anime_id'], review_data)

		self.conn.commit()

	def get_summary(self):
		r = Review('review_anime.db', self.id_anime, self.title_anime)

	def close(self):
		self.conn.close()
		self.browser.close()