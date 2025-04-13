from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Enum
from sqlalchemy.dialects.mysql import VARCHAR
from conexion import Base
import enum

# Enums personalizados
class EstadoAlmacenEnum(enum.Enum):
    Activo = "Activo"
    Inactivo = "Inactivo"

class ActivoEnum(enum.Enum):
    Si = "Sí"
    No = "No"

# Modelo: almacen
class Almacen(Base):
    __tablename__ = 'almacen'

    idalmacen = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), nullable=False, unique=True)
    ubicacion = Column(String(45), nullable=False)
    capacidad_maxima = Column(Integer, nullable=False)
    estado = Column(Enum(EstadoAlmacenEnum), nullable=False)


# Modelo: caja
class Caja(Base):
    __tablename__ = 'caja'

    idcaja = Column(Integer, primary_key=True, autoincrement=True)
    saldo_inicial = Column(DECIMAL(10, 2), nullable=False)
    fecha_apertura = Column(DateTime, nullable=False)
    saldo_final = Column(DECIMAL(10, 2), nullable=False)
    fecha_cierre = Column(DateTime, nullable=False)


# Modelo: cliente
class Cliente(Base):
    __tablename__ = 'cliente'

    ID_Cliente = Column(String(50), primary_key=True)
    Nombre = Column(String(100))
    Apellido = Column(String(100))
    Telefono = Column(String(20))
    Correo = Column(String(100))
    Direccion = Column(String(200))


# Modelo: metodo_pago
class MetodoPago(Base):
    __tablename__ = 'metodo_pago'

    idmetodo_pago = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(String(100))
    activo = Column(Enum(ActivoEnum), nullable=False, default=ActivoEnum.Si)


# Modelo: sucursal
class Sucursal(Base):
    __tablename__ = 'sucursal'

    id_sucursal = Column(Integer, primary_key=True)
    nombre = Column(String(45), nullable=False)
    direccion = Column(String(45), nullable=False)
    ciudad = Column(String(45), nullable=False)
    estado = Column(String(45), nullable=False)
    codigo_postal = Column(String(45), nullable=False)
    telefono = Column(String(45), nullable=False, unique=True)

class Proveedor(Base):
    __tablename__ = 'proveedor'

    id_proveedor = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(45), nullable=False)
    telefono = Column(String(45), nullable=False, unique=True)
    correo = Column(String(45), nullable=False, unique=True)
    direccion = Column(String(45), nullable=False)