import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import get_connection

if __name__ == "__main__":
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        print('Conexión OK →', cur.fetchone())
        cur.close()
        conn.close()
    except Exception as e:
        print('Error de conexión →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python3 tests/test_get_connection.py
