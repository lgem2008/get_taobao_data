# 爬取淘宝订单
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
import xlwt
import csv
import datetime

#---------------------------------------------------------#
# tb_name:      淘宝的账号
# tb_password:  淘宝账号的密码
#---------------------------------------------------------#
tb_name = ''
tb_password = ''
#---------------------------------------------------------#
# get_data_start_num: 开始访问的订单编号 --> 起始编号默认为4
# get_data_total_num: 需要访问的订单数量
#---------------------------------------------------------#
get_data_start_num = 4
get_data_total_num = 10
#---------------------------------------------------------#
# csv: csv导出的路径
#---------------------------------------------------------#
csv_save_path = r"tb_data.csv"
#---------------------------------------------------------#

start_time = datetime.datetime.now()

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
print("开始登录网站...")
driver.get('https://taobao.com')
print("点击我的淘宝...")
driver.find_element(By.XPATH, '//*[@id="J_SiteNavMytaobao"]/div[1]/a/span').click()
print("开始登录账号...")
driver.find_element(By.XPATH, '//*[@id="fm-login-id"]').send_keys(tb_name) 
driver.find_element(By.XPATH, '//*[@id="fm-login-password"]').send_keys(tb_password)
driver.find_element(By.XPATH, '//*[@id="login-form"]/div[4]/button').click()
print("点击已买到的宝贝...")
driver.find_element(By.XPATH, '//*[@id="bought"]').click()

print("开始创建csv...")
table_heads = ['商家名称','商品名称','商品套餐','商品数量','商品价格','总价格','购买日期','订单号']
with open(csv_save_path, 'a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(table_heads)

print("开始获取整个表格数据...")   
dataView_info = driver.find_element(By.XPATH, '//*[@id="tp-bought-root"]')
for num in range(get_data_start_num,get_data_start_num+get_data_total_num):
    try:
        print("将获取第"+str(num-3)+"个商家到第"+str(get_data_start_num-3+get_data_total_num)+"个商家的订单数据")
        table_xpath = 'div[' + str(num) + ']'
        print("开始获取第"+str(num-3)+"个商家的全部信息...")
        table1 = dataView_info.find_element(By.XPATH,table_xpath)   #第一个商家的物品

        print("开始获取第"+str(num-3)+"个商家的全部信息的表头...")
        tbody1 = table1.find_element(By.XPATH,'div/table/tbody[1]') #表头
        # print(tbody1.text)
        goods_data = tbody1.find_element(By.XPATH,'tr/td[1]/label') #日期
        goods_order_id = tbody1.find_element(By.XPATH,'tr/td[1]/span/span[3]')  #订单号
        goods_business_name = tbody1.find_element(By.XPATH,'tr/td[2]')  #商家名称

        print("开始获取第"+str(get_data_start_num-3)+"个商家的全部信息的商品数据...")
        tbody2 = table1.find_element(By.XPATH,'div/table/tbody[2]')
        rows = tbody2.find_elements(By.TAG_NAME,'tr')   #查找每个表格中的行数
        before_add_numbers = len(rows)
        

        for i in range(before_add_numbers):
            goods_num_choice_xpath = "tr["+str(i+1)+"]"
            goods_num_choice = tbody2.find_element(By.XPATH,goods_num_choice_xpath)
            goods_name = goods_num_choice.find_element(By.XPATH,'td[1]/div/div[2]/p[1]/a[1]/span[2]')   #商品名称
            print("购买第"+str(num+1-4)+"个商家("+goods_business_name.text+")的第"+str(i+1)+"商品为: "+goods_name.text)

            k = goods_num_choice.find_element(By.XPATH,'td[1]/div/div[2]')  
            goods_choice_num = len(k.find_elements(By.TAG_NAME,'p'))

            if(goods_choice_num == 4):
                goods_choice = goods_num_choice.find_element(By.XPATH,'td[1]/div/div[2]/p[2]/span/span[3]').text    #商品套餐选择
            elif(goods_choice_num == 3):#存在没有套餐选择的可能性
                try:
                    goods_choice = goods_num_choice.find_element(By.XPATH,'td[1]/div/div[2]/p[2]/span/span[3]').text    #商品套餐选择
                except:
                    goods_choice = ''
            elif(goods_choice_num == 2):#存在没有套餐选择的可能性
                goods_choice = ''

            kk = goods_num_choice.find_element(By.XPATH,'td[2]/div')  
            goods_price_num = len(kk.find_elements(By.TAG_NAME,'p'))

            if(goods_price_num == 1):   #没有优惠,所以只有一个价格
                goods_price = goods_num_choice.find_element(By.XPATH,'td[2]/div/p/span[2]')
            elif(goods_price_num == 2): #存在优惠,所以有两个价格=原价+折后价
                goods_price = goods_num_choice.find_element(By.XPATH,'td[2]/div/p[2]/span[2]')

            goods_num = goods_num_choice.find_element(By.XPATH,'td[3]') #商品的数量
            if(i==0):   #商家名称,订单号,总价,购买时间只需要记录一次
                goods_all_price = goods_num_choice.find_element(By.XPATH,'td[5]/div/div[1]/p/strong/span[2]')
                with open(csv_save_path, 'a', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow([goods_business_name.text,goods_name.text,goods_choice,goods_num.text,goods_price.text,goods_all_price.text,goods_data.text,goods_order_id.text])
            else: 
                with open(csv_save_path, 'a', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow(['',goods_name.text,goods_choice,goods_num.text,goods_price.text])

        print("=====================================================================================================")
        print("购买第"+str(num+1-4)+"个商家("+goods_business_name.text+")的商品数量为: "+str(before_add_numbers))
        print("购买第"+str(num+1-4)+"个商家("+goods_business_name.text+")的总金额为  : "+goods_all_price.text)
        print("=====================================================================================================")
        with open(csv_save_path, 'a', newline='', encoding='utf-8-sig') as file:    #每个商家之间空两行来帮助识别
            writer = csv.writer(file)
            writer.writerow('')
            writer.writerow('')
    except Exception as ex:
        print(ex)

driver.close()
end_time = datetime.datetime.now()

print("爬取结束,总用时：",str(end_time-start_time),"s")
print("=====================================================================================================")
