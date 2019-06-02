from Tools.Review import Review

r = Review('review_anime.db', '32281', ['story', 'art', 'character', 'plot'])
r.get_summary()
r.save()