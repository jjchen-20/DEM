import math
""" 计算区域是一个类,先考虑矩形区域并且接收从颗粒的相关信息，以处理颗粒与边界的碰撞，更新颗粒的速度
 三维维矩形需要传入6个参数,前3个是中心点的坐标,其余4个是矩形的长,宽,高"""
class Domain:
    def __init__(self,center_coord,long,wide,high):
        self.center_coord = center_coord #这里应该传入一个三维向量,代表矩形中心
        self.long = long
        self.wide = wide 
        self.high = high
        self.cuboid_vertices = self.calculate_rectangular_prism_vertices()
        self.normals = []
        self.plane_points = []  
        self.point_for_draw = [self.cuboid_vertices[4],self.cuboid_vertices[0],self.cuboid_vertices[1],self.cuboid_vertices[5],self.cuboid_vertices[6],self.cuboid_vertices[2],self.cuboid_vertices[3],self.cuboid_vertices[7]]
        # 前面和后面  ,0前左下,1前右下,2前左上 ,3前右上,4后左下,5后右下,6后左上,7后右上
        front_normal = self.compute_normal(self.cuboid_vertices[0], self.cuboid_vertices[1], self.cuboid_vertices[2])  
        back_normal = self.compute_normal(self.cuboid_vertices[4], self.cuboid_vertices[5], self.cuboid_vertices[6])  
        self.normals.extend([front_normal, back_normal])  # 后面法向量取反，因为方向是朝内的  
        self.plane_points.extend([self.cuboid_vertices[0], self.cuboid_vertices[4]])  
        
        # 顶面和底面  
        top_normal = self.compute_normal(self.cuboid_vertices[2], self.cuboid_vertices[3], self.cuboid_vertices[6])  
        bottom_normal = self.compute_normal(self.cuboid_vertices[0], self.cuboid_vertices[1], self.cuboid_vertices[4])  
        self.normals.extend([top_normal, bottom_normal])  # 底面法向量取反  
        self.plane_points.extend([self.cuboid_vertices[2], self.cuboid_vertices[4]])  
        
        # 左面和右面  
        left_normal = self.compute_normal(self.cuboid_vertices[0], self.cuboid_vertices[2], self.cuboid_vertices[4])  
        right_normal = self.compute_normal(self.cuboid_vertices[1], self.cuboid_vertices[3], self.cuboid_vertices[5])  
        self.normals.extend([left_normal, right_normal])  # 右面法向量取反  
        self.plane_points.extend([self.cuboid_vertices[0], self.cuboid_vertices[1]])  
        
        #此刻，normals列表已经存储了六个面的法向量，而self.plane_pointsy也存储了平面的代表点
        #依次是，前面，后面，顶面，底面，左面，右面
    def calculate_rectangular_prism_vertices(self):  
        x, y, z =  self.center_coord
        l, w, h = self.long / 2, self.wide / 2, self.high / 2  # 除以2,因为是从中心点到顶点的距离  

        # 计算六个顶点的坐标  
        vertex1 = (x + l, y - w, z - h)  # 前左下 顶点  
        vertex2 = (x + l, y + w, z - h)  # 前右下 顶点  
        vertex3 = (x + l, y - w, z + h)  # 前左上 顶点  
        vertex4 = (x + l, y + w, z + h)  # 前右上 顶点  
        vertex5 = (x - l, y - w, z - h)  # 后左下 顶点 
        vertex6 = (x - l, y + w, z - h)  # 后右下 顶点 
        vertex7 = (x - l, y - w, z + h)  # 后左上 顶点 
        vertex8 = (x - l, y + w, z + h)  # 后右上 顶点  
        # 0，1，2三个点应该是前左上 ，前左下，前右上。3应该是后右上，4，5，6三个点应该是后左下，后左上，后右下,7是前右下
        return  [vertex1, vertex2, vertex3, vertex4, vertex5, vertex6,vertex7,vertex8]
    #[vertex3, vertex1, vertex4, vertex8, vertex5, vertex7,vertex6,vertex2] 
       
        #计算法向量
    def compute_normal(self,v1, v2, v3):
        """计算由三个点定义的平面的法向量"""  
        u = [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]  
        v = [v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]]  
        normal = [u[1] * v[2] - u[2] * v[1],  
                u[2] * v[0] - u[0] * v[2],  
                u[0] * v[1] - u[1] * v[0]]  
        return normal
     
    #点到平面距离的计算,传入的都是三维向量
    def point_to_plane_distance(self,point, plane_point, normal):  
        """计算点到平面的距离"""  
        vec_to_plane = [a - b for a, b in zip(point, plane_point)]  
        return abs(sum(c * d for c, d in zip(vec_to_plane, normal))) / math.sqrt(sum(e * e for e in normal))  
    
    
    def rebound_sphere_from_cuboid(self, element):  
        """  
        计算小球与长方体相交的情况，并返回反弹后的小球中心位置。  
        :param self.cuboid_vertices: 长方体八个顶点的坐标列表，顺序为：(x1, y1, z1), (x2, y1, z1), ... (x2, y2, z2)  
        :param element.m_velocity: 小球中心的坐标 (x, y, z)  
        :param element.m_r: 小球的半径  
        :return: 反弹后的小球中心位置，如果没有相交则返回原位置  
        """
        Collision_situation = False          
        # 计算六个面的法向量和代表点  
        distance = []
        point =  [element.m_x,element.m_y,element.m_z]
        # 依次计算小球中心到各个面的距离并且存储到distance,一共六个
        for i, (normal, plane_point) in enumerate(zip(self.normals, self.plane_points)):  
            distance1 = self.point_to_plane_distance(point, plane_point, normal)  
            distance.append(distance1) 
     
        #把最小的距离h和对应的指标都存储出来
        min_distance = []
        min_index = []
        min_value = min(distance)
        for index,value in enumerate(distance):
            if value == min_value:
                min_distance.append(value)
                min_index.append(index)
        # 检查是否有相交
        for indx,(index,dist) in enumerate(zip(min_index,min_distance)):
            if dist < element.m_r:
                Collision_situation = True
                #判断是哪个面，对应速度处理
                if indx == 0:#撞到前面,y方向速度取反
                    element.m_velocity[0] = -element.m_velocity[0]
                elif indx == 1:#撞到了后面
                    element.m_velocity[0] = -element.m_velocity[0]
                elif indx == 2:#撞到了顶面
                    element.m_velocity[2] = -element.m_velocity[2]
                elif indx == 3:#撞到了底面
                    element.m_velocity[2] = -element.m_velocity[2]
                elif indx == 4:#撞到了左面
                    element.m_velocity[1] = -element.m_velocity[1]
                elif indx == 5:#撞到了右面
                     element.m_velocity[1] = -element.m_velocity[1]
            else:
                continue
        return Collision_situation