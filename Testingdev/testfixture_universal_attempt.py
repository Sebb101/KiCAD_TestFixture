import numpy as np
import pandas as pd
import cadquery as cq
import os

class testFixture():
    def __init__(self):
        # Dimensions in mm
        self.length = 0
        self.width = 0
        self.thickness = 3
        self.length_width_OFFSET = 10

class testpoint():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.diameter = 1

class mountingHole():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.diameter = 3.2


def main():
    # Read from pos file from kiCAD Fabrication file
    # Also asks user to provide the path to KiCAD File
    csv_path = input("Enter the full path to your KiCAD .csv (.pos) file: ").strip()
    boardposFile = pd.read_csv(csv_path)

    # List of all testpoint & mounting hole indices on csv
    testpoint_indices = boardposFile.index[boardposFile['Val'] == "TestPoint"].tolist()
    mount_indices = boardposFile.index[boardposFile['Val'] == "MountingHole_Pad"].tolist()


    # Array of footprint objects
    textboard = testFixture()
    testpoints = [testpoint() for i in range(len(testpoint_indices))]
    mountHoles = [mountingHole() for i in range(len(mount_indices))]

    # Assign one mounting hole as our origin
    XPOS_ZERO = boardposFile.iloc[mount_indices[0]]["PosX"]
    YPOS_ZERO = boardposFile.iloc[mount_indices[0]]["PosY"]

    # Create objects for all test points
    for row in range(0,len(testpoint_indices)):
        testpoints[row].xpos = boardposFile.iloc[testpoint_indices[row]]["PosX"] - XPOS_ZERO
        testpoints[row].ypos = boardposFile.iloc[testpoint_indices[row]]["PosY"] - YPOS_ZERO

    for row in range(0,len(mount_indices)):
        mountHoles[row].xpos = boardposFile.iloc[mount_indices[row]]["PosX"] - XPOS_ZERO
        mountHoles[row].ypos = boardposFile.iloc[mount_indices[row]]["PosY"] - YPOS_ZERO


    # Find the length and width of test fixture board
    # ONLY FOR RECTANGLES!
    for y in range(1,len(mount_indices)):
        if(mountHoles[0].xpos == mountHoles[y].xpos):
            textboard.length = mountHoles[0].ypos - mountHoles[y].ypos
            if(textboard.length < 0):
                textboard.length = (textboard.length * -1) 
        elif(mountHoles[0].ypos == mountHoles[y].ypos):
            textboard.width = mountHoles[0].xpos - mountHoles[y].xpos
            if(textboard.width < 0):
                textboard.width = (textboard.width * -1)
        if(textboard.length > 0 and textboard.width > 0):
            break

    # Add offset to board
    textboard.length = textboard.length + textboard.length_width_OFFSET
    textboard.width = textboard.width + textboard.length_width_OFFSET


    # Print sizing to confirm
    print(textboard.length)
    print(textboard.width)

    coord_change = (textboard.length/2) - (textboard.length_width_OFFSET/2)

    # Change coords to be relative to center of board
    # If mounting hole is NOT in upper left corner must add/change offset direction
    for row in range(0,len(mount_indices)):
        mountHoles[row].xpos = mountHoles[row].xpos - coord_change
        mountHoles[row].ypos = mountHoles[row].ypos + coord_change

    for row in range(0,len(testpoint_indices)):

        testpoints[row].xpos = testpoints[row].xpos - coord_change
        testpoints[row].ypos = testpoints[row].ypos + coord_change

    # Extrude Holes for mounting holes and test probes
    # Fixed the second mountHoles[0].xpos to mountHoles[0].ypos
    # Same fix on tplist
    mhlist = [[mountHoles[0].xpos,mountHoles[0].ypos]]
    for y in range(1,len(mount_indices)):
        mhlist.append([mountHoles[y].xpos,mountHoles[y].ypos])

    # result = result.pushPoints(mhlist)  # now testpoints are on the stack
    # result = result.circle(mountHoles[0].diameter)

    tplist = [[testpoints[0].xpos,testpoints[0].ypos]]

    print(len(mount_indices))
    print(len(testpoint_indices))

    for y in range(1,len(testpoint_indices)):
        tplist.append([testpoints[y].xpos,testpoints[y].ypos])
        
    # # Render the solid
    # #show_object(result)

    # Export object as stl file
    # Fixed .box(textboard.length, textboard.width,...)
    # to .box(textboard.width, textboard.length,...)
    boardthing = cq.Workplane("front").box(textboard.width, textboard.length, textboard.thickness).faces(">Z").workplane()

    boardthing = boardthing.pushPoints(mhlist)  # now testpoints are on the stack
    boardthing = boardthing.hole(mountHoles[0].diameter)
    #Don't need this line as it is using .hole() to cut through 
    # boardthing = boardthing.cutThruAll()
    boardthing = boardthing.pushPoints(tplist)  # now testpoints are on the stack
    boardthing = boardthing.hole(testpoints[0].diameter)

    # added code below to find STL file
    os.makedirs("kiCAD_BoardTesting", exist_ok=True)
    output_path = os.path.abspath("kiCAD_BoardTesting/testfixture1.stl")
    print("Exporting STL to: ", output_path)

    cq.exporters.export(boardthing, "kiCAD_BoardTesting/testfixture1.stl")
    
if __name__ == "__main__":
    main()