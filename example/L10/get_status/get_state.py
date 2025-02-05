#!/usr/bin/env python3
import sys,os,time
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(target_dir)

from LinkerHand.linker_hand_api import LinkerHandApi
from LinkerHand.utils.load_write_yaml import LoadWriteYaml
from LinkerHand.utils.init_linker_hand import InitLinkerHand
from LinkerHand.utils.color_msg import ColorMsg

class GetState:
    def __init__(self):
        # 验证当前LinkerHand配置
        hand = InitLinkerHand()
        # 获取当前LinkerHand信息
        self.hand_joint, self.hand_type = hand.current_hand()
        if self.hand_joint != False and self.hand_type != False:
            # 初始化API
            self.api = LinkerHandApi(hand_joint=self.hand_joint,hand_type=self.hand_type)
        self.get_state()
    # 获取当前状态
    def get_state(self):
        count = 0
        while True:
            state = self.api.get_state()+[count]
            print(f"Current state: {state}")
            count += 1
            time.sleep(0.01)

if __name__ == "__main__":
    GetState()
