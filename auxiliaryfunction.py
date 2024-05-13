import math
import random
#计算向量模长，点乘，叉乘等数值

# VectorMagnitude函数用来计算向量模长
def VectorMagnitude(v):
    magnitude = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    return magnitude
#取出向量的单位方向向量
def VectorDirecton(v):
    lenth = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if lenth == 0:
        print("0 can not become a divison")
    direx = v[0]/lenth
    direy = v[1]/lenth
    direz = v[2]/lenth
    list = [direx,direy,direz]  #用列表来存储方向向量
    return list
def DotProduct(v1, v2):  
    # 确保两个列表长度相同，即向量维度相同  
    assert len(v1) == 3 and len(v2) == 3
      
    # 计算点乘  
    return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
def CrossProduct(v1, v2):  
    # 确保传入的列表长度为3，即三维向量  
    assert len(v1) == 3 and len(v2) == 3    
    # 根据叉乘公式计算各个分量  
    Cx = v1[1] * v2[2] - v1[2] * v2[1]  
    Cy = v1[2] * v2[0] - v1[0] * v2[2]  
    Cz = v1[0] * v2[1] - v1[1] * v2[0]       
    # 返回一个包含三个分量的列表，代表叉乘的结果向量 
    list = [Cx, Cy, Cz]
    return list

#生成小球很棘手，这里只考虑等距均匀居中分布生成
def Generating_coordinate(total_number,domain,r):
    
    start_x = domain.center_coord[0] - domain.wide / 2 + r
    end_x = domain.center_coord[0] + domain.wide / 2 - r
    interval_x = (end_x- start_x)/ (total_number-1)
    
    start_y = domain.center_coord[1] - domain.long / 2 + r
    end_y = domain.center_coord[1] + domain.long / 2 - r
    interval_y = (end_y- start_y)/ (total_number-1)
    
    start_z = domain.center_coord[2] - domain.high / 2 + r
    end_z = domain.center_coord[2] + domain.high / 2 - r
    interval_z = (end_z- start_z)/ (total_number-1)
    list = []
    #先生成一列小球的x坐标listx[],
    for _ in range(total_number):
        listx = [start_x + i * interval_x for i in range(total_number)] 
    for _ in range(total_number):
        listy = [start_y + i*interval_y for i in range(total_number)]
    for _ in range(total_number):
            listz = [start_z + i*interval_z for i in range(total_number)]
    for index1 ,item1 in enumerate(listx):
        for index2 ,item2 in enumerate(listy):
                for index3 ,item3 in enumerate(listz):
                    #生成每个位置的坐标存放在list当中
                    list.append([listx[index1],listy[index2],listz[index3]])
    return list

#初始化所有小球的速度
def Generating_velocity(total_number):
    #x方向的速度,这里暂且都是一个随机速度吧
    # 生成一个包含随机浮点数的列表，每个浮点数在1.0到100.0之间，均匀分布 
    for i in range(total_number):
        listvelx = [random.uniform(1.0, 10.0) for _ in range(total_number)]
    #y方向的速度，也是随机数  
    for i in range(total_number):
        listvely = [random.uniform(1.0, 10.0) for _ in range(total_number)]  
    #z方向的速度，也是随机数
    for i in range(total_number):
        listvelz = [random.uniform(1.0, 10.0) for _ in range(total_number)]  
    return [listvelx,listvely,listvelz]

#初始化所有小球的角速度
def Generating_omega(total_number):
    #x方向的角速度,这里暂且都是一个随机速度吧
    # 生成一个包含随机浮点数的列表，每个浮点数在1.0到100.0之间，均匀分布 
    for i in range(total_number):
        listomegax = [random.uniform(1.0, 10.0) for _ in range(total_number)]
    #y方向的速度，也是随机数  
    for i in range(total_number):
        listomegay = [random.uniform(1.0, 10.0) for _ in range(total_number)]  
    #z方向的速度，也是随机数
    for i in range(total_number):
        listomegaz = [random.uniform(1.0, 10.0) for _ in range(total_number)]  
    return [listomegax,listomegay,listomegaz]

#计算列表减法
def AddLists(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Both lists must have the same length to perform element-wise addition.")
    
    result = [list1[i] + list2[i] for i in range(len(list1))]
    return result

def SubtractLists(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Both lists must have the same length to perform element-wise subtraction.")
    
    result = [list1[i] - list2[i] for i in range(len(list1))]
    return result

#浮点数和列表的乘法
def multiply_list_by_float(lst, float_value):
    """
    将列表中的每个元素乘以指定的浮点数，并返回新的列表。

    参数:
    lst (list): 包含数值的列表
    float_value (float): 要乘以列表元素的浮点数

    返回:
    list: 新的列表，其中每个元素都是原列表对应元素与浮点数相乘的结果
    """
    return [item * float_value for item in lst]
