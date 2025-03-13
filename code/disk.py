RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[94m'

import time

class Disk_deal:
    def __init__(self, tolerance=3, stationary_flag=6, grab_distance = 150):
        self.action = None
        self.actions = [None, None]
        self.tolerance = tolerance
        self.stationary_flag = stationary_flag # define a 
        self.grab_distance = grab_distance
        self.rectangle = None
        self.session = 0
        self.stationary_counts = 0
        self.stable_center_xy = [35, -10]
        self.error_center_xy = None
        self.qr_data = None
        self.send_grab = False
        self.if_send_data = False
        self.first_color = None
    
    def clear(self):
        self.action = None
        self.actions = [None, None]
        self.rectangle = None
        self.session = 0
        self.stationary_counts = 0
        self.stable_center_xy = [35, -10]
        self.error_center_xy = None
        self.send_grab = False
        self.if_send_data = False
        self.first_color = None
    
    def _in_rectangle(self, center_xy):
        if (abs(self.stable_center_xy[0] - center_xy[0]) > self.grab_distance) or (abs(self.stable_center_xy[1] - center_xy[1]) > self.grab_distance):
            return False
        return True
        
        
    
    def if_move(self, center_xy):
        if self.session == 0:
            try:
                self.actions[0] = self.actions[1]
                self.actions[1] = center_xy[:2]
            except:
                if center_xy == None:
                    # print(f"{YELLOW}center_xy is None!!{RESET}")
                    self.actions[0] = None
                    self.actions[1] = None
            try:
                if (abs(self.actions[0][0] - self.actions[1][0]) > self.tolerance) or (abs(self.actions[0][1] - self.actions[1][1]) > self.tolerance):
                    self.action = "Moving"
                    self.stationary_counts = 0
                    self.rectangle = None
                else:
                    self.action = "Stationary"
                    self.stationary_counts += 1
            except Exception as e:
                # print(e)
                self.action = "None"
                self.stationary_counts = 0
            # self.rectangle = None
            if self.stationary_counts >= self.stationary_flag and self.session == 0:
                self.error_center_xy = center_xy
                self.first_color = [center_xy[2], False]
                self.rectangle = ((self.stable_center_xy[0] + 320 - 130, self.stable_center_xy[1] + 240 - 130), (self.stable_center_xy[0] + 320 + 130, self.stable_center_xy[1] + 240 + 130))
                print(f"{GREEN}Find the right rectangle!!{RESET}")
                self.session = 1
            # print(self.stationary_counts)
        elif self.session == 1:
            self.action = "Sending..."
            # try:
            #   if center_xy[2] != self.first_color[0]:
            #       self.first_color[1] = False
            #       self.session = 2
            #       print(f"{GREEN}Okay, ready to grab!{RESET}")
            # except:
            #   pass
        elif self.session == 2:
            if self.qr_data is None:
                print(f"{RED}qr_data is None!!{RESET}")
                print(f"{RED}qr_data is None!!{RESET}")
                print(f"{RED}qr_data is None!!{RESET}")
                print(f"{RED}qr_data is None!!{RESET}")
                print(f"{RED}Scan qr_data first!!!{RESET}")
            elif len(self.qr_data) == 0:
                pass
                # print(f"{GREEN}Grab Done next task!!{RESET}")
            elif self.if_send_data:
                self.action = "Grabing..."
            elif not self.if_send_data:
                self.action = "Waiting..."
            try:
                if self.qr_data[0] == int(center_xy[2]) and (not self.if_send_data) and self._in_rectangle(center_xy[:2]):
                    print(f"{GREEN}Ready to grab color {center_xy[2]}....{RESET}")
                    self.send_grab = True
            except Exception as e:
                pass   
            # print(f"send_grab: {self.send_grab}")
            # print(f"if_send_data: {self.if_send_data}")
                
        # print(f"self.stationary_counts: {self.stationary_counts}")
    # def if_grab(self):
