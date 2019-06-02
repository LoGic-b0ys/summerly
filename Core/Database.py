import sqlite3

class Database:
	'''
		This class provide an interface to the database. We just cover a read and insert operation
		Because we can't update the review or delete that from the database
	'''

	'''
		This class construct with one argument, a single filename with sqlite3 format ofr python
	'''
	def __init__(self, file_name) :
		self.conn = sqlite3.connect(file_name) # The variable conn will be the database cursor


	'''
		This method provide interface to read a database and get the array of it. It didn't provide a column name.
		Instead python hold the result in a list of list so you can access column by their index e.g 0,1,2 etc.

		Parameter:
		table_name is a string
		column is a list that hold the name of column that you want to access
		where is a string that hold the filter
	'''
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

	'''
		This method provide interface to insert tha data to the table.

		Parameter
		table_name is a string
		column is a list that indicate the target column
		data is a tuple that indicate the data that you want to insert

		Note : column and data MUST be in the same order
	'''
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

	'''
		This method provide interface to commit the database. You must commit all the change to make your database
	'''
	def commit(self):
		self.conn.commit()

	'''
		This method rovide interface to close your database from the memory
	'''
	def close(self):
		self.conn.close()