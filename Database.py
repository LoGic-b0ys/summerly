import sqlite3

class Database:
	'Class ini berisi tentang database'
	def __init__(self, file_name) :
		self.conn = sqlite3.connect(file_name)

	def read(self, table_name, column, where='') :
		# Query formulation from a table_name and the column
		query = "select "
		for cell in column[:-1]:
			query += cell + ', '
		query += column[-1]
		query += ' from ' + table_name

		query += where

		# Execute the query
		cursor = self.conn.execute(query)

		# Get the list from table
		res = []
		for row in cursor:
			res.append(row)
		return res

	def insert(self, table_name, column, data) :
		# Query formulation
		sql = 'insert into '
		sql += table_name + '('
		for cell in column[:-1]:
			sql += cell + ', '
		sql += column[-1] + ') values('
		for cell in column[:-1]:
			sql += '?,'
		sql += '?)'

		# Get the cursor
		c = self.conn.cursor()

		# Insert data
		c.execute(sql, data)

	def commit(self):
		self.conn.commit()

	def close(self):
		self.conn.close()