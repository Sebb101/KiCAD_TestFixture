import numpy as np
import pandas as pd
import cadquery as cad



class testpoint():
    def __init__(self):
        self.xpos=0
        self.ypos=0
        self.diameter = 1.5

class mountingHole():
    def __init__(self):
        self.xpos=0
        self.ypos=0
        self.diameter = 3.2


if __name__ == '__main__':
    boardposFile = pd.read_csv("C:/Users/jasev/OneDrive/Desktop/KiCad Designs/KiCad_RP/Constellation Stack V3.0 Review ZIP/footprint_report/Constellation Stack V3.0-all-pos.csv")

    # List of all testpoint & mounting hole indices on csv
    testpoint_indices = boardposFile.index[boardposFile['Val'] == "TestPoint"].tolist()
    mount_indices = boardposFile.index[boardposFile['Val'] == "MountingHole_Pad"].tolist()

    # Array of footprint objects
    testpoints = [testpoint() for i in range(len(testpoint_indices))]
    mountHoles = [mountingHole() for i in range(len(mount_indices))]

    # Assign one mounting hole as our origin
    XPOS_ZERO = boardposFile.iloc[mount_indices[0]]["PosX"]
    YPOS_ZERO = boardposFile.iloc[mount_indices[0]]["PosY"]
    
    print(XPOS_ZERO)
    print(YPOS_ZERO)

    for row in range(0,len(testpoint_indices)):
        testpoints[row].xpos = boardposFile.iloc[testpoint_indices[row]]["PosX"] - XPOS_ZERO
        testpoints[row].ypos = boardposFile.iloc[testpoint_indices[row]]["PosY"] - YPOS_ZERO

    for row in range(0,len(mount_indices)):
        mountHoles[row].xpos = boardposFile.iloc[mount_indices[row]]["PosX"] - XPOS_ZERO
        mountHoles[row].ypos = boardposFile.iloc[mount_indices[row]]["PosY"] - YPOS_ZERO




