#!/usr/bin/env python3
import sys,os,time
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(target_dir)
from LinkerHand.linker_hand_api import LinkerHandApi
from LinkerHand.utils.init_linker_hand import InitLinkerHand
from LinkerHand.utils.color_msg import ColorMsg

# 初始化机械手
linkerhand = InitLinkerHand()
left_hand, left_hand_joint, left_hand_type, left_hand_force, left_hand_pose, left_hand_torque, left_hand_speed, \
right_hand, right_hand_joint, right_hand_type, right_hand_force, right_hand_pose, right_hand_torque, right_hand_speed, setting = linkerhand.current_hand()

print(f'left {left_hand_joint and left_hand_type}')
print(f'left {right_hand_joint and right_hand_type}')

hand = None
if left_hand_joint and left_hand_type:
    # 如果右手未连接，尝试使用左手
    hand = LinkerHandApi(hand_joint=left_hand_joint, hand_type=left_hand_type)
    ColorMsg(msg=f"使用左手: {left_hand_joint} {left_hand_type}", color="blue")

elif right_hand_joint and right_hand_type:
    # 初始化API
    hand = LinkerHandApi(hand_joint=right_hand_joint, hand_type=right_hand_type)
    ColorMsg(msg=f"使用右手: {right_hand_joint} {right_hand_type}", color="blue")

else:
    ColorMsg(msg="错误：未检测到连接的 LinkerHand 设备。", color="red")
    sys.exit(1)

# 设置速度
speed = [150, 150, 150, 150, 150, 150, 150]  # 提高速度以适应复杂动作
hand.set_speed(speed=speed)
ColorMsg(msg=f"设置速度为: {speed}", color="green")

# 定义手指舞动作序列
def finger_dance():
    print("开始超级复杂的手指舞表演...")
    
    # 第一部分：快速点击与交替
    for _ in range(4):
        hand.finger_move(pose=[0, 0, 255, 0, 0, 0, 0])  # 食指快速点击
        time.sleep(0.15)
        hand.finger_move(pose=[0, 0, 0, 0, 0, 255, 0])  # 小指快速点击
        time.sleep(0.15)
    hand.finger_move(pose=[0, 0, 0, 0, 0, 0, 0])
    time.sleep(0.2)
    
    # 第二部分：波浪动作双向
    for i in range(2, 7):  # 从食指到小指
        pose = [0] * 7
        pose[i] = 255  # 依次抬起每个手指
        hand.finger_move(pose=pose)
        time.sleep(0.08)
    for i in range(5, 1, -1):  # 从无名指到食指
        pose = [0] * 7
        pose[i] = 255
        hand.finger_move(pose=pose)
        time.sleep(0.08)
    hand.finger_move(pose=[0] * 7)
    time.sleep(0.2)
    
    # 第三部分：复杂组合动作 - 对角交替
    for _ in range(2):
        hand.finger_move(pose=[0, 0, 255, 0, 255, 0, 0])  # 食指和无名指
        time.sleep(0.2)
        hand.finger_move(pose=[0, 0, 0, 255, 0, 255, 0])  # 中指和小指
        time.sleep(0.2)
    hand.finger_move(pose=[0] * 7)
    time.sleep(0.2)
    
    # 第四部分：快速三指组合变换
    for _ in range(3):
        hand.finger_move(pose=[0, 0, 255, 255, 0, 0, 0])  # 食指和中指
        time.sleep(0.15)
        hand.finger_move(pose=[0, 0, 0, 255, 255, 0, 0])  # 中指和无名指
        time.sleep(0.15)
        hand.finger_move(pose=[0, 0, 0, 0, 255, 255, 0])  # 无名指和小指
        time.sleep(0.15)
    hand.finger_move(pose=[0] * 7)
    time.sleep(0.2)
    
    # 第五部分：拇指特殊动作（如果支持）
    for _ in range(2):
        hand.finger_move(pose=[255, 255, 0, 0, 0, 0, 0])  # 拇指张开和侧摆
        time.sleep(0.25)
        hand.finger_move(pose=[0, 0, 0, 0, 0, 0, 0])  # 拇指收回
        time.sleep(0.25)
    
    # 第六部分：随机快速闪烁效果
    import random
    for _ in range(6):
        pose = [random.choice([0, 255]) for _ in range(6)] + [0]  # 随机开合手指
        hand.finger_move(pose=pose)
        time.sleep(0.1)
    hand.finger_move(pose=[0] * 7)
    time.sleep(0.2)
    
    # 结束动作：全部手指快速开合 + 渐慢展示
    for t in [0.2, 0.3, 0.4]:  # 逐渐放慢速度
        hand.finger_move(pose=[255, 255, 255, 255, 255, 255, 0])
        time.sleep(t)
        hand.finger_move(pose=[0, 0, 0, 0, 0, 0, 0])
        time.sleep(t)
    
    print("超级复杂的手指舞表演结束！")

if __name__ == "__main__":
    try:
        finger_dance()
    except KeyboardInterrupt:
        print("\n再见!")
    finally:
        # 没有找到明确的关闭方法，可能不需要
        pass
