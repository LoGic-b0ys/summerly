# Refactor this after match

# Untuk selenium webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import sqlite3

conn = sqlite3.connect('review_anime.db')

# Penggunaan webdriver path
webdriver_path = './chromedriver'

# Untuk browser tanpa windows
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1920x1080')
url = "https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood/reviews?p=1"
url_part = url.split('/')

id_anime = url_part[4]
title_anime = url_part[5]

# Buka browser tanpa windows dan menuju ke url dibawah
browser = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)
browser.get(url)

# Ambil list div kemudian detail dari search
list_div = browser.find_element_by_class_name("js-scrollfix-bottom-rel")
details_divs = list_div.find_elements_by_class_name("borderDark")

sql = ''' INSERT INTO sentences(judul, sentences, anime_id) VALUES(?,?,?) '''
cur = conn.cursor()

# Fetch hasilnya dan kemudian simpan ke file
for detail_div in details_divs:
	try :
		read_more = detail_div.find_element_by_class_name("js-toggle-review-button")
		browser.execute_script("arguments[0].click();", read_more)
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
			review_data = (title_anime, stripped, id_anime)
			cur.execute(sql, review_data)
conn.commit()
conn.close()

# Close browsernya
browser.quit()