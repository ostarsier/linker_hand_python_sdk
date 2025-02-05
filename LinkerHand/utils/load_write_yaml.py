import yaml, os, sys
# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 找到上上级目录
target_dir = os.path.abspath(os.path.join(current_dir, "../.."))
# 添加到 sys.path
sys.path.append(target_dir)


class LoadWriteYaml():
    def __init__(self):
        self.setting_path = target_dir + "/LinkerHand/config/setting.yaml"
        self.l10_positions = target_dir + "/LinkerHand/config/L10_positions.yaml"
        self.l20_positions = target_dir + "/LinkerHand/config/L20_positions.yaml"
        

    def load_setting_yaml(self):
        try:
            with open(self.setting_path, 'r', encoding='utf-8') as file:
                setting = yaml.safe_load(file)
                self.sdk_version = setting["VERSION"]
                self.left_hand_exists = setting['LINKER_HAND']['LEFT_HAND']['EXISTS']
                self.left_hand_names = setting['LINKER_HAND']['LEFT_HAND']['NAME']
                self.left_hand_joint = setting['LINKER_HAND']['LEFT_HAND']['JOINT']
                self.left_hand_force = setting['LINKER_HAND']['LEFT_HAND']['TOUCH']
                self.right_hand_exists = setting['LINKER_HAND']['RIGHT_HAND']['EXISTS']
                self.right_hand_names = setting['LINKER_HAND']['RIGHT_HAND']['NAME']
                self.right_hand_joint = setting['LINKER_HAND']['RIGHT_HAND']['JOINT']
                self.right_hand_force = setting['LINKER_HAND']['RIGHT_HAND']['TOUCH']
                self.password = setting['PASSWORD']
        except Exception as e:
            setting = None
            print(f"Error reading setting.yaml: {e}")
        self.setting = setting
        return self.setting
    
    def load_action_yaml(self,hand_joint="",hand_type=""):
        if hand_joint == "L20":
            action_path = self.l20_positions
        elif hand_joint == "L10":
            action_path = self.l10_positions
        elif hand_joint == "L25":
            #action_path = action_path + "L25_action.yaml"
            pass
        try:
            with open(action_path, 'r', encoding='utf-8') as file:
                yaml_data = yaml.safe_load(file)
                if hand_type == "left":
                    self.action_yaml = yaml_data["LEFT_HAND"]
                else:
                    self.action_yaml = yaml_data["RIGHT_HAND"]
        except Exception as e:
            self.action_yaml = None
            print(f"yaml配置文件不存在: {e}")
        return self.action_yaml 

    def write_to_yaml(self, action_name, action_pos,hand_joint="",hand_type=""):
        a = False
        if hand_joint == "L20":
            action_path = self.l20_positions
        elif hand_joint == "L10":
            action_path = self.l10_positions
        elif hand_joint == "L25":
            #action_path = action_path + "L25_action.yaml"
            pass
        try:
            with open(action_path, 'r', encoding='utf-8') as file:
                yaml_data = yaml.safe_load(file)
                print(yaml_data)
            if hand_type == "left":
                if yaml_data["LEFT_HAND"] == None:
                    yaml_data["LEFT_HAND"] = []
                yaml_data["LEFT_HAND"].append({"ACTION_NAME": action_name, "POSITION": action_pos})
            elif hand_type == "right":
                if yaml_data["RIGHT_HAND"] == None:
                    yaml_data["RIGHT_HAND"] = []
                yaml_data["RIGHT_HAND"].append({"ACTION_NAME": action_name, "POSITION": action_pos})
            with open(action_path, 'w', encoding='utf-8') as file:
                yaml.safe_dump(yaml_data, file, allow_unicode=True)
            a = True
        except Exception as e:
            a = False
            print(f"Error writing to yaml file: {e}")
        return a
        