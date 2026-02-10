import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import insert_producto

if __name__ == "__main__":
    try:
        nuevo_id = insert_producto(
            nombre='COSRX Advanced Snail 92 All In One Cream',
            categoria='Moisturizer',
            precio=28.50,
            stock=75,
            descripcion='Crema todo en uno con 92% de mucina de caracol'
        )

        print('ID producto insertado →', nuevo_id)
    except Exception as e:
        print('Error al insertar producto →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python3 tests/test_insert_producto.py
