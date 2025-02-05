#!/usr/bin/env python3
import sys,os,time
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(target_dir)

from LinkerHand.linker_hand_api import LinkerHandApi
from LinkerHand.utils.load_write_yaml import LoadWriteYaml
from LinkerHand.utils.init_linker_hand import InitLinkerHand
from LinkerHand.utils.color_msg import ColorMsg

class GetForce:
    def __init__(self):
        # 验证当前LinkerHand配置
        hand = InitLinkerHand()
        # 获取当前LinkerHand信息
        self.hand_joint, self.hand_type = hand.current_hand()
        if self.hand_joint != False and self.hand_type != False:
            # 初始化API
            self.api = LinkerHandApi(hand_joint=self.hand_joint,hand_type=self.hand_type)
        self.get_force()
    
    def get_force(self):
        while True:
            values = self.api.get_force()
            hand_normal_force = values[0] # 五指法向压力
            ColorMsg(msg=f"五指法向压力: {hand_normal_force}", color="green")
            hand_tangential_force = values[1] # 五指切向压力
            ColorMsg(msg=f"五指切向压力: {hand_tangential_force}", color="green")
            hand_tangential_force_dir = values[2] # 五指切向压力方向
            ColorMsg(msg=f"五指切向压力方向: {hand_tangential_force_dir}", color="green")
            hand_approach_inc = values[3] # 五指接近感应
            ColorMsg(msg=f"五指接近感应: {hand_approach_inc}", color="green")
            # 最低间隔时间为0.01
            time.sleep(0.1)

if __name__ == "__main__":
    GetForce()