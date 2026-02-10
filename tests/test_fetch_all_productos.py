import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import fetch_all_productos

if __name__ == "__main__":
    try:
        productos = fetch_all_productos()
        print(f'Productos encontrados: {len(productos)}')
        for p in productos:
            print(p)
    except Exception as e:
        print('Error al obtener productos →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python3 tests/test_fetch_all_productos.py
