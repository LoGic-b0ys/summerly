# This is the library we use
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# This is our library
from Core.Database import Database
from Tools.Review import Review


'''
	This class provide interface to the crawler with selenium and chromedriver

	Role of this class is a crawler so you can implement this if you want to crawl the web
'''
class Crawler:

	'''
		This class construct with 2 argument.

		file_name is a string that indicates where you want to put your crawl result in a database.
		url is a string where is your review
	'''
	def __init__(self, file_name) :

		self.conn = Database(file_name)  # This is our database interface

		# We use chrome web driver
		webdriver_path = './chromedriver'

		# This is our browsing option
		chrome_options = Options()
		chrome_options.add_argument('--headless') # We don't browse with a window
		chrome_options.add_argument('--window-size=1920x1080') # And UltraHD screen size
		self.browser = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)

		self.url = ''
		self.id_anime = ''
		self.title_anime = ''

	'''
		This method provide an interface to change the URL and automatically change the anime id too
	'''
	def setURL(self, url):
		self.url = url
		url_part = url.split('/')
		self.id_anime = url_part[4]
		self.title_anime = url_part[5]


	'''
		This is our main crawl process. After the preparation is complete we can execute this to crawl the web
	'''
	def process(self):
		data = self.conn.read('anime_list', ['id', 'judul'], ' WHERE id='+self.id_anime)
		if len(data) == 0:
			self.conn.insert('anime_list', ['id', 'judul'], (self.id_anime, self.title_anime))
		# Open the url
		self.browser.get(self.url)

		'''
			You can change this to your preferred review container
		'''
		list_div = self.browser.find_element_by_class_name("js-scrollfix-bottom-rel")
		details_divs = list_div.find_elements_by_class_name("borderDark")

		# Make a loop through the review
		for detail_div in details_divs:
			try :
				# In animelist we must click the read more to read the complete review so we clic it
				read_more = detail_div.find_element_by_class_name("js-toggle-review-button")
				self.browser.execute_script("arguments[0].click();", read_more)
			except :
				pass
			review = detail_div.find_element_by_class_name("textReadability").text.strip()
			review = review.split('\n')

			# This is our preprocessing and sentence tokenizing
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
		print('Process complete')

	'''
		The main summarization process is handled by the Review class and we call it from here
	'''
	def get_summary(self, feature_list):
		r = Review('review_anime.db', self.id_anime, feature_list)
		return r.get_summary()
	'''
		We close the browser and the database
	'''
	def close(self):
		self.conn.close()
		self.browser.close()