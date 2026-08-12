# Peperig Tools 🛠️

Un conjunto de herramientas de Python para Autodesk Maya diseñado para optimizar y acelerar los flujos de trabajo de Rigging y desarrollo técnico.

## ✨ Herramientas incluidas

### 1. Constraint Manager 🔗
* **Gestión centralizada:** Controla y organiza múltiples tipos de constraints desde una interfaz limpia.
* **Automatización de jerarquías:** Reduce errores manuales al conectar nodos complejos.

### 2. Custom Outliner 👁️
* **Filtros avanzados:** Visualiza solo los nodos que te interesan para el rig (joints, controles, locators).
* **Organización limpia:** Limpia el ruido visual del Outliner nativo de Maya para trabajar más rápido.

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
