from Review import Review
from Crawler import Crawler

c = Crawler('review_anime.db')
url = input('Masukkan url: ')
depth = int(input('Masukkan kedalaman: '))

for i in range(2,depth+1):
	c.setURL(url+'?p='+str(i))
	c.process()

print('Getting summary')
c.get_summary()
c.close()