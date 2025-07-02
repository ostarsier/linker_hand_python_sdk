#!/usr/bin/env python3
import sys, os
from flask import Flask, jsonify, request
from threading import Thread
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(target_dir)
from LinkerHand.linker_hand_api import LinkerHandApi
from LinkerHand.utils.load_write_yaml import LoadWriteYaml
from LinkerHand.utils.init_linker_hand import InitLinkerHand
from LinkerHand.utils.color_msg import ColorMsg
import numpy as np

app = Flask(__name__)

# 初始化手部控制
linkerhand = InitLinkerHand()
left_hand, left_hand_joint, left_hand_type, left_hand_force, left_hand_pose, left_hand_torque, left_hand_speed, \
right_hand, right_hand_joint, right_hand_type, right_hand_force, right_hand_pose, right_hand_torque, right_hand_speed, setting = linkerhand.current_hand()

hand = None
if right_hand_joint and right_hand_type:
    hand = LinkerHandApi(hand_joint=right_hand_joint, hand_type=right_hand_type)
    ColorMsg(msg=f"使用右手: {right_hand_joint} {right_hand_type}", color="blue")
elif left_hand_joint and left_hand_type:
    hand = LinkerHandApi(hand_joint=left_hand_joint, hand_type=left_hand_type)
    ColorMsg(msg=f"使用左手: {left_hand_joint} {left_hand_type}", color="blue")
else:
    ColorMsg(msg="错误：未检测到连接的 LinkerHand 设备。", color="red")
    exit(1)

# 设置速度
speed = [120, 120, 120, 120, 120, 120, 120] 
hand.set_speed(speed=speed)

# 定义各种手势的姿势数据
poses = {
    "handshake": [180, 180, 180, 180, 180, 180, 180],  # 握手姿势
    "open": [255, 255, 255, 255, 255, 255, 255],       # 手指完全张开
    "scissors": [255, 255, 255, 100, 100, 100, 255],   # 剪刀手势（食指和中指伸直，其他手指弯曲）
    "rock": [100, 100, 100, 100, 100, 100, 100],        # 石头手势（拳头）
    "paper": [200, 200, 200, 200, 200, 200, 200]        # 布手势（手掌）
}

def execute_action(action):
    """执行手势动作"""
    try:
        if action not in poses:
            return jsonify({"error": f"未知的动作: {action}"}), 400
            
        pose = poses[action]
        hand.finger_move(pose=pose)
        return jsonify({"status": "success", "action": action})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/hand/<action>', methods=['GET'])
def hand_action(action):
    """执行手部动作的API接口"""
    return execute_action(action)

@app.route('/hand/<action>', methods=['GET'])
def hand_action_default(action):
    """执行手部动作的API接口，默认使用open姿势"""
    return execute_action(action, "open")

@app.route('/actions', methods=['GET'])
def list_actions():
    """列出所有可用的动作"""
    return jsonify({"actions": list(poses.keys())})

@app.route('/status', methods=['GET'])
def status():
    """获取手部状态"""
    return jsonify({
        "status": "connected",
        "hand": "right" if right_hand_joint else "left",
        "joint": right_hand_joint if right_hand_joint else left_hand_joint,
        "type": right_hand_type if right_hand_type else left_hand_type
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
