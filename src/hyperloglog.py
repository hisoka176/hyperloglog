#encoding=utf-8
from __future__ import division
import sys
reload(sys)

import math
sys.setdefaultencoding('utf-8')
import random
# hyperloglog 实现
class HLL(object):
    # 初始化对象
    # self.log2m
    # self.register_num 桶的个数
    # self.content 各个桶存储的数据
    # self.alpha_value 计算E的系数，不同桶的个数，系数也不同，通常桶的个数有2^4,2^5,2^6个

    def __init__(self,log2m=6,regwidth=5):
        self.log2m = log2m
        self.register_num = 2**self.log2m
        self.regwidth = regwidth
        self.content = [0]*(2**self.log2m)
        self.alpha_value = self.alpha()
    # 计算E的系数
    def alpha(self):
        if self.log2m == 4:
            alpha_value = 0.673 * self.register_num*self.register_num
        elif self.log2m == 5:
            alpha_value = 0.697 * self.register_num*self.register_num
        elif self.log2m == 6:
            alpha_value = 0.709 * self.register_num*self.register_num
        else:
            alpha_value = (0.7213 / (1.0 + 1.079 / self.register_num)) * self.register_num * self.register_num
        return alpha_value
    # 返回bits第一个1的位置
    def position(self,x):
        x = x >> self.log2m
        pos = 0
        lenght = 32- self.log2m
        for i in range(lenght):
            pos += 1
            result = x & 1
            x = x>>1
            if result == 1:
                return pos
        
        return lenght
    # 计算桶的索引
    def cluster(self,x):
        mask = (1 << self.log2m) -1 
        x = x & mask
       
                
        return x 
    # 添加数据的入口，list_data为很多数据的集合
    def main(self,list_data):
        listdata = [abs(hash(x)) for x in list_data]
        for i in listdata:
            cluster_ind = self.cluster(i)  
            self.content[cluster_ind] = max(self.position(i),self.content[cluster_ind])
        
    # 返回估计的基数个数 
    def emister(self,value,v):
        if value <= 2.5*self.register_num:
            return self.register_num*math.log((self.register_num+0.0)/v,2)
        elif value <= 2**32/30:
            return value
        else:
            return -2**32*math.log(1-value/2**32,2)
    # 计算E的大小
    def count(self):
        total = 0.0
        num = 0.0
        for i in self.content:
            if i == 0:
                num += 1
 
            total += 2**(-i)
        
        total = self.alpha()/total
   
        return math.ceil(self.emister(total, v=num))
        
if __name__=='__main__':
    # 做了10次测试，1000为实际基础，可以重新设定
    for j in range(10):
        a = HLL(8,4)
        a.main([''+str(random.random()) for i in range(1000)])
        string = "第%d次,占实际基数百分比：%f" % (j,a.count()/1000)
        print(string.decode('utf-8').encode('utf-8'))