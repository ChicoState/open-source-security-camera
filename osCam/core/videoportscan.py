# from cv2 import VideoCapture
from cmath import inf
from typing import Tuple
from typing_extensions import Self
import cv2

class VideoPortScan:
    def __init__(self) -> None:
        super().__init__()
        self.availablePorts = []
        self.workingPorts = []
        self.nonWorkingPorts =[]

    def __str__(self) -> str:
        return super().__str__() + "::" + VideoPortScan.__name__ + " port:: [{}]".format(self.available_ports)

    
    
    @classmethod
    def ListAllPorts(self)-> Tuple[list, list, list]:
        """
        Test the ports and returns a tuple with the available ports and the ones that are working.
        """
        non_working_ports = []
        dev_port = 0
        working_ports = []
        available_ports = []
        while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
            camera = cv2.VideoCapture(dev_port)
            # camera = VideoCapture(dev_port)
            if not camera.isOpened():
                non_working_ports.append(dev_port)
                print("Port %s is not working." % dev_port)
            else:
                is_reading, img = camera.read()
                w = camera.get(3)
                h = camera.get(4)
                if is_reading:
                    print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                    working_ports.append(dev_port)
                else:
                    print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                    available_ports.append(dev_port)
            dev_port +=1
        return available_ports, working_ports,non_working_ports

    @staticmethod
    def availableAndWorkingPorts() -> Tuple[list, list, bool]:
        available_ports, working_ports, non_working_ports = VideoPortScan.ListAllPorts()
        isAvailable = False
        if available_ports:
            isAvailable = True
        return (available_ports, working_ports, isAvailable)
    
    @staticmethod
    def create():
        return VideoPortScan()