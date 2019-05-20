import sqlite3
from apyori import apriori

conn = sqlite3.connect('review_anime.db')

cursor = conn.execute("SELECT noun_list from sentence_noun")
transaction_list = []

for row in cursor:
	transaction = row[0].split(',')[:-1]
	if len(transaction) > 0 :
		transaction_list.append(transaction)

association_rules = apriori(transaction_list, min_support=0.001, min_confidence=0, min_lift=3, min_length=2)
association_results = list(association_rules)

features = []

for item in association_results:
	# first index of the inner list
	# Contains base item and add item
	pair = item[0] 
	items = [x for x in pair]
	features.append(items[0])

features = set(features)

sql = '''insert into feature(id_anime, feature) values(?,?)'''
feature_text = ''

for feature in features :
	feature_text += feature + '|'

cnt = conn.cursor()

cnt.execute(sql, (5114, feature_text))
conn.commit()

conn.close()