#excel 测试代码

import xlwt

xls = xlwt.Workbook()
sht1 = xls.add_sheet('Sheet1')
table_heads = ['商品名称','商品套餐','商品数量','商品价格','商家名称','订单号','总价格']
table_heads_len = len(table_heads)
for i in range(table_heads_len):
    sht1.write(0,i,table_heads[i])

# #添加字段
# sht1.write(0,0,'字段1')
# sht1.write(0,1,'字段2')
# sht1.write(0,2,'字段3')
# sht1.write(0,3,'字段4')
# #给字段中加值   考虑使用循环
# sht1.write(1,0,'值1')
# sht1.write(1,1,'值2')
# sht1.write(1,2,'值3')
# sht1.write(1,3,'值4')

xls.save('./mydata.xls')
