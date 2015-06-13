# -*- coding:UTF-8 -*-
import logging
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from urls import urls
from config import SETTINGS

define("port",default = 8888,help = "run on the port 8888",type = int)

class Application(tornado.web.Application):
	def __init__(self):
		tornado.web.Application.__init__(self,handlers = urls,**SETTINGS)

def main():
	tornado.options.parse_command_line()
	logging.info("Web服务启动，准备调用WebService")
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
