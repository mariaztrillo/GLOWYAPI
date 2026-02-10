import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import fetch_producto_by_id

if __name__ == "__main__":
    try:
        # Validar que se haya pasado el ID como parámetro
        if len(sys.argv) < 2:
            print('Error: Debes proporcionar el ID del producto')
            print('Uso: python tests/test_fetch_producto_by_id.py <ID>')
            sys.exit(1)
        
        # Obtener el ID del producto desde los argumentos
        producto_id = int(sys.argv[1])
        producto = fetch_producto_by_id(producto_id)

        if producto:
            print('Producto encontrado:')
            print(producto)
        else:
            print('Producto no encontrado')
    except ValueError:
        print('Error: El ID debe ser un número entero')
        sys.exit(1)
    except Exception as e:
        print('Error al buscar producto →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python3 tests/test_fetch_producto_by_id.py 1
