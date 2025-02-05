#!/usr/bin/env python3
import sys,os,time
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(target_dir)
from LinkerHand.linker_hand_api import LinkerHandApi
'''
手指快速移动
'''
def main():
    hand = LinkerHandApi(hand_joint="L10",hand_type="right")
    while True:
        for i in range(10):
            if i % 2 == 0:
                pose = [255, 128, 255, 255, 255, 255, 128, 128, 128, 128]
            else:
                pose = [80, 80, 80, 80, 80, 80, 80, 80, 80, 80]
            print(f"Pose {i}: {pose}")
            # 在这里添加更新pose的代码，例如发送到硬件设备
            time.sleep(0.1)  # 等待1秒
            hand.finger_move(pose=pose)

if __name__ == "__main__":
    main()