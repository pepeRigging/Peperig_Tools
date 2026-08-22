# -*- coding: utf-8 -*-
__author__ = "jose lozano"

__version__ = "1.0"
__maintainer__ = "jose lozano"
__email__ = "Jose.lozano@3Doubles.com"
__status__ = "WIP"

from PySide6 import QtWidgets as wdg
from PySide6 import QtGui as gui
from PySide6 import QtCore as core
from PySide6.QtWidgets import QMessageBox as QMB
import maya.cmds as cmds
import maya.OpenMayaUI as mui
import shiboken6
import time
import math
import functools
import pymel.core as pm

import sys
import subprocess
mainWindow=None

try:
    import pymel.core as pm
except ImportError:
    # Si PyMel no existe, se instala automáticamente en el Python de Maya
    print("PyMel no detectado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymel"])
    import pymel.core as pm

class secondary(wdg.QWidget):
    def __init__(self,seleccion):
        super(secondary,self).__init__()
        ## usamos self para importar
        self.resize(100,500)
        self.seletObj=seleccion
        self.setWindowFlags(core.Qt.WindowStaysOnTopHint)
        self.createUI()
    ## interface
    def createUI(self):
        mainLayout=wdg.QHBoxLayout(self)
        mainLayout.setAlignment(core.Qt.AlignTop)
        
        boxes=wdg.QGroupBox()
        boxes_Lyt=wdg.QHBoxLayout(boxes)
        
        labeling=wdg.QLabel("Driver Node :")
        self.EnumingControl=wdg.QLineEdit(self.seletObj)
        self.boton=wdg.QPushButton("<<")
        labeling2=wdg.QLabel("Name Display :")
        self.EnumingDysplay=wdg.QLineEdit(self.seletObj)
        self.botonDelete=wdg.QPushButton("X")
        self.botonDelete.setStyleSheet('QPushButton {color: red;}')

        
        self.botonDelete.released.connect(self.deletetarget)
        self.boton.released.connect(self.changeDriverName)
        
        boxes_Lyt.addWidget(labeling)
        boxes_Lyt.addWidget(self.EnumingControl)
        boxes_Lyt.addWidget(self.boton)
        boxes_Lyt.addWidget(labeling2)
        boxes_Lyt.addWidget(self.EnumingDysplay)
        boxes_Lyt.addWidget(self.botonDelete)
        
        mainLayout.addWidget(boxes)
    
    def changeDriverName(self):
        sel=cmds.ls(sl=True)
        if len(sel)!=1:
            cmds.warning("need 1 only")
            return
        self.EnumingControl.setText(sel[0])
        
    def deletetarget(self):
        self.close()
        SpaceSwitcherTool.lisVentanas.remove(self)
        SpaceSwitcherTool.Switches.remove(self)
        self.setAttribute(core.Qt.WA_DeleteOnClose)
    
    def cerrarEnum(self):
        self.close()
        self.setAttribute(core.Qt.WA_DeleteOnClose)
        

        
