# Peperig Tools 🛠️

A collection of Python tools for Autodesk Maya designed to streamline and speed up Rigging and Technical Development workflows.

## ✨ Included Tools

### 1. Constraint Manager 🔗

* **Centralized Management:** Manage and organize multiple types of constraints from a clean and intuitive interface.
* **Hierarchy Automation:** Reduce manual errors when connecting and managing complex node hierarchies.

**Demo**
https://youtu.be/oSyYuMWCV2M?si=1ZVym-O0YxOOunVR
### 2. Custom Outliner 👁️

* **Advanced Filtering:** Display only the nodes you need for your rig, such as joints, controls, locators, and more.
* **Clean Organization:** Reduce the visual clutter of Maya's native Outliner, making it faster and easier to work with complex rigs.

**Demo**
https://youtu.be/6x2vQmQfe5Q?si=ZMnr2HReByCICJ45
## 🚀 Installation & Usage

1. Download or clone this repository into your Maya scripts folder:

```bash
git clone https://github.com/pepeRigging/Peperig_Tools.git
```

2. Open Maya's **Script Editor**, switch to the **Python** tab, and run the tool you want to use:

```python
# Open the Constraint Manager:
import ConstraintMng
import importlib
importlib.reload(ConstraintMng)

ConstraintMng.run()

# Open the Custom Outliner:
import CustomOutliner
import importlib
importlib.reload(CustomOutliner)

CustomOutliner.run()
```

## 📝 Requirements

* Autodesk Maya 2025 or later
* Python 3

---

*Developed with 🛠️ by* **pepeRigging**.

If you have any suggestions or find a bug, feel free to open an **Issue**!

##############################################################################################################################################
# Peperig Tools 🛠️

Un conjunto de herramientas de Python para Autodesk Maya diseñado para optimizar y acelerar los flujos de trabajo de Rigging y desarrollo técnico.

## ✨ Herramientas incluidas

### 1. Constraint Manager 🔗
* **Gestión centralizada:** Controla y organiza múltiples tipos de constraints desde una interfaz limpia.
* **Automatización de jerarquías:** Reduce errores manuales al conectar nodos complejos.

**Demo**
https://youtu.be/oSyYuMWCV2M?si=1ZVym-O0YxOOunVR
### 2. Custom Outliner 👁️
* **Filtros avanzados:** Visualiza solo los nodos que te interesan para el rig (joints, controles, locators).
* **Organización limpia:** Limpia el ruido visual del Outliner nativo de Maya para trabajar más rápido.

**Demo**
https://youtu.be/6x2vQmQfe5Q?si=ZMnr2HReByCICJ45
## 🚀 Instalación y Uso

1. Descarga o clona este repositorio dentro de tu carpeta de scripts de Maya:
   ```bash
   git clone (https://github.com/pepeRigging/Peperig_Tools.git)
   ```

2. Abre el **Script Editor** de Maya en una pestaña de **Python** y ejecuta la herramienta que necesites:

```python
# Para abrir el Constraint Manager:
import ConstraintMng
import importlib
importlib.reload(ConstraintMng)

ConstraintMng.run()

# Para abrir el Custom Outliner:
import CustomOutliner  # Ajusta el nombre de tu archivo del Outliner aquí si es diferente
import importlib
importlib.reload(CustomOutliner)

CustomOutliner.run()
```

## 📝 Requisitos
* Autodesk Maya 2025 o superior (Python 3).

---
*Desarrollado con 🛠️ por **pepeRigging**. Si tienes sugerencias o encuentras algún bug, ¡abre un Issue!*
