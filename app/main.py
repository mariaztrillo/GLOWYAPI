from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, field_validator
from typing import Optional, List

# Importamos las funciones que consultan/insertan/eliminan en MySQL
from app.database import (
    fetch_all_productos, 
    insert_producto, 
    delete_producto,
    fetch_producto_by_id,
    update_producto
)


# --------------------------------------------------
# MODELOS Pydantic
# --------------------------------------------------

# Modelo base con validaciones comunes
class ProductoBase(BaseModel):
    nombre: str
    categoria: str
    precio: float
    stock: int
    descripcion: Optional[str] = None

    @field_validator('nombre')
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        """Valida que el nombre del producto tenga formato correcto."""
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        
        v = v.strip()
        
        if len(v) < 3:
            raise ValueError('El nombre debe tener al menos 3 caracteres')
        
        if len(v) > 150:
            raise ValueError('El nombre no puede exceder 150 caracteres')
        
        return v
    
    @field_validator('categoria')
    @classmethod
    def validar_categoria(cls, v: str) -> str:
        """Valida que la categoría sea una de las permitidas."""
        if not v or not v.strip():
            raise ValueError('La categoría no puede estar vacía')
        
        v = v.strip()
        
        categorias_validas = [
            'Serum', 'Cleanser', 'Moisturizer', 
            'Toner', 'Sunscreen', 'Mask', 'Exfoliator',
            'Eye Cream', 'Ampoule', 'Essence'
        ]
        
        # Normalizar para comparar (ignorar mayúsculas)
        if v.title() not in categorias_validas:
            raise ValueError(
                f'Categoría no válida. Debe ser una de: {", ".join(categorias_validas)}'
            )
        
        return v.title()  # Capitaliza la primera letra
    
    @field_validator('precio')
    @classmethod
    def validar_precio(cls, v: float) -> float:
        """Valida que el precio tenga formato correcto."""
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        
        if v > 999.99:
            raise ValueError('El precio no puede exceder 999.99€')
        
        # Redondear a 2 decimales
        return round(v, 2)
    
    @field_validator('stock')
    @classmethod
    def validar_stock(cls, v: int) -> int:
        """Valida que el stock sea válido."""
        if v < 0:
            raise ValueError('El stock no puede ser negativo')
        
        if v > 9999:
            raise ValueError('El stock no puede exceder 9999 unidades')
        
        return v
    
    @field_validator('descripcion')
    @classmethod
    def validar_descripcion(cls, v: Optional[str]) -> Optional[str]:
        """Valida la descripción del producto."""
        if v is None or v.strip() == '':
            return None
        
        v = v.strip()
        
        if len(v) > 500:
            raise ValueError('La descripción no puede exceder 500 caracteres')
        
        return v


# Modelo para crear producto (sin ID)
class ProductoCreate(ProductoBase):
    pass


# Modelo para actualizar producto (sin ID)
class ProductoUpdate(ProductoBase):
    pass


# Modelo completo de Producto (con ID y validaciones)
class Producto(ProductoBase):
    id: int


# --------------------------------------------------
# APP
# --------------------------------------------------

app = FastAPI(
    title="Glowy API - Skincare Coreano",
    description="API REST para gestión de productos de skincare coreano con SQL directo (sin ORM)",
    version="1.0.0",
    contact={
        "name": "Tu nombre",
        "email": "tu-email@example.com"
    }
)



# ENDPOINTS

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a Glowy API - Skincare Coreano",
        "description": "API para gestion de productos de belleza coreanos",
    }

# --- Endpoint de health check ---
@app.get("/ping")
def ping():
    """
    Endpoint de health check para verificar que la API está funcionando.
    """
    return {"message": "pong", "service": "Glowy API"}


# --- Endpoint para favicon (evita 404 en navegadores) ---
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Endpoint para manejar peticiones de favicon del navegador.
    Retorna 204 (sin contenido) para evitar logs de error.
    """
    return Response(status_code=204)


# --- Endpoint para listar todos los productos ---
@app.get("/productos", response_model=List[Producto], tags=["Productos"])
def listar_productos():
    """
    Obtiene la lista completa de productos de skincare desde la base de datos.
    
    Returns:
        List[Producto]: Lista de todos los productos
    """
    rows = fetch_all_productos()
    return [Producto(**row) for row in rows]


# --- Endpoint para obtener un producto por ID ---
@app.get("/productos/{producto_id}", response_model=Producto, tags=["Productos"])
def obtener_producto(producto_id: int):
    """
    Obtiene un producto específico por su ID.
    
    Args:
        producto_id (int): ID del producto a buscar
        
    Returns:
        Producto: Datos del producto
        
    Raises:
        HTTPException: 404 si el producto no existe
    """
    producto = fetch_producto_by_id(producto_id)
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return Producto(**producto)


# --- Endpoint para crear un nuevo producto ---
@app.post("/productos", response_model=Producto, status_code=201, tags=["Productos"])
def crear_producto(producto: ProductoCreate):
    """
    Crea un nuevo producto en la base de datos.
    Los datos son validados automáticamente por Pydantic.
    
    Args:
        producto (ProductoCreate): Datos del producto a crear
        
    Returns:
        Producto: Producto creado con su ID asignado
    """
    producto_id = insert_producto(
        producto.nombre,
        producto.categoria,
        producto.precio,
        producto.stock,
        producto.descripcion
    )
    
    return Producto(
        id=producto_id,
        nombre=producto.nombre,
        categoria=producto.categoria,
        precio=producto.precio,
        stock=producto.stock,
        descripcion=producto.descripcion
    )


# --- Endpoint para actualizar un producto ---
@app.put("/productos/{producto_id}", response_model=Producto, tags=["Productos"])
def actualizar_producto(producto_id: int, producto: ProductoUpdate):
    """
    Actualiza los datos de un producto existente.
    Los datos son validados automáticamente por Pydantic.
    
    Args:
        producto_id (int): ID del producto a actualizar
        producto (ProductoUpdate): Nuevos datos del producto
        
    Returns:
        Producto: Producto actualizado
        
    Raises:
        HTTPException: 404 si el producto no existe
    """
    actualizado = update_producto(
        producto_id,
        producto.nombre,
        producto.categoria,
        producto.precio,
        producto.stock,
        producto.descripcion
    )
    
    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return Producto(
        id=producto_id,
        nombre=producto.nombre,
        categoria=producto.categoria,
        precio=producto.precio,
        stock=producto.stock,
        descripcion=producto.descripcion
    )


# --- Endpoint para eliminar un producto ---
@app.delete("/productos/{producto_id}", status_code=204, tags=["Productos"])
def eliminar_producto(producto_id: int):
    """
    Elimina un producto de la base de datos por su ID.
    
    Args:
        producto_id (int): ID del producto a eliminar
        
    Raises:
        HTTPException: 404 si el producto no existe
    """
    eliminado = delete_producto(producto_id)
    
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return None
