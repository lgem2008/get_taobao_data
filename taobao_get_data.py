# 爬取淘宝订单
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from bs4 import BeautifulSoup
from wxpy import *
import time
import math
import winsound
import random
import xlwt
import csv

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # => 为Chrome配置无头模式
options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
  "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})
driver.maximize_window()
driver.implicitly_wait(10) # seconds
driver.get("https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a21bo.jianhua.1997525045.2.5af911d913ex0r")
driver.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys("*********") 
driver.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys("*********")
driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button').click()

time.sleep(0.2)
dataView_info = driver.find_element(By.XPATH, '//*[@id="tp-bought-root"]')
time.sleep(0.2)
# print(dataView_info.text)
print("-----------------------1-----------------------")

for num in range(4,8):
    try:
        table_xpath = 'div[' + str(num) + ']'
        # table1 = dataView_info.find_element(By.XPATH,'div[4]')          #第一个商家的物品
        table1 = dataView_info.find_element(By.XPATH,table_xpath)          #第一个商家的物品
        # print("=====================================")
        # print(table_xpath)
        # print("=====================================")
        # print(table1.text)
        tbody1 = table1.find_element(By.XPATH,'div/table/tbody[1]')     #表头
        # print(tbody1.text)
        goods_data = tbody1.find_element(By.XPATH,'tr/td[1]/label')                #日期
        print("goods_data",goods_data.text)
        goods_order_id = tbody1.find_element(By.XPATH,'tr/td[1]/span/span[3]')                 #订单号
        print("goods_order_id",goods_order_id.text)
        goods_business_name = tbody1.find_element(By.XPATH,'tr/td[2]')                 #商家名称
        print("goods_business_name",goods_business_name.text)
        # # #excel 创建
        # # xls = xlwt.Workbook()
        # # sht1 = xls.add_sheet('Sheet1')
        # # table_heads = ['商品名称','商品套餐','商品数量','商品价格','商家名称','订单号','总价格','购买日期']
        # # table_heads_len = len(table_heads)
        # # for i in range(table_heads_len):
        # #     sht1.write(0,i,table_heads[i])
        # # sht1.write(1,4,goods_business_name.text)    
        # # sht1.write(1,5,goods_order_id.text)    
        # # sht1.write(1,7,goods_data.text)  
        # # xls.save('./mydata.xls')
        
        table_heads = ['商品名称','商品套餐','商品数量','商品价格','商家名称','订单号','总价格','购买日期']
        with open("test.csv", 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(table_heads)

        # # //*[@id="tp-bought-root"]/div[4]/div/table/tbody[1]/tr/td[1]/label/span[2]      日期
        # # //*[@id="tp-bought-root"]/div[4]/div/table/tbody[1]/tr/td[1]/span/span[3]       订单号
        # # //*[@id="tp-bought-root"]/div[4]/div/table/tbody[1]/tr/td[2]/span/a             商家名称
        tbody2 = table1.find_element(By.XPATH,'div/table/tbody[2]')
        time.sleep(1)
        print(tbody2.text)
        print("-----------------------7-----------------------")


        rows = tbody2.find_elements(By.TAG_NAME,'tr')   #查找每个表格中的行数
        before_add_numbers = len(rows)
        print(before_add_numbers)
        # print(rows)
        print("-----------------------8-----------------------")
        for i in range(before_add_numbers):
            print("The num of the goods:", i+1)
            # for row in rows:
            # print(row.text)
            goods_num_choice_xpath = "tr["+str(i+1)+"]"
            # print(goods_num_choice_xpath)
            goods_num_choice = tbody2.find_element(By.XPATH,goods_num_choice_xpath)
            goods_name = goods_num_choice.find_element(By.XPATH,'td[1]/div/div[2]/p[1]/a[1]/span[2]')
            print("goods_name:",goods_name.text)
            try:
                goods_choice = goods_num_choice.find_element(By.XPATH,'td[1]/div/div[2]/p[2]/span/span[3]').text
                print("goods_choice:",goods_choice)
            except:
                goods_choice = ''
                print("goods_choice:",goods_choice)

            goods_price_xpath = 'td[2]/div'
            k = goods_num_choice.find_element(By.XPATH,goods_price_xpath)
            a = k.find_elements(By.TAG_NAME,'p')   #查找每个表格中的行数
            goods_price_num = len(a)
            print("----------------------------------------------")
            print(goods_price_num)
            print("----------------------------------------------")
            if(goods_price_num == 1):
                goods_price = goods_num_choice.find_element(By.XPATH,'td[2]/div/p/span[2]')
            elif(goods_price_num == 2):
                goods_price = goods_num_choice.find_element(By.XPATH,'td[2]/div/p[2]/span[2]')
            print("goods_price:",goods_price.text)
            goods_num = goods_num_choice.find_element(By.XPATH,'td[3]')
            print("goods_num:",goods_num.text)
            if(i==0):
                goods_all_price = goods_num_choice.find_element(By.XPATH,'td[5]/div/div[1]/p/strong/span[2]')
            with open("test.csv", 'a', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow([goods_name.text,goods_choice,goods_num.text,goods_price.text,goods_business_name.text,goods_order_id.text,goods_all_price.text,goods_data.text])
                # writer.
    except Exception as ex:
        print(ex)

# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[1]/td[2]/div/p[2]/span[2]
# //*[@id="tp-bought-root"]/div[5]/div/table/tbody[2]/tr[1]/td[2]/div/p/span[2]
# //*[@id="tp-bought-root"]/div[6]/div/table/tbody[2]/tr[1]/td[2]/div/p/span[2]
# //*[@id="tp-bought-root"]/div[7]/div/table/tbody[2]/tr[1]/td[2]/div/p[2]/span[2]
time.sleep(500)


# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[1]/tr/td[1]/label/span[2]      日期
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[1]/tr/td[1]/span/span[3]       订单号
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[1]/tr/td[2]/span/a             商家名称
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[1]/td[1]/div/div[2]/p[1]/a[1]/span[2]      第一个商品名称
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[1]/td[1]/div/div[2]/p[2]/span/span[1]      第一个商品套餐选择
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[1]/td[2]/div/p[2]                          第一个商品金额
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[1]/td[3]/div/p                             第一个商品数量
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[1]/td[5]/div/div[1]/p/strong/span[2]       总金额

# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[2]/td[1]/div/div[2]/p[1]/a[1]/span[2]      第二个商品名称

# //*[@id="tp-bought-root"]/div[5]/div/table/tbody[1]/tr/td[1]/label/span[2]
# //*[@id="tp-bought-root"]/div[5]/div/table/tbody[1]/tr/td[1]/span/span[3]
# //*[@id="tp-bought-root"]/div[5]/div/table/tbody[2]/tr[1]/td[1]/div/div[2]/p[1]/a[1]/span[2]

