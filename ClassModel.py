"""
CalContactForce函数应该需要计算不同种类的接触模型,
定义Model类是为了与CalContactForce通信,操作CalContactForce函数实现相应功能,
这个类的对象需要传递给CalContactForce函数信息,告知函数需要按照哪条路径计算接触力
这个类的对象应该返回模型列表model_list特定位置的元素即相应类型的接触模型。
"""
class Model:
    def __init__(self,paticle_1,particle_2):#也许将来需要加上contactparameter形参
        self.particle_1 = paticle_1
        self.particle_2 = particle_2
    # 定义model_type是一个自然数,它用来顺序表示不同模型,这里第一个模型是线性弹簧
        self.model_type = 1 #初始化为1,默认是线性弹簧
    # 如果是弹簧model_type设置为1
    def TypeChecking(self):
        # if语句检查两个颗粒间接触模型是否为线性弹簧（通过两个颗粒间的信息来判断）
        if self.particle_1.type == 1  and self.particle_2.type == 1:
            self.model_type = 1 
        else:
            pass#待完善其他模型
        return self.model_type