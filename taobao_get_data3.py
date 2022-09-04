# 爬取淘宝订单
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
import xlwt
import csv

#---------------------------------------------------------
# tb_name:      淘宝的账号
# tb_password:  淘宝账号的密码
tb_name = ''
tb_password = ''
#---------------------------------------------------------
# get_data_start_num: 开始访问的订单编号 --> 其实编号默认为4
# get_data_total_num: 需要访问的订单数量
get_data_start_num = 4
get_data_total_num = 10
#---------------------------------------------------------
# csv: csv导出的路径
csv_save_path = r"test4.csv"
#---------------------------------------------------------

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
driver.get('https://taobao.com')
driver.find_element(By.XPATH, '//*[@id="J_SiteNavMytaobao"]/div[1]/a/span').click()

driver.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys(tb_name) 
driver.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys(tb_password)
driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button').click()

driver.find_element(By.XPATH, '//*[@id="bought"]').click()

time.sleep(0.2)
dataView_info = driver.find_element(By.XPATH, '//*[@id="tp-bought-root"]')
# print(dataView_info.text)
print("-----------------------1-----------------------")
table_heads = ['商家名称','商品名称','商品套餐','商品数量','商品价格','链接','订单号','总价格','购买日期']
with open(csv_save_path, 'a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(table_heads)

for num in range(get_data_start_num,get_data_start_num+get_data_total_num):
    try:
        table_xpath = 'div[' + str(num) + ']'
        # table1 = dataView_info.find_element(By.XPATH,'div[4]')          #第一个商家的物品
        table1 = dataView_info.find_element(By.XPATH,table_xpath)          #第一个商家的物品
        # print("=====================================")
        # print(table_xpath)
        # print("=====================================")
        # print(table1.text)

        tbody1 = table1.find_element(By.XPATH,'div/table/tbody[1]')#表头
        # print(tbody1.text)
        goods_data = tbody1.find_element(By.XPATH,'tr/td[1]/label')#日期
        print("goods_data",goods_data.text)
        goods_order_id = tbody1.find_element(By.XPATH,'tr/td[1]/span/span[3]')#订单号
        print("goods_order_id",goods_order_id.text)
        goods_business_name = tbody1.find_element(By.XPATH,'tr/td[2]')#商家名称
        print("goods_business_name",goods_business_name.text)
        # # //*[@id="tp-bought-root"]/div[4]/div/table/tbody[1]/tr/td[1]/label/span[2]      日期
        # # //*[@id="tp-bought-root"]/div[4]/div/table/tbody[1]/tr/td[1]/span/span[3]       订单号
        # # //*[@id="tp-bought-root"]/div[4]/div/table/tbody[1]/tr/td[2]/span/a             商家名称
        # //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr/td[1]/div/div[2]/p[1]/a

        tbody2 = table1.find_element(By.XPATH,'div/table/tbody[2]')
        # print(tbody2.text)
        print("-----------------------2-----------------------")

        rows = tbody2.find_elements(By.TAG_NAME,'tr')   #查找每个表格中的行数
        before_add_numbers = len(rows)
        print("rows:",before_add_numbers)
        print("-----------------------3-----------------------")

# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[1]/td[1]/div/div[2]/p[1]/a[1]/span[2]      第一个商品名称
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[1]/td[1]/div/div[2]/p[2]/span/span[1]      第一个商品套餐选择
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[1]/td[2]/div/p[2]                          第一个商品金额
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[1]/td[3]/div/p                             第一个商品数量
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[1]/td[5]/div/div[1]/p/strong/span[2]       总金额

        
# //*[@id="tp-bought-root"]/div[4]/div/table/tbody[2]/tr[2]/td[1]/div/div[2]/p[1]/a[1]/span[2]      第二个商品名称
        for i in range(before_add_numbers):
            print("The num of the goods:", i+1)
            goods_num_choice_xpath = "tr["+str(i+1)+"]"
            # print(goods_num_choice_xpath)
            
            goods_num_choice = tbody2.find_element(By.XPATH,goods_num_choice_xpath)
            goods_link = goods_num_choice.find_element(By.XPATH,'td[1]/div/div[2]/p[1]/a[1]').get_attribute('href') + '  '    #商品链接
            print("good_link: ",goods_link)
            goods_name = goods_num_choice.find_element(By.XPATH,'td[1]/div/div[2]/p[1]/a[1]/span[2]')   #商品名称
            print("goods_name:",goods_name.text)
            try:
                goods_choice = goods_num_choice.find_element(By.XPATH,'td[1]/div/div[2]/p[2]/span/span[3]').text    #商品套餐选择
                print("goods_choice:",goods_choice)
            except:
                goods_choice = ''   #存在没有套餐选择的可能性
                print("goods_choice:",goods_choice)

            goods_price_xpath = 'td[2]/div'
            k = goods_num_choice.find_element(By.XPATH,goods_price_xpath)
            a = k.find_elements(By.TAG_NAME,'p')   #查找每个表格中的行数
            goods_price_num = len(a)
            # print("----------------------------------------------")
            # print(goods_price_num)
            # print("----------------------------------------------")
            if(goods_price_num == 1):   #没有优惠,所以只有一个价格
                goods_price = goods_num_choice.find_element(By.XPATH,'td[2]/div/p/span[2]')
            elif(goods_price_num == 2): #存在优惠,所以有两个价格=原价+折后价
                goods_price = goods_num_choice.find_element(By.XPATH,'td[2]/div/p[2]/span[2]')
            print("goods_price:",goods_price.text)
            goods_num = goods_num_choice.find_element(By.XPATH,'td[3]') #商品的数量
            print("goods_num:",goods_num.text)
            if(i==0):   #商家名称,订单号,总价,购买时间只需要记录一次
                goods_all_price = goods_num_choice.find_element(By.XPATH,'td[5]/div/div[1]/p/strong/span[2]')
                with open(csv_save_path, 'a', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow([goods_business_name.text,goods_name.text,goods_choice,goods_num.text,goods_price.text,goods_link,goods_order_id.text,goods_all_price.text,goods_data.text])
            else: 
                with open(csv_save_path, 'a', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow(['',goods_name.text,goods_choice,goods_num.text,goods_price.text,goods_link])
        with open(csv_save_path, 'a', newline='', encoding='utf-8-sig') as file:    #每个商家之间空两行来帮助识别
            writer = csv.writer(file)
            writer.writerow('')
            writer.writerow('')
    except Exception as ex:
        print(ex)
print("爬取结束")


