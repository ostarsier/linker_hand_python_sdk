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
手指侧摆
'''
def main():
    # 验证当前LinkerHand配置
    linkerhand = InitLinkerHand()
    # 获取当前LinkerHand信息
    hand_joint, hand_type = linkerhand.current_hand()
    if hand_joint != False and hand_type != False:
        # 初始化API
        hand = LinkerHandApi(hand_joint=hand_joint,hand_type=hand_type)
    # 设置速度
    hand.set_speed(speed=[120,60,60,60,60])
    # 手指姿态数据
    poses = [
        [255.0,255.0,255.0,255.0,255.0,255.0,40.0,88.0,80.0,63.0], # 手掌张开
        [255.0,0.0,255.0,255.0,255.0,255.0,40.0,88.0,80.0,63.0], # 拇指侧摆
        [255.0,70.0,255.0,255.0,255.0,255.0,40.0,88.0,80.0,0.0], # *手掌张开
        [255.0,255.0,255.0,255.0,255.0,255.0,40.0,88.0,80.0,255.0], # 拇指旋转
        [255.0,255.0,255.0,255.0,255.0,255.0,40.0,88.0,80.0,63.0], # 手掌张开
        [255.0,255.0,255.0,255.0,255.0,255.0,255.0,88.0,80.0,63.0], # 食指侧摆
        [255.0,255.0,255.0,255.0,255.0,255.0,40.0,88.0,80.0,63.0], # 手掌张开
        [255.0,255.0,255.0,255.0,255.0,255.0,40.0,255.0,80.0,63.0], # 无名指侧摆
        [255.0,255.0,255.0,255.0,255.0,255.0,40.0,88.0,80.0,63.0], # 手掌张开
        [255.0,255.0,255.0,255.0,255.0,255.0,40.0,88.0,255.0,63.0], # 小拇指侧摆
        [255.0,255.0,255.0,255.0,255.0,255.0,40.0,88.0,80.0,63.0], # 手掌张开
    ]
    while True:
        for pose in poses:
            hand.finger_move(pose=pose)
            time.sleep(1)


if __name__ == "__main__":
    main()