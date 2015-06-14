# -*- coding:UTF-8 -*-
import logging
import torndb
from operator import attrgetter
from config import SETTINGS
from action.base import BaseHandler

'''
商家管理模块
date:2015-06-14

'''

class SellerQueryHandler(BaseHandler):
	def get(self):
		'''
		获取商家信息
		date:2015-06-13

		'''
		pagesize = 10
		cd_name = self.get_argument("name",None)
		cd_curpage = self.get_argument("page",1)
		cd_pagesize = self.get_argument("pageSize",pagesize)
		cd_query_info = []

		logging.info(u"查询商家信息，关键词为："+cd_name)
		if cd_name:
			cd_query_info = self.db.query(
				"SELECT SQL_CALC_FOUND_ROWS id,name,address,code,telPhone,chatNum,addTime FROM tb_seller "
				"WHERE active=1 and name LIKE %s ORDER BY addTime DESC LIMIT %s,%s","%"+cd_name+"%",int(cd_pagesize)*(int(cd_curpage)-1),int(cd_pagesize)*int(cd_curpage))
			cd_query_count = self.db.get("SELECT FOUND_ROWS() as res")
			cd_query_pagecount = str((int(cd_query_count.res)+int(cd_pagesize)-1)/int(cd_pagesize))
		else:
			cd_query_info = self.db.query(
				"SELECT SQL_CALC_FOUND_ROWS id,name,address,code,telPhone,chatNum,addTime FROM tb_seller "
				"WHERE active=1 ORDER BY addTime DESC LIMIT %s,%s",int(cd_pagesize)*(int(cd_curpage)-1),int(cd_pagesize)*int(cd_curpage))
			cd_query_count = self.db.get("SELECT FOUND_ROWS() as res")
 			cd_query_pagecount = str((int(cd_query_count.res)+int(cd_pagesize)-1)/int(cd_pagesize))
		cd_table = ""
		if not cd_query_info:
			return
		for info in cd_query_info:
			cd_table += "<tr><td style='display:none'><input type='checkbox' class='chk_id' value='"+str(info.id)+"' />"+str(info.id)+"</td><td>"+info.name+"</td><td>"+info.telPhone+"</td><td>"+info.address+"</td><td>"+info.code+"</td><td>"+info.chatNum+"</td><td>"+str(info.addTime)+"</td><td align='center'><a href='javascript:void(0)' onclick="+"ShowDiv(this,'result_chart','1')"+"><img src='image/c_edit.png'></a>&nbsp;&nbsp;<a href='javascript:void(0)' onclick="+"javascript:seller_del(this)"+" style='margin-left:10px;'><img src='image/c_del.png'></a></td></tr>"
		self.write(cd_table+"|"+str(cd_query_count.res)+"|"+cd_query_pagecount+"|"+str(pagesize))  

class SellerInsertHandler(BaseHandler):
	def get(self):
		'''
		默认更新获取ID

		'''
		id = self.get_argument("id",None)
		self.write(id)

	def post(self):
		'''
		无ID就添加新数据，有ID，就更新数据
		date:2015-06-14

		'''
		id = self.get_argument("id",None)
		name = self.get_argument("name")
		address = self.get_argument("address")
		code = self.get_argument("code")
		phone = self.get_argument("phone")
		weixin = self.get_argument("weixin")

		if id:
			logging.info(u"更新商家信息请求，ID:"+id)
			cd_update = self.db.get("SELECT * FROM tb_seller WHERE active=1 and id = %s",int(id))
			if not cd_update:raise tornado.web.HTTPError(404)
			self.db.execute(
				"UPDATE tb_seller SET name = %s, address = %s, code = %s, telPhone = %s, chatNum = %s "
				"WHERE id = %s",name,address,code,phone,weixin,int(id))
			self.write("更新商家信息成功！")
		else:
			logging.info(u"添加商家信息请求,商家名称："+name)
			self.db.execute(
				"INSERT INTO tb_seller(name,address,code,telPhone,chatNum) "
				"VALUES(%s,%s,%s,%s,%s)",name,address,code,phone,weixin)
			self.write("添加商家信息成功！")

class SellerGetById(BaseHandler):
	def get(self):
		'''
		通过ID，获取单条信息的详细内容
		date:2015-06-14

		'''
		id = self.get_argument("id",None)

		logging.info(u"获取商家信息请求，ID:"+id)
		if id:
			cd_get_id = self.db.get(
				"SELECT id,name,address,code,telPhone,chatNum FROM tb_seller "
				"WHERE active=1 and id= %s",int(id))
			self.write(cd_get_id)
		else:
			self.write("获取该商家信息失败！")

class SellerDelHandler(BaseHandler):
	def post(self):
		'''
		通用ID删除商家信息，改变状态，不是物理删除
		date:2015-06-14

		'''
		id = self.get_argument("id",None)

		logging.info(u"删除商家信息请求，ID:"+id)
		if id:
			cd_del = self.db.get("SELECT * FROM tb_seller WHERE id = %s",int(id))
			if not cd_del:raise tornado.web.HTTPError(404)
			self.db.execute(
				"UPDATE tb_seller SET active = 0 "
				"WHERE id = %s",int(id))
			self.write("删除商家信息成功！")
		else:
			self.write("删除商家信息失败！")
