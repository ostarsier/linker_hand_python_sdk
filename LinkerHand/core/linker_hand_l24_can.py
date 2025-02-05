#!/usr/bin/env python3
import can
import time,sys,os
import threading
import numpy as np
from enum import Enum

class FrameProperty(Enum):
    INVALID_FRAME_PROPERTY = 0x00  # 无效的can帧属性 | 无返回
    # 并行指令区域
    ROLL_POS = 0x01  # 横滚关节位置 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度
    YAW_POS = 0x02  # 航向关节位置 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度
    ROOT1_POS = 0x03  # 指根1关节位置 | 最接近手掌的指根关节
    ROOT2_POS = 0x04  # 指根2关节位置 | 最接近手掌的指根关节
    ROOT3_POS = 0x05  # 指根3关节位置 | 最接近手掌的指根关节
    TIP_POS = 0x06  # 指尖关节位置 | 最接近手掌的指根关节

    ROLL_SPEED = 0x09  # 横滚关节速度 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度
    YAW_SPEED = 0x0A  # 航向关节速度 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度
    ROOT1_SPEED = 0x0B  # 指根1关节速度 | 最接近手掌的指根关节
    ROOT2_SPEED = 0x0C  # 指根2关节速度 | 最接近手掌的指根关节
    ROOT3_SPEED = 0x0D  # 指根3关节速度 | 最接近手掌的指根关节
    TIP_SPEED = 0x0E  # 指尖关节速度 | 最接近手掌的指根关节

    ROLL_TORQUE = 0x11  # 横滚关节扭矩 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度
    YAW_TORQUE = 0x12  # 航向关节扭矩 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度
    ROOT1_TORQUE = 0x13  # 指根1关节扭矩 | 最接近手掌的指根关节
    ROOT2_TORQUE = 0x14  # 指根2关节扭矩 | 最接近手掌的指根关节
    ROOT3_TORQUE = 0x15  # 指根3关节扭矩 | 最接近手掌的指根关节
    TIP_TORQUE = 0x16  # 指尖关节扭矩 | 最接近手掌的指根关节

    ROLL_FAULT = 0x19  # 横滚关节故障码 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度
    YAW_FAULT = 0x1A  # 航向关节故障码 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度
    ROOT1_FAULT = 0x1B  # 指根1关节故障码 | 最接近手掌的指根关节
    ROOT2_FAULT = 0x1C  # 指根2关节故障码 | 最接近手掌的指根关节
    ROOT3_FAULT = 0x1D  # 指根3关节故障码 | 最接近手掌的指根关节
    TIP_FAULT = 0x1E  # 指尖关节故障码 | 最接近手掌的指根关节

    ROLL_TEMPERATURE = 0x21  # 横滚关节温度 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度
    YAW_TEMPERATURE = 0x22  # 航向关节温度 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度
    ROOT1_TEMPERATURE = 0x23  # 指根1关节温度 | 最接近手掌的指根关节
    ROOT2_TEMPERATURE = 0x24  # 指根2关节温度 | 最接近手掌的指根关节
    ROOT3_TEMPERATURE = 0x25  # 指根3关节温度 | 最接近手掌的指根关节
    TIP_TEMPERATURE = 0x26  # 指尖关节温度 | 最接近手掌的指根关节
    # 并行指令区域

    # 串行指令区域
    THUMB_POS = 0x41  # 大拇指指关节位置 | 返回本类型数据
    INDEX_POS = 0x42  # 食指关节位置 | 返回本类型数据
    MIDDLE_POS = 0x43  # 中指关节位置 | 返回本类型数据
    RING_POS = 0x44  # 无名指关节位置 | 返回本类型数据
    LITTLE_POS = 0x45  # 小拇指关节位置 | 返回本类型数据

    THUMB_SPEED = 0x29  # 大拇指速度 | 返回本类型数据
    INDEX_SPEED = 0x2A  # 食指速度 | 返回本类型数据
    MIDDLE_SPEED = 0x2B  # 中指速度 | 返回本类型数据
    RING_SPEED = 0x2C  # 无名指速度 | 返回本类型数据
    LITTLE_SPEED = 0x2D  # 小拇指速度 | 返回本类型数据

    THUMB_TORQUE = 0x51  # 大拇指扭矩 | 返回本类型数据
    INDEX_TORQUE = 0x52  # 食指扭矩 | 返回本类型数据
    MIDDLE_TORQUE = 0x53  # 中指扭矩 | 返回本类型数据
    RING_TORQUE = 0x54  # 无名指扭矩 | 返回本类型数据
    LITTLE_TORQUE = 0x55  # 小拇指扭矩 | 返回本类型数据

    THUMB_FAULT = 0x59  # 大拇指故障码 | 返回本类型数据
    INDEX_FAULT = 0x5A  # 食指故障码 | 返回本类型数据
    MIDDLE_FAULT = 0x5B  # 中指故障码 | 返回本类型数据
    RING_FAULT = 0x5C  # 无名指故障码 | 返回本类型数据
    LITTLE_FAULT = 0x5D  # 小拇指故障码 | 返回本类型数据

    THUMB_TEMPERATURE = 0x61  # 大拇指温度 | 返回本类型数据
    INDEX_TEMPERATURE = 0x62  # 食指温度 | 返回本类型数据
    MIDDLE_TEMPERATURE = 0x63  # 中指温度 | 返回本类型数据
    RING_TEMPERATURE = 0x64  # 无名指温度 | 返回本类型数据
    LITTLE_TEMPERATURE = 0x65  # 小拇指温度 | 返回本类型数据
    # 串行指令区域

    # 合并指令区域，同一手指非必要单控数据合并
    FINGER_SPEED = 0x81  # 手指速度 | 返回本类型数据
    FINGER_TORQUE = 0x82  # 转矩 | 返回本类型数据
    FINGER_FAULT = 0x83  # 手指故障码 | 返回本类型数据

    # 指尖传感器数据组
    HAND_NORMAL_FORCE = 0x90  # 五指法向压力
    HAND_TANGENTIAL_FORCE = 0x91  # 五指切向压力
    HAND_TANGENTIAL_FORCE_DIR = 0x92  # 五指切向方向
    HAND_APPROACH_INC = 0x93  # 五指接近感应

    THUMB_ALL_DATA = 0x98  # 大拇指所有数据
    INDEX_ALL_DATA = 0x99  # 食指所有数据
    MIDDLE_ALL_DATA = 0x9A  # 中指所有数据
    RING_ALL_DATA = 0x9B  # 无名指所有数据
    LITTLE_ALL_DATA = 0x9C  # 小拇指所有数据
    # 动作指令 ·ACTION
    ACTION_PLAY = 0xA0  # 动作

    # 配置命令·CONFIG
    HAND_UID = 0xC0  # 设备唯一标识码
    HAND_HARDWARE_VERSION = 0xC1  # 硬件版本
    HAND_SOFTWARE_VERSION = 0xC2  # 软件版本
    HAND_COMM_ID = 0xC3  # 设备id
    HAND_FACTORY_RESET = 0xCE  # 恢复出厂设置
    HAND_SAVE_PARAMETER = 0xCF  # 保存参数

    WHOLE_FRAME = 0xF0  # 整帧传输 | 返回一字节帧属性+整个结构体485及网络传输专属

