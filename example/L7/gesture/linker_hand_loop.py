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
手掌握拳
'''
def main():
    # 验证当前LinkerHand配置
    linkerhand = InitLinkerHand()
    # 获取当前LinkerHand信息
    left_hand ,left_hand_joint ,left_hand_type ,left_hand_force,left_hand_pose, left_hand_torque, left_hand_speed ,right_hand ,right_hand_joint ,right_hand_type ,right_hand_force,right_hand_pose, right_hand_torque, right_hand_speed,setting = linkerhand.current_hand()
    if left_hand_joint != False and left_hand_type != False:
        # 初始化API
        hand = LinkerHandApi(hand_joint=left_hand_joint,hand_type=left_hand_type)
    if right_hand_joint != False and right_hand_type != False:
        # 初始化API
        hand = LinkerHandApi(hand_joint=right_hand_joint,hand_type=right_hand_type)
    # 设置速度
    speed = [120,250,250,250,250,250,250]
    hand.set_speed(speed=speed)
    ColorMsg(msg=f"当前设置速度为:{speed}", color="green")
    pose = [[255,255,255,255,255,255,255],[255,255,0,255,255,255,255],[255,255,0,0,255,255,255],[255,255,0,0,0,255,255],[255,255,0,0,0,0,255],[72,90,0,0,0,0,55]]
    while True:
        for i in range(6):
            print("_-"*10)
            print(i)
            ColorMsg(msg=f"当前为手指运动坐标:{pose[i]}", color="green")
            hand.finger_move(pose=pose[i])
            time.sleep(3)


if __name__ == "__main__":
    main()