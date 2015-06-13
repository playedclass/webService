#-*- coding: utf-8 -*-
import torndb
from tornado.options import define,options

define("mysql_host",default = "115.28.54.133:3306",help = "mysql host name")
define("mysql_database",default = "pltc_db",help = "database name")
define("mysql_user",default = "root",help = "database user")
define("mysql_password",default = "",help="database password")

class database():
	@classmethod
	def get_db():
		'''
		返回数据库连接信息
		date:2015-06-13
		
		'''
		self.db = torndb.Connection(
			host = options.mysql_host,database = options.mysql_database,
			user = options.mysql_user,password = options.mysql_password)