class SpaceSwitcherTool(wdg.QMainWindow):
    lisVentanas=[]
    Switches=[]
    def __init__(self):
        super(SpaceSwitcherTool,self).__init__()
        ## usamos self para importar
        self.setWindowTitle("Space Switcher Tool v{}".format(__version__))
        self.setWindowFlags(core.Qt.WindowStaysOnTopHint)
        self.resize(500,500)
        self.createUI()
        del self.Switches[:]
        del self.lisVentanas[:]

    ## interface
    def createUI(self):
        #crear layoutMain y widget
        centralWidget=wdg.QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout=wdg.QVBoxLayout(centralWidget)
        
        tabs=wdg.QTabWidget()
        creation_tab=wdg.QWidget()
        creacion_Lyt=wdg.QVBoxLayout(creation_tab)
        tabs.addTab(creation_tab,"Constraint")
        
        edit_tab=wdg.QWidget()
        tabs.addTab(edit_tab,"Visibility")
        mainLayout.addWidget(tabs)
        
        ##Group boxes
                ##info group
        grupoinfo= wdg.QGroupBox("Info")
        grupoinfo.setStyleSheet("QGroupBox::title {subcontrol-position : left top;"
                                "background-color: transparent;"
                                "padding-top: 0px;"
                                "padding-left: 10px;"
                                "color: white}"
                                "QGroupBox {font-weight: bold;}")
        info_Lyt=wdg.QGridLayout(grupoinfo)
        info_Lyt.setColumnStretch(0,0)
        info_Lyt.setColumnStretch(1,0)
        info_Lyt.setColumnStretch(2,1)
                ## spaces group
        grupospaces= wdg.QGroupBox("Spaces")
        grupospaces.setStyleSheet("QGroupBox::title {subcontrol-position : left top;"
                                "background-color: transparent;"
                                "padding-top: 0px;"
                                "padding-left: 10px;"
                                "color: white}"
                                "QGroupBox {font-weight: bold;}")
        spaces_Lyt=wdg.QVBoxLayout(grupospaces)
        
        ###############
                            ##info Space contenido
        self.spaces_Btn=wdg.QPushButton("Add Spaces")
        ##dinamic window
        self.dinamicspaceswitget=wdg.QScrollArea()
        #self.dinamicspaceswitget.setSizePolicy(wdg.QSizePolicy.MinimumExpanding,wdg.QSizePolicy.Fixed)
        
        self.dinamicspaceswitget.setWidgetResizable(True)
        self.scrollwitget=wdg.QWidget()
        self.scrollwitget.setSizePolicy(wdg.QSizePolicy.Expanding,wdg.QSizePolicy.Maximum)
        self.dinamicspaceswitget.setWidget(self.scrollwitget)
        self.dinamicspacesLayout=wdg.QVBoxLayout(self.scrollwitget)
        self.dinamicspaceswitget.setVerticalScrollBarPolicy(core.Qt.ScrollBarAlwaysOn)
        spaces_Lyt.addWidget(self.dinamicspaceswitget)
        ## add to main lyt
        spaces_Lyt.addWidget(self.spaces_Btn)
        spaces_Lyt.addWidget(self.dinamicspaceswitget)
        
        ###############
                            ##info group contenido
        labeling=["Target Node","Parent Grp","Switch Attr","Switch Constraint"]
        self.buttoninfo=[]
        self.infoNamingLine=[]
        for i in range(1,5):
            for j in range(1,4):
                if j==1:
                    info_Lyt.addWidget(wdg.QLabel(labeling[i-1]),i,j)
                elif j==2:
                    text=wdg.QLineEdit()
                    info_Lyt.addWidget(text,i,j)
                    self.infoNamingLine.append(text)
                elif j==3 and i!=4 and i!=3:
                    button=wdg.QPushButton("<<")
                    info_Lyt.addWidget(button,i,j)
                    self.buttoninfo.append(button)
                elif j==3 and i==3:
                    pass
                elif j==3 and i==4:
                    constraint_cb=wdg.QComboBox()
                    constraint_cb.addItems(["parentConstraint","pointConstraint","orientConstraint"])
                    info_Lyt.addWidget(constraint_cb,i,j)
                    self.buttoninfo.append(constraint_cb)
        self.infoNamingLine[0].setPlaceholderText("Object where attribute appear")
        self.infoNamingLine[1].setPlaceholderText("Object to constraint")
        self.infoNamingLine[2].setPlaceholderText("Name attribute")
        self.infoNamingLine[3].setPlaceholderText("Type of constraint")
        ############################
                ##creacion add widgets
        ###################
        ##add groupboxex
        creacion_Lyt.addWidget(grupoinfo)
        creacion_Lyt.addWidget(grupospaces)
        
        ##add creation and delete buttons
        self.delete_bt=wdg.QPushButton("Delete Space")
        self.create_bt=wdg.QPushButton("Generate")
        
        ## add button
        creacion_Lyt.addWidget(self.delete_bt)
        creacion_Lyt.addWidget(self.create_bt)
        

        ##############
        ######          COMMANDS
        ###############
        self.delete_bt.released.connect(self.deleteSpaces)
        self.create_bt.released.connect(self.generateSpaces)
        
        self.buttoninfo[0].released.connect(self.getTarget)
        self.buttoninfo[1].released.connect(self.getParentGrp)
        self.buttoninfo[2].currentIndexChanged.connect(self.getConstraint)
        
        
        self.spaces_Btn.released.connect(self.addSpacesWindows)
    ##############
        ######          FUNCTIONS
        ###############
    def addSpacesWindows(self):
        sel=cmds.ls(sl=True)
        if len(sel)==0:
            cmds.warning("need selection")
            return
            
        for name in sel:
            enumeres=secondary(name)
            self.Switches.append(enumeres)
            self.lisVentanas.append(enumeres)
            for each in self.lisVentanas:
                if not cmds.window(each,q=True,exists=True):
                    self.dinamicspacesLayout.addWidget(each)
        
        
        
    def pasteNameselected(self,Target):
        sel=pm.ls(sl=True)
        if len(sel)!=1:
            cmds.warning("need 1 selection")
            return
        if Target==True:
            self.infoNamingLine[0].setText(sel[0].name())
        else:
            self.infoNamingLine[1].setText(sel[0].name())
    def getTarget(self):
        self.pasteNameselected(True)
    
    def getConstraint(self):
        self.infoNamingLine[3].setText(self.buttoninfo[2].currentText())
        
    def getParentGrp(self):
        self.pasteNameselected(False)
    
    def createSystem(self): 
        if cmds.attributeQuery(self.infoNamingLine[2].text(), ex=True ,node=self.infoNamingLine[0].text()):
            cmds.warning("Name attribute exist already")
            return
        driver=[]
        driverNaming=[]
        for each in self.Switches:
            driver.append(each.EnumingControl.text())
            driverNaming.append(each.EnumingDysplay.text())
            
        if len(driver)<2:
            cmds.warning("need Add 2 spaces")
            return
        

                                                ##comprobar si tiene conexiones y si tiene STOP
        
        typeConstraint=self.infoNamingLine[3].text() 
        attr=[".tx",".ty",".tz",".rx",".ry",".rz",".sx",".sy",".sz"]
        if typeConstraint=="parentConstraint":
            for each in attr:
                if ".tx" in each:
                    if (cmds.listConnections(self.infoNamingLine[1].text()+ each)):
                        cmds.warning("not able to create Parent :Target has conexion")
                        return
            constraint = cmds.parentConstraint(driver,self.infoNamingLine[1].text(), mo=1)[0]
            weight=cmds.parentConstraint(constraint,wal=True,q=True)
        if typeConstraint=="pointConstraint":
            for each in attr:
                if ".tx" in each:
                    if (cmds.listConnections(self.infoNamingLine[1].text()+ each)):
                        cmds.warning("not able to create Point :Target has conexion,")
                        return
            constraint = cmds.pointConstraint(driver,self.infoNamingLine[1].text(), mo=1)[0]
            weight=cmds.pointConstraint(constraint,wal=True,q=True)
        if typeConstraint=="orientConstraint":
            for each in attr:
                if ".rx" in each:
                    if (cmds.listConnections(self.infoNamingLine[1].text()+ each)):
                        cmds.warning("not able to create orient :Target has conexion")
                        return
            constraint = cmds.orientConstraint(driver,self.infoNamingLine[1].text(), mo=1)[0]
            weight=cmds.orientConstraint(constraint,wal=True,q=True)
            
            
        defaultState=0
        ## crear attribute
        cmds.addAttr(self.infoNamingLine[0].text(),ln=self.infoNamingLine[2].text(), at="enum", en=":".join(driverNaming), dv=defaultState,k=1)
        
        ## crear choices setups
        for each in range(len(driver))[::-1]:
            valorChoice= [1 if num==each else 0 for num in range(len(driver))]
                                                        ##crear bien los choice para mirar si EXISTEN
            choice = cmds.createNode("choice", n="C_enumSwitch"+str(each) + "_CHE")
            cmds.connectAttr(self.infoNamingLine[0].text() + "."+ self.infoNamingLine[2].text() ,choice + ".selector")
            for inp in range (len(valorChoice)):
                cmds.setAttr(choice + ".input[{0}]".format(inp),valorChoice[inp])
            
            cmds.connectAttr(choice + ".output",constraint + "." + weight[each] )
        
            ## conect choice to constraint
        
        
    def createConstraint(self,drivers,driven):
        costraint = cmds.parentConstraint(drivers,driven, mo=1)[0]
        return costraint
        
    def deleteSpaces(self):
        for each in self.Switches:
            each.cerrarEnum()
        del self.lisVentanas[:]
        del self.Switches[:]
        
    def generateSpaces(self):
        self.createSystem()
        
    def closeEvent(self,event):
        event.accept()    
## iniciar la ventana y comprobar si existe
def run():
    global mainWindow
    if not mainWindow or not cmds.window(mainWindow,q=True,exists=True):
        mainWindow = SpaceSwitcherTool()
    mainWindow.show()

run()