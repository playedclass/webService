# -*- coding: UTF-8 -*-
import json
import torndb
from config import SETTINGS
from action.base import BaseHandler

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

		logging.info("调用获取商家信息：要查询的商家为：" + cd_name)
		if cd_name:
			cd_query_info = self.db.query(
				"SELECT SQL_CALC_FOUND_ROWS id,name,address,code,telPhone,chatNum,addTime FROM tb_seller "
				"WHERE active=1 and name LIKE %s ORDER BY addTime DESC LIMIT %s,%s","%"+cd_name+"%",int(cd_pagesize)*(int(cd_curpage)-1),int(cd_pagesize)*int(cd_curpage))
			cd_query_count = self.db.get("SELECT FOUND_ROWS() as res")
			cd_query_pagecount = str((int(cd_query_count.res)+int(cd_pagesize)-1)/int(cd_pagesize))
		cd_table = ""
		if not cd_query_info:
			return
		for info in cd_query_info:
			cd_table += "<tr><td><input type='checkbox' class='chk_id' value='"+str(info.id)+"' />"+str(info.id)+"</td><td>"+info.name+"</td><td>"+info.telPhone+"</td><td>"+info.address+"</td><td>"+info.code+"</td><td>"+info.chatNum+"</td><td>"+str(info.addTime)+"</td><td align='center'><a href='javascript:void(0)' onclick="+"ShowDiv(this,'result_chart','1')"+"><img src='image/c_edit.png'></a>&nbsp;&nbsp;<a href='javascript:void(0)' onclick="+"javascript:seller_del(this)"+" style='margin-left:10px;'><img src='image/c_del.png'></a></td></tr>"
		self.write(cd_table+"|"+str(cd_query_count.res)+"|"+cd_query_pagecount+"|"+str(pagesize))  