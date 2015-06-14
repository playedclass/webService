# -*- coding: UTF-8 -*-
from action.handlers import *
	
urls = [
    #商家用户管理
    (r'/sellers/insert',SellerInsertHandler),
    (r'/sellers/query',SellerQueryHandler),
    (r'/sellers/getbyid',SellerGetById),
    (r'/sellers/del',SellerDelHandler),
]