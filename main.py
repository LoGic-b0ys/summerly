from Review import Review
from crawler import Crawler

c = Crawler('review_anime.db', 'https://myanimelist.net/anime/4181/Clannad__After_Story/reviews')
c.process()
c.get_summary()
c.setURL('https://myanimelist.net/anime/35247/Owarimonogatari_2nd_Season/reviews')
c.process()
c.get_summary()
c.close()