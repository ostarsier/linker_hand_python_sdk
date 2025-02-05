# LinkerHand-Python-SDK

## Overview
LinkerHand Python SDK

## Caution
- 请确保灵巧手未开启其他控制，如linker_hand_sdk_ros、动捕手套控制和其他控制灵巧手的topic。以免冲突。
- 请将固定灵巧手，以免灵巧手在运动时跌落。
- 请确保灵巧手电源与USB转CAN连接正确。

## Installation
&ensp;&ensp;您可以在安装requirements.txt后的情况下运行示例。仅支持 Python3。
- download

  ```bash
  git clone https://github.com/linkerbotai/linker_hand_python_sdk.git
  ```

- install

  ```bash
  pip3 install -r requirements.txt
  ```

## 相关文档


## 更新说明
- > ### 1.1.2
  - 支持LinkerHand L10版本灵巧手
  - 增加GUI控制L10灵巧手
  - 增加GUI显示L10灵巧手压感图形模式数据
  - 增加部分示例源码
  


## [L10_Example](example/L10)

&ensp;&ensp; __在运行之前, 请将 [setting.yaml](LinkerHand/config/setting.yaml) 的配置信息修改为您实际控制的灵巧手配置信息.__

- #### [0000-gui_control](example/gui_control/gui_control.py)
- #### [0001-linker_hand_fast](example/L10/gesture/linker_hand_fast.py)
- #### [0002-linker_hand_finger_bend](example/L10/gesture/linker_hand_finger_bend.py)
- #### [0003-linker_hand_fist](example/L10/gesture/linker_hand_fist.py)
- #### [0004-linker_hand_open_palm](example/L10/gesture/linker_hand_open_palm.py)
- #### [0005-linker_hand_opposition](example/L10/gesture/linker_hand_opposition.py)
- #### [0006-linker_hand_sway](example/L10/gesture/linker_hand_sway.py)

- #### [0006-linker_hand_get_force](example/L10/get_status/get_force.py)
- #### [0006-linker_hand_get_speed](example/L10/get_status/get_speed.py)
- #### [0006-linker_hand_get_state](example/L10/get_status/get_state.py)




- #### Import
  ```python
  from LinkerHand.linker_hand_api import LinkerHandApi
  # 初始化API L10 左手
  hand = LinkerHandApi(hand_joint="L10",hand_type="left")
  # 初始化API L10 右手
  hand = LinkerHandApi(hand_joint="L10",hand_type="right")
  ```

- #### Connect/Disconnect
  ```python
  arm.connect(...)
  arm.disconnect()
  ```

- #### Move
  ```python
  hand.finger_move(...)
  ```

- #### Set
  ```python
  hand.set_speed(...)
  ```

- #### Get
  ```python
  hand.get_force()
  hand.get_speed()
  hand.get_state()
  ```



