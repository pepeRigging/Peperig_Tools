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


### 3. Switcher Tool 👁

* **Custom Menus:** Create personalized drop-down menus in the Channel Box to show linked elements.
* **Viewport Access:** Generate a convenient context menu directly in the viewport for quick selection.


**Demo**
https://youtu.be/NLXNSn9J4-M

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

# Open the SpaceSwitchTool:
import SpaceSwitchTool
import importlib
importlib.reload(SpaceSwitchTool)

SpaceSwitchTool.run()
```

## 📝 Requirements

* Autodesk Maya 2025 or later
* Python 3

---

*Developed with 🛠️ by* **pepeRigging**.

If you have any suggestions or find a bug, feel free to open an **Issue**!