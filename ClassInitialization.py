from ClassElement import Element
from ClassModel import Model 
from ClassDomain import Domain
import auxiliaryfunction as aux
#这个类用于计算每个时间步所有小球的受力分析
#计算之前需要判断是否触碰到边界，如果有得给出相应的处理
class Initialization:
    #类变量
    def __init__(self,listx,listy,listz,listvelx,listvely,listvelz,listoemgax,listoemgay,listoemgaz):
        #初始化单元列表,需要传入六个列表，每个列表都对应一列小球的某一个初始属性             #model_list = []     #创建接触模型列表，存储 对两两小球之间的模型类型的判断
        self.listx = listx
        self.listy = listy
        self.listz = listz
        self.listvelx = listvelx
        self.listvely = listvely
        self.listvelz = listvelz
        self.listomegax = listoemgax
        self.listomegay = listoemgay
        self.listomegaz = listoemgaz
        self.element_list = []   #创建单元列表，用来存储所有小球单元,调用方法完成初始化 
               
    def ElementListGnerate(self):
        #按照要求生成小球
        for i in range(Element.total_number):
            self.element_list.append(Element(i,self.listx[i], self.listy[i],self.listz[i],self.listvelx[i],self.listvely[i],self.listvelz[i],self.listomegax[i],self.listomegay[i],self.listomegaz[i]))
