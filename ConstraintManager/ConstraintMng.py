# -*- coding: utf-8 -*-
__author__ = "jose lozano"
__version__ = "1.0"
__maintainer__ = "jose lozano"
__email__ = "contact@peperig.com"
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
#import pymel.core as pm

import sys
import subprocess

try:
    import pymel.core as pm
except ImportError:
    # Si PyMel no existe, se instala automáticamente en el Python de Maya
    print("PyMel no detectado. Instalando...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymel"])
    import pymel.core as pm
    
mainWindow=None
    
class ConstraintMng(wdg.QMainWindow):
    def __init__(self):
        super(ConstraintMng,self).__init__()
        ## usamos self para importar
        self.setWindowTitle("Constraint Manager Tool v{}".format(__version__))
        self.resize(400,600)
        self.setWindowFlags(core.Qt.WindowStaysOnTopHint)
        self.createUI()

    ## interface
    def createUI(self):
        #crear layoutMain y widget
        centralWidget=wdg.QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout=wdg.QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(0,15,0,0)
        ## create groupBoxes
        Type_gb=wdg.QGroupBox("Type")
        typeLayout=wdg.QHBoxLayout(Type_gb)
        Type_gb.setSizePolicy(wdg.QSizePolicy.Expanding,wdg.QSizePolicy.Fixed)
        Type_gb.setStyleSheet("QGroupBox::title {subcontrol-position : top;"
                                "background-color: transparent;"
                                "padding-top: 10px;"
                                "color: white}"
                                "QGroupBox {font-weight: bold;}")
        Transforms_gb=wdg.QGroupBox("Offset-Transform")
        transformLayout=wdg.QHBoxLayout(Transforms_gb)
        
        Transforms_gb.setSizePolicy(wdg.QSizePolicy.Expanding,wdg.QSizePolicy.Fixed)
        Transforms_gb.setStyleSheet("QGroupBox::title {subcontrol-position : top;"
                                    "background-color: transparent;"
                                    "padding-top: 10px;"
                                    "color: white}"
                                    "QGroupBox {font-weight: bold;}")
                                
        listConstraints_gb=wdg.QGroupBox("List Constraint")
        listLayout=wdg.QVBoxLayout(listConstraints_gb)
        listConstraints_gb.setStyleSheet("QGroupBox::title {subcontrol-position : top;"
                                        "background-color: transparent;"
                                        "padding-top: 10px;"
                                        "color: white}"
                                        "QGroupBox {font-weight: bold;}")                                
        mainLayout.addWidget(Type_gb)
        mainLayout.addWidget(Transforms_gb)
        mainLayout.addWidget(listConstraints_gb)

        ## radial buttons types
        self.parent_rb=wdg.QRadioButton("Parent")
        self.point_rb=wdg.QRadioButton("Point")
        self.orient_rb=wdg.QRadioButton("Orient")
        
        typeLayout.addWidget(self.parent_rb)
        typeLayout.addWidget(self.point_rb)
        typeLayout.addWidget(self.orient_rb)
        
        ## transform check list constraints
        leftWidgets=wdg.QWidget()
        leftLayout=wdg.QVBoxLayout(leftWidgets)
        
        midWidgets=wdg.QWidget()
        midLayout=wdg.QVBoxLayout(midWidgets)
        
        rightWidgets=wdg.QWidget()
        rightLayout=wdg.QVBoxLayout(rightWidgets)
        
        ## offsets
        self.offset_cb=wdg.QCheckBox("Offset")
        leftLayout.addWidget(self.offset_cb)    
        ## translates
        self.tx_cb=wdg.QCheckBox("translate X")
        self.ty_cb=wdg.QCheckBox("translate Y")
        self.tz_cb=wdg.QCheckBox("translate Z")
        
        midLayout.addWidget(self.tx_cb)
        midLayout.addWidget(self.ty_cb)
        midLayout.addWidget(self.tz_cb) 
        ## rotates
        self.rx_cb=wdg.QCheckBox("rotate X")
        self.ry_cb=wdg.QCheckBox("rotate Y")
        self.rz_cb=wdg.QCheckBox("rotate Z")
        
        rightLayout.addWidget(self.rx_cb)
        rightLayout.addWidget(self.ry_cb)
        rightLayout.addWidget(self.rz_cb)
        
        transformLayout.addWidget(leftWidgets)
        transformLayout.addWidget(midWidgets)
        transformLayout.addWidget(rightWidgets)

        ## qtablWidget
        self.filter_wdg=wdg.QLineEdit("")
        listLayout.addWidget(self.filter_wdg)
        
        self.table_wdg=wdg.QTableWidget()
        self.table_wdg.setColumnCount(4)

        
        Drivers=wdg.QTableWidgetItem("Drivers")
        Driven=wdg.QTableWidgetItem("Driven")
        Type=wdg.QTableWidgetItem("Type")
        Name=wdg.QTableWidgetItem("ConstraintName")
        
        self.table_wdg.setHorizontalHeaderItem(0,Drivers)
        self.table_wdg.setHorizontalHeaderItem(1,Driven)
        self.table_wdg.setHorizontalHeaderItem(2,Type)
        self.table_wdg.setHorizontalHeaderItem(3,Name)
        
        header = self.table_wdg.horizontalHeader()
        header.setSectionResizeMode(wdg.QHeaderView.Stretch)        

        listLayout.addWidget(self.table_wdg)

        ## BOTONES FINALES
        ButtonsWidgets=wdg.QWidget()
        ButtonsLayout=wdg.QHBoxLayout(ButtonsWidgets)
        
        self.createBtn=wdg.QPushButton("Create")
        self.changeBtn=wdg.QPushButton("Change")
        self.DeleteBtn=wdg.QPushButton("Delete")
        self.RefreshBtn=wdg.QPushButton("Refresh")
        
        ButtonsLayout.addWidget(self.createBtn)
        ButtonsLayout.addWidget(self.changeBtn)
        ButtonsLayout.addWidget(self.DeleteBtn)
        ButtonsLayout.addWidget(self.RefreshBtn)
        ##calls function
        self.createBtn.released.connect(self.__create)
        self.changeBtn.released.connect(self.__change)
        self.DeleteBtn.released.connect(self.__delete)
        self.RefreshBtn.released.connect(self.__refresh)
        
        self.parent_rb.clicked.connect(self.__changeStateCheckboxes)
        self.point_rb.clicked.connect(self.__changeStateCheckboxes)
        self.orient_rb.clicked.connect(self.__changeStateCheckboxes)
        self.table_wdg.itemClicked.connect(self.__updateCheckboxes)
        
        self.filter_wdg.textChanged.connect(self.__changeText)
        listLayout.addWidget(ButtonsWidgets)
        
    def __changeText(self):
        rowCounts = self.table_wdg.rowCount()
        text_to_find = self.filter_wdg.text()  
        for each in range(rowCounts):
            found = False
            if text_to_find in str(self.table_wdg.item(each, 0).text()):
                found = True
            elif text_to_find in str(self.table_wdg.item(each, 1).text()):
                found = True
            elif text_to_find in str(self.table_wdg.item(each, 2).text()):
                found = True
            if found:
                self.table_wdg.showRow(each)
            else:
                self.table_wdg.hideRow(each)
                
    def __addElementToTable(self, element1, element2, tipo,name):
        # Check if duplicated
        items = self.table_wdg.findItems(element1, core.Qt.MatchExactly)
        if items:
            for item in items:
                if (str(self.table_wdg.item(item.row(), 0).text())== element1):
                    if (str(self.table_wdg.item(item.row(), 1).text())== element2):
                        if (str(self.table_wdg.item(item.row(), 2).text())== tipo):
                            if (str(self.table_wdg.item(item.row(), 3).text())== name):
                                return

        # Comprobamos que linea sera la siguiente en la que insertaremos los datos
        rowPosition = self.table_wdg.rowCount()
        # Insertamos los datos en la linea correspondiente
        self.table_wdg.insertRow(rowPosition)
        self.table_wdg.setItem(rowPosition, 0, wdg.QTableWidgetItem(element1))
        self.table_wdg.setItem(rowPosition, 1, wdg.QTableWidgetItem(element2))
        self.table_wdg.setItem(rowPosition, 2, wdg.QTableWidgetItem(tipo))
        self.table_wdg.setItem(rowPosition, 3, wdg.QTableWidgetItem(name))
        
    def __Constraint(self,changeOption):
        selection = pm.ls(selection=True)
        # Comprobamos si el usuario ha seleccionado dos elementos de la escena
        if (len(selection) < 2):
            cmds.warning('atleat 2 objects selected necesary')
            return
    
        target=pm.ls(selection[-1])
        driver=pm.ls(selection[:-1])
        
        if self.parent_rb.isChecked()==0 and self.point_rb.isChecked()==0 and self.orient_rb.isChecked() ==0:
            cmds.warning("Need to select a Type")
            return
        ##esta parte debo cambiarla porque no permite distintos constraints
        if(self.parent_rb.isChecked()):
            if ((target[0].tx.isConnected() or
                 target[0].ty.isConnected() or
                 target[0].tz.isConnected() or
                 target[0].rx.isConnected() or
                 target[0].ry.isConnected() or
                 target[0].rz.isConnected())
                    and not changeOption):
                        cmds.warning("already conected")
                        return
        if(self.point_rb.isChecked()):
            if ((target[0].tx.isConnected() or
                 target[0].ty.isConnected() or
                 target[0].tz.isConnected())
                    and not changeOption):
                        cmds.warning("already conected")
                        return    
        if(self.orient_rb.isChecked()):
            if ((target[0].rx.isConnected() or
                 target[0].ry.isConnected() or
                 target[0].rz.isConnected())
                    and not changeOption):
                        cmds.warning("already conected")
                        return    

        offset = self.offset_cb.isChecked()
        skipTranslate = []
        if(self.tx_cb.isChecked() is False):
            skipTranslate.append("x")
        if(self.ty_cb.isChecked() is False):
            skipTranslate.append("y")
        if(self.tz_cb.isChecked() is False):
            skipTranslate.append("z")
        skipRotate = []
        if(self.rx_cb.isChecked() is False):
            skipRotate.append("x")
        if(self.ry_cb.isChecked() is False):
            skipRotate.append("y")
        if(self.rz_cb.isChecked() is False):
            skipRotate.append("z")
        # Comprobamos que tipo de constraint se va a crear
        if(self.parent_rb.isChecked()):
            tipo = "Parent"
        if(self.point_rb.isChecked()):
            tipo = "Point"
        if(self.orient_rb.isChecked()):
            tipo = "Orient"
        
        if isinstance(driver, list): 
            contraints = ','.join(str(e) for e in driver) 

        if(tipo == "Parent"):
            if  len(skipTranslate)==3 and len(skipRotate)==3:
                cmds.warning("not selected any transform")
                pass
            else:
                cst=pm.parentConstraint(driver, target,
                                    mo=offset, st=skipTranslate, sr=skipRotate)
                      ## los drivers me dan la batalla              
                self.__addElementToTable(str(contraints), str(target[0]), tipo,str(cst.name()))
                
        if(tipo == "Point"):
            if  len(skipTranslate)==3:
                cmds.warning("not selected any transform")
                pass
            else:
                cst=pm.pointConstraint(driver, target,
                                   mo=offset, sk=skipTranslate)
                self.__addElementToTable(str(contraints), str(target[0]), tipo,str(cst.name()))
        if(tipo == "Orient"):
            if  len(skipRotate)==3:
                cmds.warning("not selected any transform")
                pass
            else:
                cst=pm.orientConstraint(driver, target,
                                    mo=offset, sk=skipRotate)
                self.__addElementToTable(str(contraints), str(target[0]), tipo,str(cst.name()))
        
    def __deleteConstraint(self):
        delete=False
        # Comprobamos cuantas filas ha seleccionado el usuario
        rowSelected = self.table_wdg.selectionModel().selectedRows()
        # Si no hay ninguna linea seleccionada salimos
        if (len(rowSelected) == 1):
            # Almacenamos el indice de la fila seleccionada
            row = self.table_wdg.currentRow()
            # Almacenamos los campos de las columnas de la fila seleccionada
            rowFields = []
            rowFields.append(self.table_wdg.item(row, 0).text())
            rowFields.append(self.table_wdg.item(row, 1).text())
            rowFields.append(self.table_wdg.item(row, 2).text())
            # Seleccionamos el driver y el driven
            target= rowFields[1]
            drivers=[]
            if "," in rowFields[0]:
                driver=rowFields[0].split(",")
                for each in driver:
                    drivers.append(each)
            else:
                drivers.append(rowFields[0])
            
            for each in drivers:
                cmds.select(each,add=True)
                
            cmds.select(target,add=True)
            selection = cmds.ls(sl=True)

            # Segun el tipo de constraint seleccionado, lo eliminaremos con
            # el metodo correspondiente

            if rowFields[2] == "Parent":
                cmds.parentConstraint(selection[:-1],selection[-1], e=True, rm=True)
            if rowFields[2] == "Point":
                pm.pointConstraint(selection[:-1], selection[-1], e=True, rm=True)
            if rowFields[2] == "Orient":
                pm.orientConstraint(selection[:-1], selection[-1], e=True, rm=True)
            # Una vez eliminado, lo eliminamos tambien de la tabla
            drivers=[]
            if "," in rowFields[0]:
                driver=rowFields[0].split(",")
                for each in driver:
                    drivers.append(each)
            else:
                drivers.append(rowFields[0])
            
            for each in drivers:
                cmds.select(each,add=True)
                
            pm.select(target,add=True)
            selection = pm.ls(sl=True)

            index = rowSelected[0].row()
            self.__removeElementFromTable(index)
            delete=True
        else:
            cmds.warning("not row selected")
        return delete

    def __removeElementFromTable(self, index):
        self.table_wdg.removeRow(index)    
    
    
    def __refreshTable(self):
        countRows=self.table_wdg.rowCount()
        for each in range(countRows)[::-1]:
            self.table_wdg.removeRow(each)  
        
        # Seleccionamos todos los constraints que haya en la escena
        allConst = pm.ls(type=[
            "parentConstraint",
            "pointConstraint",
            "orientConstraint"
            ])
        # Iteramos por todos ellos, obteniendo su driver y su driven,
        # ademas de su tipo, para agregarlo a la tabla
        for const in allConst:
            name = str(const.name())

            inputs = const.listConnections(p=True, source=False, destination=True)
            # Con los inputs, y el metodo getTargetList, obtenemos el
            # driver y el driven
            driver = const.getTargetList()
            if isinstance(driver, list): 
                contraints = ','.join(str(e) for e in driver) 
            # Los inputs vienen dados en un array, como el nombre viene
            # separado por un punto, le hacemos un split, y nos quedamos
            # con la primera parte, que es la que nos interesa
            driven = inputs[0].split(".")

            # Obtenemos tambien el tipo de constraint
            if (const.type() == "parentConstraint"):
                tipo = "Parent"
            if (const.type() == "pointConstraint"):
                tipo = "Point"
            if (const.type() == "orientConstraint"):
                tipo = "Orient"
            # Agregamos el elemento a la tabla
            self.__addElementToTable(str(contraints), str(driven[0]), tipo,name)
    
    def __changeConstraint(self):
        # Eliminamos el constraint seleccionado en la lista
        if pm.ls(selection=True):
            oldselect= pm.ls(selection=True)
            cmds.warning("need to deselect to do changes")
                    
        else:##nothingselected
            delete=self.__deleteConstraint()
            
            if delete==True:
                # creamos el constraint con la nueva configuracion
                self.__Constraint(True)
                # Actualizamos el hecho de que unos checkboxes esten o
                # o no habilitados para su configuracion
                if(self.parent_rb.isChecked()):
                    self.__changeStateCheckboxes()
                if(self.point_rb.isChecked()):
                    self.__changeStateCheckboxes()
                if(self.orient_rb.isChecked()):
                    self.__changeStateCheckboxes()    

    def __changeStateCheckboxes(self):
        # Para el caso de que el constraint sea tipo parent, podra
        # configurar cualquier checkbox
        if self.parent_rb.isChecked():
            self.tx_cb.setEnabled(True)
            self.ty_cb.setEnabled(True)
            self.tz_cb.setEnabled(True)
            self.rx_cb.setEnabled(True)
            self.ry_cb.setEnabled(True)
            self.rz_cb.setEnabled(True)
        # Para el caso de que el constraint sea tipo point, podra
        # configurar solo los checkboxes de traslacion y el offset
        if self.point_rb.isChecked():
            self.tx_cb.setEnabled(True)
            self.ty_cb.setEnabled(True)
            self.tz_cb.setEnabled(True)
            self.rx_cb.setEnabled(False)
            self.ry_cb.setEnabled(False)
            self.rz_cb.setEnabled(False)
        # Para el caso de que el constraint sea tipo parent, podra
        # configurar solo los checkboxes de rotacion y el offset
        if self.orient_rb.isChecked():
            self.tx_cb.setEnabled(False)
            self.ty_cb.setEnabled(False)
            self.tz_cb.setEnabled(False)
            self.rx_cb.setEnabled(True)
            self.ry_cb.setEnabled(True)
            self.rz_cb.setEnabled(True)
    
    def __updateCheckboxes(self):
        # Obtenemos la fila seleccionada
        row = self.table_wdg.currentRow()
        # Guardamos los datos de la fila seleccionada
        rowFields = []
        rowFields.append(self.table_wdg.item(row, 0).text())
        rowFields.append(self.table_wdg.item(row, 1).text())
        rowFields.append(self.table_wdg.item(row, 2).text())
        # Cambiamos el radial segun el tipo de constraint de la fila
        # seleccionada, y listamos todos los constraints de ese tipo
        if rowFields[2] == "Parent":
            self.parent_rb.setChecked(True)
            self.__changeStateCheckboxes()
            allConst = pm.ls(type="parentConstraint")
        if rowFields[2] == "Point":
            self.point_rb.setChecked(True)
            self.__changeStateCheckboxes()
            allConst = pm.ls(type="pointConstraint")
        if rowFields[2] == "Orient":
            self.orient_rb.setChecked(True)
            self.__changeStateCheckboxes()
            allConst = pm.ls(type="orientConstraint")    
        # Buscamos el constraint en la lista de constraints, para ello,
        # obtenemos todos los targets y comprobamos si el elemento afectado
        # por el constarint aparece en la lista (si contiene el driven)
                                
        i = 0
        for const in allConst:
            targetlist = const.getTargetList()
            if len(targetlist)>1:
                driver=targetlist[0] + ","+  targetlist[1]
            else:    
                driver=targetlist[0]
                
            if driver.find(rowFields[0]) != -1:
                if const.find(rowFields[1]) != -1:
                    break
            i = i + 1
        # Obtenemos todos los atributos conectados al constraint
            
        inputs = allConst[i].listConnections(
            p=True, source=False, destination=True)
            
        # Desactivamos todos los checked
        self.tx_cb.setChecked(False)
        self.ty_cb.setChecked(False)
        self.tz_cb.setChecked(False)
        self.rx_cb.setChecked(False)
        self.ry_cb.setChecked(False)
        self.rz_cb.setChecked(False)
        # Si un atributo aparece en la lista de inputs, es decir,
        # esta conectado, es porque esta afectado,de modo que se
        # activara el checkbox
        for atributo in inputs:
            if atributo.find("translateX") != -1:
                self.tx_cb.setChecked(True)
            if atributo.find("translateY") != -1:
                self.ty_cb.setChecked(True)
            if atributo.find("translateZ") != -1:
                self.tz_cb.setChecked(True)
            if atributo.find("rotateX") != -1:
                self.rx_cb.setChecked(True)
            if atributo.find("rotateY") != -1:
                self.ry_cb.setChecked(True)
            if atributo.find("rotateZ") != -1:
                self.rz_cb.setChecked(True)
        # Establecemos los flags de offset para rotacion y traslacion
        offsetTranslate = False
        offsetRotate = False
        if len(targetlist)==1:
            #  Comprobamos si la posicion es la misma para ambos elementos
            translateDriver = pm.getAttr(rowFields[0] + '.translate')
            translateDriven = pm.getAttr(rowFields[1] + '.translate')
            #  Comprobamos tambien si la traslacion es la misma
            rotateDriver = pm.getAttr(rowFields[0] + '.rotate')
            rotateDriven = pm.getAttr(rowFields[1] + '.rotate')
            # Si la posicion o la rotacion es distinta, es porque mantienen
            # un offset
            if translateDriven != translateDriver:
                offsetTranslate = True
            if rotateDriven != rotateDriver:
                offsetRotate = True
            # Desactivamos inicialmente el checkbox del offset
            self.offset_cb.setChecked(False)
            # Se establece el valor del checkbox de offset a lo analizado
            if rowFields[2] == "Parent":
                if (offsetTranslate or offsetRotate):
                    self.offset_cb.setChecked(True)
            if rowFields[2] == "Point":
                if (offsetTranslate):
                    self.offset_cb.setChecked(True)
            if rowFields[2] == "Orient":
                if (offsetRotate):
                    self.offset_cb.setChecked(True)
                    
     ##############################################################   
    def __create(self):
        self.__Constraint(False)
        
    def __change(self):
        self.__changeConstraint()
        
    def __delete(self):
        self.__deleteConstraint()
        
    def __refresh(self):
        self.__refreshTable()
        
    def closeEvent(self,event):
        event.accept()    
        
## iniciar la ventana y comprobar si existe
def run():
    global mainWindow
    if not mainWindow or not cmds.window(mainWindow,q=True,exists=True):
        mainWindow = ConstraintMng()
    mainWindow.show()