
https://document.linkeros.cn/developer/68

# 开启CAN端口
sudo ip link set can0 down # 先关闭接口
sudo ip link set can0 type can bitrate 1000000 #USB转CAN设备蓝色灯常亮状态
sudo ip link set can0 txqueuelen 1000 # 将发送队列长度设置为1000 
sudo ip link set can0 up # 重新启动接口


# 查看can0状态
ip -details link show can0

# 查看can0数据
candump can0

# python example/L7/gesture/crasp.py


# 移动到固定姿势
python hand_api.py
curl http://localhost:5000/hand/handshake