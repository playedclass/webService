# -*- coding: UTF-8 -*-
import logging
import torndb
from action.conn import database
from tornado.web import RequestHandler as BaseRequestHandler,HTTPError

class BaseHandler(BaseRequestHandler):
	@property
	def db(self):
	    return database.get_db()

	def set_default_headers(self):
		'''
		添加跨域处理header
		date:2015-06-12

		'''
		self.set_header('Access-Control-Allow-Origin','*')
		self.set_header('Access-Control-Allow-Methods','POST,GET,OPTIONS')
		self.set_header('Access-Control-Max-Age',1000)
		self.set_header('Access-Control-Allow-Headers','*')
	