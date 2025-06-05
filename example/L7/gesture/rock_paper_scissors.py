import sys, os, time
import random # 新增导入

current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(target_dir)

from LinkerHand.linker_hand_api import LinkerHandApi
from LinkerHand.utils.init_linker_hand import InitLinkerHand
from LinkerHand.utils.color_msg import ColorMsg
# from LinkerHand.utils.load_write_yaml import LoadWriteYaml # 似乎未使用，暂时注释
# import numpy as np # 似乎未使用，暂时注释

def main():
    linkerhand = InitLinkerHand()
    left_hand, left_hand_joint, left_hand_type, left_hand_force, left_hand_pose, left_hand_torque, left_hand_speed, \
    right_hand, right_hand_joint, right_hand_type, right_hand_force, right_hand_pose, right_hand_torque, right_hand_speed, setting = linkerhand.current_hand()

    hand = None
    if right_hand_joint and right_hand_type:
        # 初始化API
        hand = LinkerHandApi(hand_joint=right_hand_joint, hand_type=right_hand_type)
        ColorMsg(msg=f"使用右手: {right_hand_joint} {right_hand_type}", color="blue")
    elif left_hand_joint and left_hand_type:
        # 如果右手未连接，尝试使用左手
        hand = LinkerHandApi(hand_joint=left_hand_joint, hand_type=left_hand_type)
        ColorMsg(msg=f"使用左手: {left_hand_joint} {left_hand_type}", color="blue")
    else:
        ColorMsg(msg="错误：未检测到连接的 LinkerHand 设备。", color="red")
        return

    # 设置速度 - 您可以根据需要调整
    speed = [120, 120, 120, 120, 120, 120, 120]
    hand.set_speed(speed=speed)
    ColorMsg(msg=f"设置速度为: {speed}", color="green")

    # 定义姿势: [拇指, 拇指侧摆, 食指, 中指, 无名指, 小指, 拇指旋转]
    # 范围 0-255, 0为握拳, 255为张开
    rock_pose =     [0,   0,   0,   0,   0,   0,   0]  # 石头
    paper_pose =    [255, 255, 255, 255, 255, 255, 0]  # 布 (拇指旋转通常保持0或根据实际调整)
    scissors_pose = [0,   0,   255, 255, 0,   0,   0]  # 剪刀 (拇指内收，食指中指伸直)

    gestures = {
        "石头": rock_pose,
        "布": paper_pose,
        "剪刀": scissors_pose
    }
    gesture_names = list(gestures.keys())

    ColorMsg(msg="准备就绪！按回车键随机切换姿势，按 Ctrl+C 退出。", color="cyan")

    while True:
        chosen_gesture_name = random.choice(gesture_names)
        current_pose = gestures[chosen_gesture_name]
        
        ColorMsg(msg=f"出示: {chosen_gesture_name} - 姿态: {current_pose}", color="yellow")
        hand.finger_move(pose=current_pose)
        
        try:
            input("按回车键切换...")
        except KeyboardInterrupt:
            print("\n再见!")
            break

if __name__ == "__main__":
    main()
