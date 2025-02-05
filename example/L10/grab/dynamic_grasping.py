#!/usr/bin/env python3
import sys,os,time
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(target_dir)
import argparse
from LinkerHand.linker_hand_api import LinkerHandApi



def main(args):
    # 初始化API
    hand = LinkerHandApi(hand_joint="L10",hand_type="left")
    # 设置速度
    hand.set_speed(speed=[20,50,50,50,50])
    # 准备抓握姿态
    pose = [255, 70, 255, 255, 255, 255, 255, 255, 255, 120]
    hand.finger_move(pose=pose)
    time.sleep(2)
    # 握拳，抓取0mm物品坐标
    # pose = [60, 70, 25, 25, 25, 25, 25, 255, 255, 88]
    # 动态设置坐标
    i = args.mm * 2
    pose[0] = 60 + i
    pose[1] = 60
    pose[2] = 25 + i
    pose[3] = 25 + i
    pose[4] = 25 + i
    pose[5] = 25 + i
    pose[6] = 255
    pose[7] = 255
    pose[8] = 255
    pose[9] = 58
    print(f"Pose {i}: {pose}")
    hand.finger_move(pose=pose)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dynamic Grasping Script")
    parser.add_argument("--hand_joint", type=str, default="L10", help="Hand joint type")
    parser.add_argument("--hand_type", type=str, default="left", help="Hand type")
    parser.add_argument("--speed", type=int, nargs='+', default=[20, 50, 50, 50, 50], help="Speed settings")
    parser.add_argument("--mm", type=int, default="30", help="Distance in mm")
    args = parser.parse_args()
    main(args)