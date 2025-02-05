import yaml, os, sys
from load_write_yaml import LoadWriteYaml

class InitLinkerHand():
    def __init__(self):
        self.yaml = LoadWriteYaml()
        self.setting = self.yaml.load_setting_yaml()

    def current_hand(self):
        # 判断左手是否配置
        self.left_hand = False
        self.right_hand = False
        if self.setting['LINKER_HAND']['LEFT_HAND']['EXISTS'] == True:
            self.left_hand = True
        elif self.setting['LINKER_HAND']['RIGHT_HAND']['EXISTS'] == True:
            self.right_hand = True
        # gui控制只支持单手，这里进行左右手互斥
        if self.left_hand == True and self.right_hand == True:
            self.left_hand = True
            self.right_hand = False
        if self.left_hand == True:
            print("左手")
            self.hand_exists = True
            self.hand_joint = self.setting['LINKER_HAND']['LEFT_HAND']['JOINT']
            self.hand_type = "left"
        if self.right_hand == True:
            print("右手")
            self.hand_exists = True
            self.hand_joint = self.setting['LINKER_HAND']['RIGHT_HAND']['JOINT']
            self.hand_type = "right"
        return self.hand_joint, self.hand_type
        