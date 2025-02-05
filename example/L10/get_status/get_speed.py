#!/usr/bin/env python3
import sys,os,time
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(target_dir)

from LinkerHand.linker_hand_api import LinkerHandApi
from LinkerHand.utils.load_write_yaml import LoadWriteYaml
from LinkerHand.utils.init_linker_hand import InitLinkerHand
from LinkerHand.utils.color_msg import ColorMsg
'''
目前L10没有监听当前速度的can指令，暂时不支持实时获取速度
'''
class GetSpeed:
    def __init__(self):
        # 验证当前LinkerHand配置
        hand = InitLinkerHand()
        # 获取当前LinkerHand信息
        self.hand_joint, self.hand_type = hand.current_hand()
        if self.hand_joint != False and self.hand_type != False:
            # 初始化API
            self.api = LinkerHandApi(hand_joint=self.hand_joint,hand_type=self.hand_type)
        self.get_speed()
    
    def get_speed(self):
        while True:
            speed = self.api.get_speed()
            print(f"Current speed: {speed}")
            time.sleep(0.01)

if __name__ == "__main__":
    GetSpeed()