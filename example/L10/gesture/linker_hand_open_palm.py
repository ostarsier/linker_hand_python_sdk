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
手掌张开
'''
def main():
    # 验证当前LinkerHand配置
    linkerhand = InitLinkerHand()
    # 验证当前LinkerHand配置
    left_hand ,left_hand_joint ,left_hand_type ,left_hand_force,left_hand_pose, left_hand_torque, left_hand_speed ,right_hand ,right_hand_joint ,right_hand_type ,right_hand_force,right_hand_pose, right_hand_torque, right_hand_speed,setting = linkerhand.current_hand()
    if left_hand_joint != False and left_hand_type != False:
        # 初始化API
        hand = LinkerHandApi(hand_joint=left_hand_joint,hand_type=left_hand_type)
    if right_hand_joint != False and right_hand_type != False:
        # 初始化API
        hand = LinkerHandApi(hand_joint=right_hand_joint,hand_type=right_hand_type)
    # 设置速度
    hand.set_speed(speed=[120,250,250,250,250])
    # 手指姿态数据
    pose = [255.0,70.0,255.0,255.0,255.0,255.0,255.0,255.0,255.0,255.0]
    hand.finger_move(pose=pose)


if __name__ == "__main__":
    main()