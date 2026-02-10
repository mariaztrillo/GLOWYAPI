# Glowy API REST - Skincare Coreano

## Descripción General

API REST pura para gestión de productos de skincare coreano. Implementa operaciones CRUD completas utilizando **SQL directo** (sin ORM) con FastAPI.

**Características:**
- ✅ API REST completamente funcional
- ✅ Documentación Swagger automática
- ✅ SQL directo con `mysql-connector-python`
- ✅ Validaciones con Pydantic
- ✅ Tests unitarios con pytest
- ✅ Respuestas en JSON

---

## 🏗️ Estructura del Proyecto

```
glowy-apirest/
├── app/
│   ├── __init__.py
│   ├── main.py              # Endpoints API REST
│   └── database.py          # Funciones CRUD con SQL directo
├── tests/
│   ├── __init__.py
│   ├── test_get_connection.py
│   ├── test_fetch_all_productos.py
│   ├── test_fetch_producto_by_id.py
│   ├── test_insert_producto.py
│   ├── test_update_producto.py
│   └── test_delete_producto.py
├── docs/
│   └── init_db.sql          # Script de base de datos
├── requirements.txt
├── env.back                 # Ejemplo de variables de entorno
├── .gitignore
└── README.md
```

---

## Requisitos Previos

- **Python 3.10+**
- **MySQL/MariaDB** (XAMPP, MAMP o standalone)

---

## Instalación

### 1️⃣ Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
```

### 2️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar variables de entorno
```bash
cp env.back .env
nano .env  # Editar con tus credenciales
```

Contenido de `.env`:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=glowy_db
DB_PORT=3306
```

### 4️⃣ Crear base de datos
```bash
mysql -u root -p < docs/init_db.sql
```

O desde phpMyAdmin: Importar → `docs/init_db.sql`

### 5️⃣ Ejecutar la API
```bash
uvicorn app.main:app --reload
```

La API estará disponible en: **http://localhost:8000**

---

## Documentación de la API

### **Swagger UI (Interactiva):**
```
http://localhost:8000/docs
```

### **ReDoc:**
```
http://localhost:8000/redoc
```

### **OpenAPI JSON:**
```
http://localhost:8000/openapi.json
```

---

## 🔗 Endpoints

| Método | Endpoint               | Descripción                    |
|--------|------------------------|--------------------------------|
| GET    | `/ping`                | Health check                   |
| GET    | `/productos`           | Listar todos los productos     |
| GET    | `/productos/{id}`      | Obtener un producto por ID     |
| POST   | `/productos`           | Crear nuevo producto           |
| PUT    | `/productos/{id}`      | Actualizar producto completo   |
| DELETE | `/productos/{id}`      | Eliminar producto              |

---

## 📝 Ejemplos de Uso

### **1. Health Check**
```bash
curl http://localhost:8002/ping
```

**Respuesta:**
```json
{
  "message": "pong",
  "service": "Glowy API"
}
```

---

### **2. Listar Productos**
```bash
curl http://localhost:8002/productos
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "COSRX Snail Mucin 96 Power Essence",
    "categoria": "Serum",
    "precio": 24.99,
    "stock": 50,
    "descripcion": "Esencia con 96% de mucina de caracol"
  }
]
```

---

### **3. Obtener Producto por ID**
```bash
curl http://localhost:8002/productos/1
```

**Respuesta exitosa:** `200 OK`
```json
{
  "id": 1,
  "nombre": "COSRX Snail Mucin 96 Power Essence",
  "categoria": "Serum",
  "precio": 24.99,
  "stock": 50,
  "descripcion": "Esencia con 96% de mucina de caracol"
}
```

**Respuesta error:** `404 Not Found`
```json
{
  "detail": "Producto no encontrado"
}
```

---

### **4. Crear Producto**
```bash
curl -X POST http://localhost:8002/productos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Beauty of Joseon Relief Sun",
    "categoria": "Sunscreen",
    "precio": 16.99,
    "stock": 80,
    "descripcion": "Protector solar orgánico con arroz"
  }'
```

**Respuesta:** `201 Created`
```json
{
  "id": 9,
  "nombre": "Beauty of Joseon Relief Sun",
  "categoria": "Sunscreen",
  "precio": 16.99,
  "stock": 80,
  "descripcion": "Protector solar orgánico con arroz"
}
```

---

### **5. Actualizar Producto**
```bash
curl -X PUT http://localhost:8002/productos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "COSRX Snail Mucin (Updated)",
    "categoria": "Serum",
    "precio": 22.99,
    "stock": 100,
    "descripcion": "Nueva descripción"
  }'
```

