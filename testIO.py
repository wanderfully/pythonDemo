

import os
# with open('boom.txt','r') as f:
#     print(f.read())

# with open('boom.txt','w') as f:
#     f.write('这是写入的数据！')
def mkdir(path):
   nowpath = os.getcwd()
   print('现在的路劲为：',nowpath)
   fileName = '文件夹yi'
   fileNamePath = nowpath+path
   os.makedirs(fileNamePath)

mkdir('\mzitu\data\mints')