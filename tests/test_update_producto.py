import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import update_producto

if __name__ == "__main__":
    try:
        # Validar que se haya pasado el ID como parámetro
        if len(sys.argv) < 2:
            print('Error: Debes proporcionar el ID del producto')
            print('Uso: python tests/test_update_producto.py <ID>')
            sys.exit(1)
        
        # Obtener el ID del producto desde los argumentos
        producto_id = int(sys.argv[1])
        resultado = update_producto(
            producto_id=producto_id,
            nombre='Producto modificado por el test',
            categoria='Serum',
            precio=35.99,
            stock=120,
            descripcion='Descripción actualizada desde test'
        )

        if resultado:
            print(f'Producto {producto_id} actualizado correctamente')
        else:
            print(f'Producto {producto_id} no encontrado')
    except ValueError:
        print('Error: El ID debe ser un número entero')
        sys.exit(1)
    except Exception as e:
        print('Error al actualizar producto →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python3 tests/test_update_producto.py 1