**Respuesta:** `200 OK`

---

### **6. Eliminar Producto**
```bash
curl -X DELETE http://localhost:8002/productos/1
```

**Respuesta exitosa:** `204 No Content`

---

## ✅ Validaciones

### **Campo: nombre**
- Requerido
- 3-150 caracteres
- No vacío

### **Campo: categoria**
- Requerido
- Valores válidos: Serum, Cleanser, Moisturizer, Toner, Sunscreen, Mask, Exfoliator, Eye Cream, Ampoule, Essence
- Capitalización automática

### **Campo: precio**
- Requerido
- Mayor a 0
- Máximo 999.99€
- 2 decimales

### **Campo: stock**
- Requerido
- No negativo (≥ 0)
- Máximo 9999 unidades

### **Campo: descripcion**
- Opcional
- Máximo 500 caracteres

---

## 🧪 Testing

Los tests se ejecutan como scripts independientes desde la terminal.

### **Ejecutar todos los tests:**

#### Test de Conexión:
```bash
python3 tests/test_get_connection.py
```

#### Listar Productos:
```bash
python3 tests/test_fetch_all_productos.py
```

#### Obtener Producto por ID:
```bash
python3 tests/test_fetch_producto_by_id.py 1
```

#### Insertar Producto:
```bash
python3 tests/test_insert_producto.py
```

#### Actualizar Producto:
```bash
python3 tests/test_update_producto.py 1
```

#### Eliminar Producto:
```bash
python3 tests/test_delete_producto.py 9
```

### **Tests incluidos:**
- ✅ `test_get_connection.py` - Verifica conexión a BD
- ✅ `test_fetch_all_productos.py` - Lista todos los productos
- ✅ `test_fetch_producto_by_id.py <ID>` - Obtiene producto por ID
- ✅ `test_insert_producto.py` - Inserta producto de prueba
- ✅ `test_update_producto.py <ID>` - Actualiza producto
- ✅ `test_delete_producto.py <ID>` - Elimina producto

---

## 📊 Base de Datos

### **Tabla: productos**

| Campo       | Tipo          | Restricciones          |
|-------------|---------------|------------------------|
| id          | INT           | PRIMARY KEY, AUTO_INCREMENT |
| nombre      | VARCHAR(150)  | NOT NULL               |
| categoria   | VARCHAR(50)   | NOT NULL               |
| precio      | DECIMAL(10,2) | NOT NULL               |
| stock       | INT           | NOT NULL, DEFAULT 0    |
| descripcion | TEXT          | NULL                   |

---

## 🎯 Diferencias con el Monolito

| Aspecto | Monolito | API REST |
|---------|----------|----------|
| **Respuestas** | HTML (Jinja2) | JSON |
| **Frontend** | Incluido (templates) | No incluido |
| **Formularios** | HTML Form + POST | JSON Body |
| **Rutas** | GET/POST (páginas) | GET/POST/PUT/DELETE |
| **Uso** | Navegador directo | Cliente HTTP (Postman, fetch, etc.) |
| **Tests** | No incluidos | 6 archivos de tests |

---

## Solución de Problemas

### **Error: Can't connect to MySQL**
- Verifica que MySQL esté corriendo
- Revisa credenciales en `.env`

### **Error: Table 'productos' doesn't exist**
- Ejecuta `docs/init_db.sql`

### **Tests fallan:**
- Asegúrate de que la BD tenga datos iniciales
- Verifica conexión a `glowy_db`

---

## Uso con Cliente HTTP

### **Postman:**
1. Importa la colección desde Swagger
2. URL base: `http://localhost:8002`

### **JavaScript (fetch):**
```javascript
// Obtener productos
const response = await fetch('http://localhost:8002/productos');
const productos = await response.json();

// Crear producto
await fetch('http://localhost:8002/productos', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    nombre: "New Product",
    categoria: "Serum",
    precio: 25.99,
    stock: 30,
    descripcion: "Description"
  })
});
```

### **Python (requests):**
```python
import requests

# Listar productos
response = requests.get('http://localhost:8000/productos')
productos = response.json()

# Crear producto
data = {
    "nombre": "New Product",
    "categoria": "Serum",
    "precio": 25.99,
    "stock": 30,
    "descripcion": "Description"
}
response = requests.post('http://localhost:8000/productos', json=data)
```

---

## Autor

**Nombre:**  Maria de los Angeles Zamora   
**Email:** mariadezt@gmail.com  
**Asignatura:** Python 
**Proyecto:** API REST con SQL Directo

---

## Licencia

Proyecto educativo para uso académico.

---

**¡Happy Coding! 🧴✨**
# GLOWYAPI