class LinkerHandL20Can:
    def __init__(self, config, can_channel='can0', baudrate=1000000, can_id=0x28):
        self.config = config
        self.can_id = can_id
        self.running = True
        self.x01, self.x02, self.x03, self.x04,self.x05,self.x06,self.x07, self.x08,self.x09,self.x0A,self.x0B,self.x0C,self.x0D,self.x0E,self.speed = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        # 根据操作系统初始化 CAN 总线
        if sys.platform == "linux":
            self.bus = can.interface.Bus(
                channel=can_channel, interface="socketcan", bitrate=baudrate, 
                can_filters=[{"can_id": can_id, "can_mask": 0x7FF}]
            )
        elif sys.platform == "win32":
            self.bus = can.interface.Bus(
                channel='PCAN_USBBUS1', interface='pcan', bitrate=baudrate, 
                can_filters=[{"can_id": can_id, "can_mask": 0x7FF}]
            )
        else:
            raise EnvironmentError("Unsupported platform for CAN interface")

        # 根据 can_id 初始化 publisher 和相关参数
        if can_id == 0x28:  # 左手
            self.hand_exists = config['LINKER_HAND']['LEFT_HAND']['EXISTS']
            self.hand_joint = config['LINKER_HAND']['LEFT_HAND']['JOINT']
            self.hand_names = config['LINKER_HAND']['LEFT_HAND']['NAME']
        elif can_id == 0x27:  # 右手

            self.hand_exists = config['LINKER_HAND']['RIGHT_HAND']['EXISTS']
            self.hand_joint = config['LINKER_HAND']['RIGHT_HAND']['JOINT']
            self.hand_names = config['LINKER_HAND']['RIGHT_HAND']['NAME']


        # # 初始化数据存储
        # self.x01, self.x02, self.x03, self.x04 = [[0.0] * 5 for _ in range(4)]
        # self.normal_force, self.tangential_force, self.tangential_force_dir, self.approach_inc = \
        #     [[0.0] * 5 for _ in range(4)]

        # 启动接收线程
        self.receive_thread = threading.Thread(target=self.receive_response)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def send_command(self, frame_property, data_list):
        """
        发送命令到 CAN 总线
        :param frame_property: 数据帧属性
        :param data_list: 数据载荷
        """
        frame_property_value = int(frame_property.value) if hasattr(frame_property, 'value') else frame_property
        data = [frame_property_value] + [int(val) for val in data_list]
        msg = can.Message(arbitration_id=self.can_id, data=data, is_extended_id=False)
        try:
            self.bus.send(msg)
            print(f"Message sent: ID={hex(self.can_id)}, Data={data}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def receive_response(self):
        """
        接收并处理 CAN 总线的响应消息
        """
        while self.running:
            try:
                msg = self.bus.recv(timeout=1.0)  # 阻塞接收，1 秒超时
                if msg:
                    self.process_response(msg)
            except can.CanError as e:
                print(f"Error receiving message: {e}")

    # def set_finger_base(self, angles):
    #     self.send_command(FrameProperty.JOINT_PITCH_R, angles)

    # def set_finger_tip(self, angles):
    #     self.send_command(FrameProperty.JOINT_TIP_R, angles)

    # def set_finger_middle(self, angles):
    #     self.send_command(0x04, angles)

    # def set_thumb_roll(self, angle):
    #     self.send_command(FrameProperty.JOINT_ROLL_R, angle)

    def send_command(self, frame_property, data_list):
        frame_property_value = int(frame_property.value) if hasattr(frame_property, 'value') else frame_property
        data = [frame_property_value] + [int(val) for val in data_list]
        
        msg = can.Message(arbitration_id=self.can_id, data=data, is_extended_id=False)
        try:
            self.bus.send(msg)
        except can.CanError:
            print("Message NOT sent")
        time.sleep(0.002)
    
    def set_01(self, angles):
        # print("_-"*20)
        # print("set_01")
        # print(angles)
        self.send_command(0x01, angles)
        
    def set_02(self, angles):
        # print("_-"*20)
        # print("set_02")
        # print(angles)
        self.send_command(0x02, angles)

    def set_03(self, angles):
        # print("_-"*20)
        # print("set_03")
        # print(angles)
        self.send_command(0x03, angles)

    def set_04(self, angles):
        # print("_-"*20)
        # print("set_04")
        # print(angles)
        self.send_command(0x04, angles)

    def set_05(self, angles):
        # print("_-"*20)
        # print("set_05")
        # print(angles)
        self.send_command(0x05, angles)
    def set_06(self, angles):
        # print("_-"*20)
        # print("set_06")
        # print(angles)
        self.send_command(0x06, angles)
    def set_speed(self, speed):
        self.speed = [0,0,0,0,0]
        self.send_command(0x41, speed)
        # self.send_command(0x09, speed)
        # self.send_command(0x0A, speed)
        # self.send_command(0x0B, speed)
        # self.send_command(0x0C, speed)
        # self.send_command(0x0D, speed)
        # self.send_command(0x0E, speed)
    def set_finger_torque(self, torque):
        self.send_command(0x42, torque)

    def request_device_info(self):
        self.send_command(0xC0, [0])
        self.send_command(0xC1, [0])
        self.send_command(0xC2, [0])

    def save_parameters(self):
        self.send_command(0xCF, [])
    def process_response(self, msg):
        if msg.arbitration_id == self.can_id:
            frame_type = msg.data[0]
            response_data = msg.data[1:]
            if frame_type == 0x01:
                self.x01 = list(response_data)
            elif frame_type == 0x02:
                self.x02 = list(response_data)
            elif frame_type == 0x03:
                self.x03 = list(response_data)
            elif frame_type == 0x04:
                self.x04 = list(response_data)
            elif frame_type == 0x05:
                self.x05 = list(response_data)
            elif frame_type == 0x06:
                self.x06 = list(response_data)
            elif frame_type == 0xC0:
                print(f"Device ID info: {response_data}")
                if self.can_id == 0x28:
                    self.right_hand_info = response_data
                elif self.can_id == 0x27:
                    self.left_hand_info = response_data
            elif frame_type == 0x08:
                self.x08 = list(response_data)
            elif frame_type == 0x09:
                self.x09 = list(response_data)
            elif frame_type == 0x0A:
                self.x0A = list(response_data)
            elif frame_type == 0x0B:
                self.x0B = list(response_data)
            elif frame_type == 0x0C:
                self.x0C = list(response_data)
            elif frame_type == 0x0D:
                self.x0D = list(response_data)
            elif frame_type == 0x22:
                #ColorMsg(msg=f"五指切向压力方向：{list(response_data)}")
                d = list(response_data)
                self.tangential_force_dir = [float(i) for i in d]
            elif frame_type == 0x23:
                #ColorMsg(msg=f"五指接近度：{list(response_data)}")
                d = list(response_data)
                self.approach_inc = [float(i) for i in d]
            elif frame_type == 0x41:
                self.speed = list(response_data)
            elif frame_type == 0x42:
                self.finger_torque = list(response_data)

    def get_current_status(self):
        print(self.x02)
        return self.x01, self.x02, self.x03, self.x04, self.x05, self.x06
    
    def get_speed(self):
        #self.send_command(0x41, [0])
        return self.speed
        # self.send_command(0x09, [0])
        # self.send_command(0x0A, [0])
        # self.send_command(0x0B, [0])
        # self.send_command(0x0C, [0])
        # self.send_command(0x0D, [0])
        # self.send_command(0x0E, [0])
        # return self.x09+self.x0A+self.x0B+self.x0C+self.x0D+self.x0E
    def get_finger_torque(self):
        return self.finger_torque
    # def get_current(self):
    #     return self.x06
    # def get_fault(self):
    #     return self.x07
    def close_can_interface(self):
        if self.bus:
            self.bus.shutdown()  # 关闭 CAN 总线