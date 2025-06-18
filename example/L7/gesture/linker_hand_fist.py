#!/usr/bin/env python3
import sys,os,time
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(target_dir)
from LinkerHand.linker_hand_api import LinkerHandApi
from LinkerHand.utils.load_write_yaml import LoadWriteYaml
from LinkerHand.utils.init_linker_hand import InitLinkerHand
from LinkerHand.utils.color_msg import ColorMsg
import numpy as np


def main():
    # 验证当前LinkerHand配置
    linkerhand = InitLinkerHand()
    # 获取当前LinkerHand信息
    left_hand ,left_hand_joint ,left_hand_type ,left_hand_force,left_hand_pose, left_hand_torque, left_hand_speed ,right_hand ,right_hand_joint ,right_hand_type ,right_hand_force,right_hand_pose, right_hand_torque, right_hand_speed,setting = linkerhand.current_hand()
    if right_hand_joint and right_hand_type:
        # 初始化API
        hand = LinkerHandApi(hand_joint=right_hand_joint,hand_type=right_hand_type)
    elif left_hand_joint and left_hand_type:
        # 如果右手未连接，尝试使用左手
        hand = LinkerHandApi(hand_joint=left_hand_joint, hand_type=left_hand_type)
        ColorMsg(msg=f"使用左手: {left_hand_joint} {left_hand_type}", color="blue")
    else:
        ColorMsg(msg="错误：未检测到连接的 LinkerHand 设备。", color="red")
        return
    # 设置速度
    speed = [120,120,120,120,120,120,120]
    hand.set_speed(speed=speed)
    ColorMsg(msg=f"当前为{right_hand_joint} {right_hand_type},设置速度为:{speed}", color="green")
    # 手指姿态数据
    # [拇指,拇指侧摆, 食指,中指,无名指,小指， 拇指旋转]
    # 范围 0-255, 255为张开，0为握拳
    pose = [120, 120, 130, 130, 130, 130, 120] 
    ColorMsg(msg=f"当前为{right_hand_joint} {right_hand_type},手指运动坐标:{pose}", color="green")
    hand.finger_move(pose=pose)

    # 没有finger_move，get_state都是0
    print(hand.get_state())

    print(hand.get_touch_type())

    while True:
        thumb_matrix , index_matrix , middle_matrix , ring_matrix , little_matrix = hand.get_matrix_touch()
        activated_sensors = 0
        for m_list in [index_matrix, middle_matrix, ring_matrix]: 
            activated_sensors += (m_list > 0).sum()
            print(f"激活数量: {activated_sensors}")

            
        # pressure_matrices = hand.get_matrix_touch()
        # high_pressure_count = 0
        # for matrix in pressure_matrices:
        #     if np.any(matrix > 50):
        #         high_pressure_count += 1
        # print(f"高压力计数: {high_pressure_count}")

        print(f"拇指: {thumb_matrix}")
        print(f"食指: {index_matrix}")
        print(f"中指: {middle_matrix}")
        print(f"无名指: {ring_matrix}")
        print(f"小指: {little_matrix}")

        time.sleep(1)
        print('-='*20)


if __name__ == "__main__":
    main()