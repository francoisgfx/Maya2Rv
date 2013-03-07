# Maya to RV
#version 1.2

import maya.cmds as cmds
import os

#------ CAMERA ----------------

#camera = cmds.ls(selection=True)
#camera = camera[0]
#get current camera view
camera = cmds.modelPanel(cmds.getPanel(wf=True), q=True, cam=True)


#-------- IMAGE PLANE ---------------
#get its image plane
imagePlane = cmds.listConnections(camera + ".imagePlane")
#get the image plane file path
imagePlaneFile = cmds.getAttr(imagePlane[0]+".imageName")
if cmds.getAttr(imagePlane[0]+".useFrameExtension") :
    directory = os.path.dirname(imagePlaneFile)
    fullFilename = os.path.basename(imagePlaneFile)
    splitExt = os.path.splitext(fullFilename)
    fileName = splitExt[0].split(".")[0]
    imagePlaneFile = directory + "/" + fileName + "." + str(cmds.getAttr(imagePlane[0]+".frameExtension")) + splitExt[1]

#get display mode of the image plane
displayMode = cmds.getAttr(imagePlane[0]+".displayMode")
#set the display mode to None
cmds.setAttr(imagePlane[0]+".displayMode",0)


#------------ RENDER SETTINGS --------------
# Set cam to Render
allCams = cmds.listCameras()
for cam in allCams :
    cmds.setAttr(cam + ".renderable",False)
cmds.setAttr(camera + ".renderable",True)


#-------------- RENDER --------------------
#hardware render current Frame (cf)
hwrPath = cmds.hwRender(cf=True,cv=True,lql=True)


#----------------- RV ---------------------
#launch RV
os.system("rv -wipe " + hwrPath + " " + imagePlaneFile + " &" )


#-------------- RESTORE SETTINGS ------------------
#set the display mode as it was
cmds.setAttr(imagePlane[0]+".displayMode",displayMode)
