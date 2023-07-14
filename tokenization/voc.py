import json, re
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost", # 数据库主机地址
  user="root",    # 数据库用户名
  passwd="123456",   # 数据库密码
  database="wenshu" # 数据库名称
)

if mydb:
  print("数据库链接成功！")
  mycursor = mydb.cursor()
else:
  print("无法获取数据库链接！")

def process(sql_res):
  cases = []
  for i in sql_res:
    # 数据预处理
    desc = i[0].strip().replace(" ", "").replace("…","").replace("*", "x")
    desc = re.compile(r"\s+").sub("\n", desc)
    desc = re.compile(r"[×xX]+").sub("xxx", desc)
    if len(desc.split("\n")) > 2:
      cases.append(desc)
  with open("../dataset/criminal_case.json", "w", encoding="utf-8") as fo:
    fo.write(json.dumps(cases, ensure_ascii=False))

start = 0
end =2000
step = 2000
while start<end:
  sql = f"select 正文 from xingshi_wenshu where id>{start} and id<{start+step}"
  mycursor.execute(sql)
  result = mycursor.fetchall()
  process(result)
  start+=step
print("process end...")