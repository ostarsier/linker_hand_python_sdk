#!/usr/bin/env python3
import sys,os,time


current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(target_dir)

from LinkerHand.utils.color_msg import ColorMsg
from LinkerHand.utils.load_write_yaml import LoadWriteYaml
from LinkerHand.utils.open_can import OpenCan
class LinkerHandApi:
    def __init__(self,hand_type="left",hand_joint="L10"):
        self.yaml = LoadWriteYaml() # 初始化配置文件
        self.version = self.yaml.load_setting_yaml()["VERSION"]
        ColorMsg(msg=f"当前SDK version:{self.version}", color="green")
        self.hand_joint = hand_joint
        self.hand_type = hand_type
        if self.hand_type == "left":
            self.hand_id = 0x28 # 左手
        else:
            self.hand_id = 0x27 # 右手
        if self.hand_joint == "L10":
            from LinkerHand.core.linker_hand_l10_can import LinkerHandL10Can
            self.hand = LinkerHandL10Can(can_id=self.hand_id)
        if self.hand_joint == "L20":
            from LinkerHand.core.linker_hand_l20_can import LinkerHandL20Can
            pass
        # 打开can0
        if sys.platform == "linux":
            self.open_can = OpenCan()
            self.open_can.open_can0()
            self.is_can = self.open_can.is_can_up_sysfs()
            if not self.is_can:
                ColorMsg(msg="CAN0接口未打开", color="red")
                sys.exit(1)
    
    # 五指运动
    def finger_move(self,pose=[]):
        if self.hand_joint == "L10" and len(pose) == 10:
            self.hand.set_joint_positions(pose)
        else:
            ColorMsg(msg=f"当前LinkerHand为{self.hand_type}{self.hand_joint},动作序列为{pose},并不匹配", color="red")
    
    # 获取法向压力
    def _get_normal_force(self):
        self.hand.get_normal_force()
    # 获取切向压力
    def _get_tangential_force(self):
        self.hand.get_tangential_force()
    # 获取切向压力方向
    def _get_tangential_force_dir(self):
        self.hand.get_tangential_force_dir()
    # 获取接近度
    def _get_approach_inc(self):
        self.hand.get_approach_inc()

    def get_force(self):
        self._get_approach_inc()
        self._get_normal_force()
        self._get_tangential_force()
        self._get_tangential_force_dir()
        return self.hand.get_force()
    # 获取当前关节状态
    def get_state(self):
        return self.hand.get_current_status()
    # 设置速度
    def set_speed(self,speed=[100]*5):
        self.hand.set_joint_speed_l10(speed)
    # 获取速度
    def get_speed(self):
        return self.hand.get_speed()

    

        
    



if __name__ == "__main__":
    hand = LinkerHandApi()