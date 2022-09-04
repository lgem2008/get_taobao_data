#csv 测试代码
import csv
import codecs
# data = {"The num of the goods: 14
# goods_name: 黑色8.8级垫片平垫圈金属垫圈加厚螺丝平垫片超薄介子圆形M2-M30
# goods_choice: 颜色分类
# goods_price: ￥3.11
# goods_num: 1"}

with open("test.csv", 'a', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['你','fhj'])

# with codecs.open("test.csv","a",'utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames="test.csv")
#     writer.writeheader()
#     writer.writerow('你')