import math
from ClassModel import Model
import auxiliaryfunction as aux
#基本颗粒单元，球类
class Element:
    """为了DEM可以准确地模拟粒子的动力学行为，应当明确定义于粒子接触相关的输入参数,一般来说，输入参数分为两种类型：
        1.材料属性：密度，颗粒形状，粒径，剪切模量，泊松比等等
        2.交互参数：恢复系数，静摩擦系数和滚动膜材系数，还可能包括依赖于接触模型的塑性或粘性阻尼和黏附系数。
    """
    # 首先声明要用到的各物理类型变量
    # 值得注意的是这里定义的都死静态成员变量，属于类的属性，所有小球对象公用的属性，
    # 包括质量（密度），转动惯量，法向接触力弹性系数，切向接触力弹性系数，接触力，等等
    total_number = 20
    Kn = 0  # 法向刚度
    Kc = 0  # 切向刚度
    Ft = 0  # 切向接触力
    Fc = 0  # 接触力
    m = 1  # 质量 
    I = 1  # 转动惯量
    r = 0.001  # 小球半径（单位 m）

    # 常值变量，包括圆周率，重力场，时间步长等等
    PI = math.pi
    gravity = 9.8
    delta_time = 1e-3

    # 材料参数
    rho = 2500
    vc = 0.2  # 泊松比
    Gc = 1.2 * 1e4  # 剪切模量
    def __init__(self, number, coord_x, coord_y,coord_z,velx,vely,velz,omega_x,omega_y,omega_z):
        # 坐标,我们所唯一关注的小球的属性，最终就是需要更新这个
        self.m_x = coord_x  # x坐标初始化
        self.m_y = coord_y  #y坐标初始化
        self.m_z = coord_z  #z坐标初始化
        self.m_positon = [self.m_x,self.m_y,self.m_z]
        #后面计算要用到的小球的基本固有属性，比如：遍历时候需要的编号看，质量，惯量，半径
        self.m_number = number  # 单元的编号初始化
        self.m_mass = Element.m  # 单元的质量初始化
        self.m_moment = Element.I  # 单元的转动惯量初始化
        self.m_r = Element.r  # 圆半径
        #后面计算要用到的小球的运动属性，每次迭代后都会变化，比如：速度，转动角速度
            #速度部分
        self.m_velx = velx  # x平动速度初始化
        self.m_vely = vely  # y平动速度初始化
        self.m_velz = velz  # z平动速度
        self.m_velocity = [self.m_velx,self.m_vely,self.m_velz] #速度向量形式
        self.m_omegax = omega_x    # x转动速度初始化
        self.m_omegay = omega_y    # y转动速度初始化
        self.m_omegaz = omega_z    # z转动速度初始化
        self.m_omega = [self.m_omegax,self.m_omegay,self.m_omegaz]  # 单元转动速度初始化
        
        # 小球应该有一个属性，用来存储所有其他小球对其施加的力，并且其生命周期必须跨越完整的程序
        # 因为下一时刻两个小球之间的接触力的处理涉及到上一时刻的两个小球间的接触力
        # （注：也许可以改良成不断更新小球收到的合力而不是 每次更新小球间的接触力）
        self.force_of_other = [[[0,0,Element.gravity],[0,0,Element.gravity]]]
        for i in range(Element.total_number-1):
            self.force_of_other.append([[0,0,Element.gravity],[0,0,Element.gravity]])
        self.torque_of_other = [[0,0,0]]
        for i in range(Element.total_number-1):  #力矩
            self.torque_of_other.append([0,0,0])
        #受力部分x和y方向和合力及合力矩,用来计算加速度
        self.m_Fxsum = 0    #x方向合力
        self.m_Fysum = 0    #y方向合力
        self.m_Fzsum = Element.gravity    #z方向合力
        self.m_Fsum = [0,0,Element.gravity]
        self.m_Txsum  = 0    #x方向合力
        self.m_Tysum  = 0    #y方向合力
        self.m_Tzsum  = 0    #z方向 
        self.m_Tsum = [0,0,0]
        # 材料参数？？
        self.type = 1 #颗粒材料类型，1代表一种材料
        self.m_young = 0  # 弹性模量
        self.m_possion = 0  # 泊松比
        self.m_weight = 0  # 单元容重
    #CalContactForce应该传入self，施力小球particle_2,以及接触模型
    #CalContactForce应该能够按要求计算不同类型接触力，并且将力和反作用力存储到受力对象和施力对象
    def CalContactForce(self,particle_2,model):
        #先定义计算接触力需要用到的一些量
        dist_mutually = 0  # 颗粒间球心间绝对距离
        sum_radius = 0  # 半径之和
        delta_x_n = [0,0,0]  # 法向位移增量
        delta_x_c = [0,0,0]  # 切向位移增量
        delta_f_n = 0  # 法向力增量
        delta_f_c = 0  # 切向力增量
        
        # 计算球心间距，球心单位法向量（从受力球指向施力球)
        dist_12 = [0,0,0]  #存储x,y,z坐标间距
        dist_12[0] = particle_2.m_x - self.m_x
        dist_12[1] = particle_2.m_y - self.m_y
        dist_12[2] = particle_2.m_z - self.m_z
        dist_mutually = aux.VectorMagnitude(dist_12)
        vector_n = aux.VectorDirecton(dist_12) # 单位化为法向量
        
        #通过计算相对位移增量来计算法向相对位移增量
        relative_disp_increment = [0,0,0]    #相对位移增量向量
        relative_disp_increment[0] = (particle_2.m_velx - self.m_velx) * Element.delta_time
        relative_disp_increment[1] = (particle_2.m_vely - self.m_vely) * Element.delta_time
        relative_disp_increment[2] = (particle_2.m_velz - self.m_velz) * Element.delta_time
        #法向相对位移，这里就是相对位移点乘法向量n，单位法向量就是球心连线的方向，n = （cos_theta,sin_theta)，而切向的单位向量就是t=（-sin_theta，cos_theta）
        delta_x_n = aux.multiply_list_by_float(vector_n,aux.DotProduct(relative_disp_increment,vector_n))
        
        #通过计算相对角位移增量来计算相对切向位移的旋转部分
        relative_angle_increment = [0,0,0]    #相对角位移增量向量 (omega_A x r_A +  omega_B x r_B) * delta_time
        relative_angle_increment[0] = (aux.CrossProduct(self.m_omega,vector_n)[0] * self.m_r +aux.CrossProduct(particle_2.m_omega,vector_n)[0] * particle_2.m_r) * Element.delta_time
        relative_angle_increment[1] = (aux.CrossProduct(self.m_omega,vector_n)[1] * self.m_r +aux.CrossProduct(particle_2.m_omega,vector_n)[0] * particle_2.m_r) * Element.delta_time
        relative_angle_increment[2] = (aux.CrossProduct(self.m_omega,vector_n)[2] * self.m_r +aux.CrossProduct(particle_2.m_omega,vector_n)[0] * particle_2.m_r) * Element.delta_time
        #相对切向位移增量 = 相对位移在点乘切向方向向量 - 半径乘以相对旋转角量
        a = [self.m_velx * Element.delta_time,self.m_vely * Element.delta_time,self.m_velz * Element.delta_time]
        delta_x_c = relative_disp_increment = aux.SubtractLists(aux.SubtractLists(a,delta_x_n),relative_angle_increment)
        # print(len(delta_x_n))
        # print(len(relative_angle_increment))
        # print(len(delta_x_c))
        #计算接触力之前先判断接触类型
        #model_type = Model(self,particle_2).TypeChecking()
        model_type = model.TypeChecking()

        if model_type == 1: # 如果是线性弹簧模型则按照线性弹簧模型计算 
            #更新法向力和切向力，从而得到接触力大小(线性弹簧模型)
            delta_f_n = Element.Kn * aux.VectorMagnitude(delta_x_n)  #法向接触力增量大小
            delta_f_c = Element.Kc * aux.VectorMagnitude(delta_x_c)    #切向接触力增量大小            
            #更新切向接触力的方向
            #首先旋转接触平面的单位法向量
            #旋转量等于（（velocity2 - velocity1）x n )* delta_time
            # print(self.m_velx)
            # c = [self.m_velx,self.m_vely,self.m_velz]
            # print(c)
            # print(self.m_velocity)
            # print([self.m_x,self.m_y,self.m_z])
            # print([particle_2.m_x,particle_2.m_y,particle_2.m_z])

            # print(particle_2.m_velocity)
            # print(vector_n)
            # print(aux.SubtractLists(particle_2.m_velocity , self.m_velocity))
            
            # print(aux.CrossProduct(vector_n,(aux.SubtractLists(particle_2.m_velocity , self.m_velocity))))
            # print(aux.multiply_list_by_float(aux.CrossProduct(vector_n,(aux.SubtractLists(particle_2.m_velocity , self.m_velocity))),Element.delta_time))
            planar_rotation = aux.multiply_list_by_float(aux.multiply_list_by_float(aux.CrossProduct(vector_n,(aux.SubtractLists(particle_2.m_velocity , self.m_velocity))),Element.delta_time),1/dist_mutually)
            #更新两个小球间切向接触力的方向
            self.force_of_other[particle_2.m_number][1] =aux.AddLists(self.force_of_other[particle_2.m_number][1] , aux.CrossProduct(planar_rotation,self.force_of_other[particle_2.m_number][1]))
            #得到真正的更新后的切向接触力
            magnitude = aux.VectorMagnitude(self.force_of_other[particle_2.m_number][1]) + delta_f_c
            direction = aux.VectorDirecton(self.force_of_other[particle_2.m_number][1])
            self.force_of_other[particle_2.m_number][1] = aux.multiply_list_by_float(direction,magnitude)
            
            #更新法向接触力
            magnitude = aux.VectorMagnitude(self.force_of_other[particle_2.m_number][0]) + delta_f_n
            direction = vector_n
            self.force_of_other[particle_2.m_number][0] = aux.multiply_list_by_float(direction,magnitude)
            #计算接触合力
            conact_force = aux.AddLists(self.force_of_other[particle_2.m_number][0] , self.force_of_other[particle_2.m_number][1])
            #更新力矩
            self.torque_of_other[particle_2.m_number] = aux.CrossProduct((aux.multiply_list_by_float(vector_n,self.m_r)),conact_force)
            
            #更新相互作用力
            particle_2.force_of_other[self.m_number][0] = aux.SubtractLists(particle_2.force_of_other[self.m_number][0] ,self.force_of_other[particle_2.m_number][0])
            particle_2.force_of_other[self.m_number][1] = aux.SubtractLists(particle_2.force_of_other[self.m_number][1] ,self.force_of_other[particle_2.m_number][1])

            #更新相互作用力矩
            particle_2.torque_of_other[self.m_number] = aux.SubtractLists(particle_2.torque_of_other[self.m_number] ,self.torque_of_other[particle_2.m_number])
        
        else:   #其他接触模型的计算，待完善
            pass
    #此时两个小球间的接触力和接触力矩已经存入到了小球的force_of_other属性和torque_of_other属性的particle2.number的位置
        
    #定义函数将force_of_other属性中的计算的接触力和接触力矩交给此刻聚焦分析的小球的合外力和和合外力矩属性
    #为最后求加速度和角加速度做好准备
    def CombinedF(self):
        for force_list in self.force_of_other:
            for force in force_list:
                self.m_Fxsum += force[0] + force[0]
                self.m_Fysum += force[1] + force[1]
                self.m_Fzsum += force[2] + force[2]
                self.m_Fsum += [self.m_Fxsum,self.m_Fysum,self.m_Fzsum]
    def CombinedTorque(self):
        for torque in self.torque_of_other:
                self.m_Txsum += torque[0] + torque[0]
                self.m_Tysum += torque[1] + torque[1]
                self.m_Tzsum += torque[2] + torque[2]
                self.m_Tsum += [self.m_Txsum,self.m_Tysum,self.m_Tzsum]
    #对方小球是反作用力也可在这里更新
    def Interaction_force(self,particle_2):
            particle_2.force_of_other[self.m_number] += -self.force_of_other[particle_2.m_number]
            
    def Interaction_torque(self,particle_2):
            particle_2.torque_of_other[self.m_number] += -self.torque_of_other[particle_2.m_number]

