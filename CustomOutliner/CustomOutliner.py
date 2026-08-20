# -*- coding: utf-8 -*-
__author__ = "jose lozano"
__version__ = "1.0"
__maintainer__ = "jose lozano"
__email__ = "contact@peperig.com"
__status__ = "still WIP"

import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance
from PySide6 import QtWidgets as wdg
from PySide6 import QtGui as gui
from PySide6 import QtCore as core
import maya.cmds as mc
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

class OutlinerTool(wdg.QMainWindow):

    def __init__(self):
        super(OutlinerTool,self).__init__()
        ## usamos self para importa
        self.setWindowTitle("Outliner Custom  v{}".format(__version__))
        self.resize(400,200)
        self.setWindowFlags(core.Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(core.Qt.StrongFocus)
        self.createUI()

    ## interface
    def createUI(self):
        #crear layoutMain y widget
        centralWidget=wdg.QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout=wdg.QHBoxLayout(centralWidget)
        
        self.mainSplit=wdg.QSplitter(core.Qt.Vertical)

        mainLayout.addWidget(self.mainSplit)
        
        self.createOutliner()
        self.refresh()
    
    def createOutliner(self):
        
        objectSetFilter = pm.itemFilter(byType='nurbsCurve')
      
        newOutliner = mc.window(title="Outliner (Custom)", iconName="Outliner*", widthHeight=(250,100))
        frame = mc.frameLayout(labelVisible = False)     
        panel = mc.outlinerPanel()    

        self.customOutliner = pm.outlinerPanel(panel, query=True,outlinerEditor=True)

        pm.outlinerEditor(self.customOutliner,edit=True,setFilter=objectSetFilter,filter=objectSetFilter)
            
        ptr = omui.MQtUtil.findControl(self.customOutliner)
        outlinerWidget = wrapInstance(int(ptr), wdg.QWidget)

        
        self.typeEdit=wdg.QComboBox()
        self.typeEdit.addItems(["transform","nurbsCurve","mesh","joint","Constraint","locator","Light","camera","nurbsSurface"])
        ### RIGHT SIDE SPLITTER
        rightWidget=wdg.QWidget()

        rightLayout=wdg.QFormLayout(rightWidget)
        
        rightLayout.addRow("Type : " ,self.typeEdit )
        self.mainSplit.addWidget(rightWidget)
        self.mainSplit.addWidget(outlinerWidget)
        self.mainSplit.setStretchFactor(0,0)
        self.mainSplit.setStretchFactor(1,1)
        self.typeEdit.currentIndexChanged.connect(self.refresh)
        
        
    def keyPressEvent(self, e):
            if e.key() == core.Qt.Key_F:
                pm.outlinerEditor(self.customOutliner,edit=True,sc=True)
            
    def refresh(self):
        if self.typeEdit.currentText()== "Light":

            objectSetFilter = pm.itemFilter(byType=("aiAreaLight","ambientLight","aiSkyDomeLight","aiPhotometricLight","aiLightPortal"))

            pm.outlinerEditor(self.customOutliner,edit=True,setFilter=objectSetFilter,filter=objectSetFilter)
        
        elif self.typeEdit.currentText()== "Constraint":
            objectSetFilter = pm.itemFilter(byType=("parentConstraint","orientConstraint","pointConstraint","scaleConstraint","aimConstraint"))

            pm.outlinerEditor(self.customOutliner,edit=True,setFilter=objectSetFilter,filter=objectSetFilter)
        else:
            objectSetFilter = pm.itemFilter(byType=self.typeEdit.currentText())
            pm.outlinerEditor(self.customOutliner,edit=True,setFilter=objectSetFilter,filter=objectSetFilter)
    
   
def run():
    global mainWindow
    if not mainWindow or not mc.window(mainWindow,q=True,exists=True):
        mainWindow = OutlinerTool()
    mainWindow.show()
    
run()