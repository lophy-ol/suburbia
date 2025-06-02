-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema suburbia
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema suburbia
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `suburbia` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `suburbia` ;

-- TABLA categoria
CREATE TABLE IF NOT EXISTS `suburbia`.`categoria` (
  `id_categorias` INT NOT NULL AUTO_INCREMENT,
  `tipo_categoria` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_categorias`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO `suburbia`.`categoria` (tipo_categoria) VALUES
('Electrónica'), ('Ropa'), ('Alimentos'), ('Hogar'), ('Deportes'),
('Juguetes'), ('Belleza'), ('Automotriz'), ('Libros'), ('Muebles'),
('Computación'), ('Salud'), ('Herramientas'), ('Oficina'), ('Bebidas'),
('Mascotas'), ('Viajes'), ('Jardinería'), ('Joyería'), ('Zapatos');


-- TABLA proveedor
CREATE TABLE IF NOT EXISTS `suburbia`.`proveedor` (
  `RFC` VARCHAR(50) NOT NULL,
  `nombre` VARCHAR(45) NULL DEFAULT NULL,
  `telefono` CHAR(10) NULL DEFAULT NULL,
  `correo` VARCHAR(45) NULL DEFAULT NULL,
  `direccion` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`RFC`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO `suburbia`.`proveedor` (RFC, nombre, telefono, correo, direccion) VALUES
('RFC001', 'Proveedor A', '5512345678', 'a@proveedor.com', 'Calle 1'),
('RFC002', 'Proveedor B', '5512345679', 'b@proveedor.com', 'Calle 2'),
('RFC003', 'Proveedor C', '5512345680', 'c@proveedor.com', 'Calle 3'),
('RFC004', 'Proveedor D', '5512345681', 'd@proveedor.com', 'Calle 4'),
('RFC005', 'Proveedor E', '5512345682', 'e@proveedor.com', 'Calle 5'),
('RFC006', 'Proveedor F', '5512345683', 'f@proveedor.com', 'Calle 6'),
('RFC007', 'Proveedor G', '5512345684', 'g@proveedor.com', 'Calle 7'),
('RFC008', 'Proveedor H', '5512345685', 'h@proveedor.com', 'Calle 8'),
('RFC009', 'Proveedor I', '5512345686', 'i@proveedor.com', 'Calle 9'),
('RFC010', 'Proveedor J', '5512345687', 'j@proveedor.com', 'Calle 10'),
('RFC011', 'Proveedor K', '5512345688', 'k@proveedor.com', 'Calle 11'),
('RFC012', 'Proveedor L', '5512345689', 'l@proveedor.com', 'Calle 12'),
('RFC013', 'Proveedor M', '5512345690', 'm@proveedor.com', 'Calle 13'),
('RFC014', 'Proveedor N', '5512345691', 'n@proveedor.com', 'Calle 14'),
('RFC015', 'Proveedor O', '5512345692', 'o@proveedor.com', 'Calle 15'),
('RFC016', 'Proveedor P', '5512345693', 'p@proveedor.com', 'Calle 16'),
('RFC017', 'Proveedor Q', '5512345694', 'q@proveedor.com', 'Calle 17'),
('RFC018', 'Proveedor R', '5512345695', 'r@proveedor.com', 'Calle 18'),
('RFC019', 'Proveedor S', '5512345696', 's@proveedor.com', 'Calle 19'),
('RFC020', 'Proveedor T', '5512345697', 't@proveedor.com', 'Calle 20');


-- TABLA marcas
CREATE TABLE IF NOT EXISTS `suburbia`.`marcas` (
  `id_marca` INT NOT NULL AUTO_INCREMENT,
  `nombre_marca` VARCHAR(45) NULL DEFAULT NULL,
  `RFC` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_marca`),
  INDEX `fk_marcas_proveedor1_idx` (`RFC` ASC) VISIBLE,
  CONSTRAINT `fk_marcas_proveedor1`
    FOREIGN KEY (`RFC`)
    REFERENCES `suburbia`.`proveedor` (`RFC`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO `suburbia`.`marcas` (nombre_marca, RFC) VALUES
('Marca A', 'RFC001'), ('Marca B', 'RFC002'), ('Marca C', 'RFC003'), ('Marca D', 'RFC004'), ('Marca E', 'RFC005'),
('Marca F', 'RFC006'), ('Marca G', 'RFC007'), ('Marca H', 'RFC008'), ('Marca I', 'RFC009'), ('Marca J', 'RFC010'),
('Marca K', 'RFC011'), ('Marca L', 'RFC012'), ('Marca M', 'RFC013'), ('Marca N', 'RFC014'), ('Marca O', 'RFC015'),
('Marca P', 'RFC016'), ('Marca Q', 'RFC017'), ('Marca R', 'RFC018'), ('Marca S', 'RFC019'), ('Marca T', 'RFC020');


-- TABLA articulo
CREATE TABLE IF NOT EXISTS `suburbia`.`articulo` (
  `codigo_articulo` VARCHAR(20) NOT NULL,
  `nombre_articulo` VARCHAR(45) NULL DEFAULT NULL,
  `activacion_articulo` TINYINT(1) NULL DEFAULT NULL,
  `precio` DECIMAL(10,2) NULL DEFAULT NULL,
  `stock` INT NULL DEFAULT NULL,
  `id_marca` INT NOT NULL,
  `id_categorias` INT NOT NULL,
  `gasto` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`codigo_articulo`),
  INDEX `fk_articulos_marcas1_idx` (`id_marca` ASC) VISIBLE,
  INDEX `fk_articulo_categoria1_idx` (`id_categorias` ASC) VISIBLE,
  CONSTRAINT `fk_articulo_categoria1`
    FOREIGN KEY (`id_categorias`)
    REFERENCES `suburbia`.`categoria` (`id_categorias`),
  CONSTRAINT `fk_articulos_marcas1`
    FOREIGN KEY (`id_marca`)
    REFERENCES `suburbia`.`marcas` (`id_marca`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO `suburbia`.`articulo` (codigo_articulo, nombre_articulo, activacion_articulo, precio, stock, id_marca, id_categorias, gasto) VALUES
('ART001', 'Articulo 1', 1, 100.00, 50, 1, 1, 80.00),
('ART002', 'Articulo 2', 1, 150.00, 60, 2, 2, 120.00),
('ART003', 'Articulo 3', 1, 200.00, 70, 3, 3, 160.00),
('ART004', 'Articulo 4', 1, 250.00, 80, 4, 4, 210.00),
('ART005', 'Articulo 5', 1, 300.00, 90, 5, 5, 240.00),
('ART006', 'Articulo 6', 1, 350.00, 100, 6, 6, 280.00),
('ART007', 'Articulo 7', 1, 400.00, 110, 7, 7, 320.00),
('ART008', 'Articulo 8', 1, 450.00, 120, 8, 8, 360.00),
('ART009', 'Articulo 9', 1, 500.00, 130, 9, 9, 400.00),
('ART010', 'Articulo 10', 1, 550.00, 140, 10, 10, 440.00),
('ART011', 'Articulo 11', 1, 600.00, 150, 11, 11, 480.00),
('ART012', 'Articulo 12', 1, 650.00, 160, 12, 12, 520.00),
('ART013', 'Articulo 13', 1, 700.00, 170, 13, 13, 560.00),
('ART014', 'Articulo 14', 1, 750.00, 180, 14, 14, 600.00),
('ART015', 'Articulo 15', 1, 800.00, 190, 15, 15, 640.00),
('ART016', 'Articulo 16', 1, 850.00, 200, 16, 16, 680.00),
('ART017', 'Articulo 17', 1, 900.00, 210, 17, 17, 720.00),
('ART018', 'Articulo 18', 1, 950.00, 220, 18, 18, 760.00),
('ART019', 'Articulo 19', 1, 1000.00, 230, 19, 19, 800.00),
('ART020', 'Articulo 20', 1, 1050.00, 240, 20, 20, 840.00);


-- TABLA cliente
CREATE TABLE IF NOT EXISTS `suburbia`.`cliente` (
  `id_cliente` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(100) NULL DEFAULT NULL,
  `Apellido` VARCHAR(100) NULL DEFAULT NULL,
  `Telefono` CHAR(10) NULL DEFAULT NULL,
  `Correo` VARCHAR(100) NULL DEFAULT NULL,
  `Direccion` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`id_cliente`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO `suburbia`.`cliente` (Nombre, Apellido, Telefono, Correo, Direccion) VALUES
('Juan', 'Perez', '5511111111', 'juan@mail.com', 'Calle 1'),
('Maria', 'Lopez', '5522222222', 'maria@mail.com', 'Calle 2'),
('Pedro', 'Gomez', '5533333333', 'pedro@mail.com', 'Calle 3'),
('Ana', 'Martinez', '5544444444', 'ana@mail.com', 'Calle 4'),
('Luis', 'Ramirez', '5555555555', 'luis@mail.com', 'Calle 5'),
('Sofia', 'Hernandez', '5566666666', 'sofia@mail.com', 'Calle 6'),
('Carlos', 'Diaz', '5577777777', 'carlos@mail.com', 'Calle 7'),
('Laura', 'Torres', '5588888888', 'laura@mail.com', 'Calle 8'),
('Jose', 'Vargas', '5599999999', 'jose@mail.com', 'Calle 9'),
('Martha', 'Flores', '5512345670', 'martha@mail.com', 'Calle 10'),
('Ricardo', 'Santos', '5512345671', 'ricardo@mail.com', 'Calle 11'),
('Elena', 'Castro', '5512345672', 'elena@mail.com', 'Calle 12'),
('Miguel', 'Ortiz', '5512345673', 'miguel@mail.com', 'Calle 13'),
('Gabriela', 'Rios', '5512345674', 'gabriela@mail.com', 'Calle 14'),
('Jorge', 'Ruiz', '5512345675', 'jorge@mail.com', 'Calle 15'),
('Patricia', 'Cruz', '5512345676', 'patricia@mail.com', 'Calle 16'),
('Andres', 'Morales', '5512345677', 'andres@mail.com', 'Calle 17'),
('Monica', 'Reyes', '5512345678', 'monica@mail.com', 'Calle 18'),
('Daniel', 'Gutierrez', '5512345679', 'daniel@mail.com', 'Calle 19'),
('Adriana', 'Sanchez', '5512345680', 'adriana@mail.com', 'Calle 20');


-- TABLA metodo_pago
CREATE TABLE IF NOT EXISTS `suburbia`.`metodo_pago` (
  `id_modo_pago` INT NOT NULL AUTO_INCREMENT,
  `tipo` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`id_modo_pago`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO `suburbia`.`metodo_pago` (tipo) VALUES
('Efectivo'), ('Tarjeta de crédito'), ('Tarjeta de débito'), ('Transferencia bancaria'), ('Cheque'),
('Paypal'), ('MercadoPago'), ('Oxxo'), ('Depósito bancario'), ('Crédito');


-- TABLA sucursal
CREATE TABLE IF NOT EXISTS `suburbia`.`sucursal` (
  `id_sucursal` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `direccion` VARCHAR(45) NOT NULL,
  `ciudad` VARCHAR(45) NOT NULL,
  `estado` VARCHAR(45) NOT NULL,
  `codigo_postal` VARCHAR(45) NOT NULL,
  `telefono` CHAR(10) NOT NULL,
  PRIMARY KEY (`id_sucursal`),
  UNIQUE INDEX `telefono_UNIQUE` (`telefono` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO `suburbia`.`sucursal` (nombre, direccion, ciudad, estado, codigo_postal, telefono) VALUES
('Sucursal A', 'Calle 1', 'Ciudad 1', 'Estado 1', '01000', '5510000001'),
('Sucursal B', 'Calle 2', 'Ciudad 2', 'Estado 2', '02000', '5510000002'),
('Sucursal C', 'Calle 3', 'Ciudad 3', 'Estado 3', '03000', '5510000003'),
('Sucursal D', 'Calle 4', 'Ciudad 4', 'Estado 4', '04000', '5510000004'),
('Sucursal E', 'Calle 5', 'Ciudad 5', 'Estado 5', '05000', '5510000005'),
('Sucursal F', 'Calle 6', 'Ciudad 6', 'Estado 6', '06000', '5510000006'),
('Sucursal G', 'Calle 7', 'Ciudad 7', 'Estado 7', '07000', '5510000007'),
('Sucursal H', 'Calle 8', 'Ciudad 8', 'Estado 8', '08000', '5510000008'),
('Sucursal I', 'Calle 9', 'Ciudad 9', 'Estado 9', '09000', '5510000009'),
('Sucursal J', 'Calle 10', 'Ciudad 10', 'Estado 10', '10000', '5510000010'),
('Sucursal K', 'Calle 11', 'Ciudad 11', 'Estado 11', '11000', '5510000011'),
('Sucursal L', 'Calle 12', 'Ciudad 12', 'Estado 12', '12000', '5510000012'),
('Sucursal M', 'Calle 13', 'Ciudad 13', 'Estado 13', '13000', '5510000013'),
('Sucursal N', 'Calle 14', 'Ciudad 14', 'Estado 14', '14000', '5510000014'),
('Sucursal O', 'Calle 15', 'Ciudad 15', 'Estado 15', '15000', '5510000015'),
('Sucursal P', 'Calle 16', 'Ciudad 16', 'Estado 16', '16000', '5510000016'),
('Sucursal Q', 'Calle 17', 'Ciudad 17', 'Estado 17', '17000', '5510000017'),
('Sucursal R', 'Calle 18', 'Ciudad 18', 'Estado 18', '18000', '5510000018'),
('Sucursal S', 'Calle 19', 'Ciudad 19', 'Estado 19', '19000', '5510000019'),
('Sucursal T', 'Calle 20', 'Ciudad 20', 'Estado 20', '20000', '5510000020');


-- TABLA empleado
CREATE TABLE IF NOT EXISTS `suburbia`.`empleado` (
  `id_empleado` INT NOT NULL AUTO_INCREMENT,
  `nombre_empleado` VARCHAR(45) NULL DEFAULT NULL,
  `apellido_empleado` VARCHAR(45) NULL DEFAULT NULL,
  `telefono` CHAR(10) NULL DEFAULT NULL,
  `correo` VARCHAR(45) NULL DEFAULT NULL,
  `direccion` VARCHAR(100) NULL DEFAULT NULL,
  `id_sucursal` INT NOT NULL,
  PRIMARY KEY (`id_empleado`),
  INDEX `fk_empleado_sucursal1_idx` (`id_sucursal` ASC) VISIBLE,
  CONSTRAINT `fk_empleado_sucursal1`
    FOREIGN KEY (`id_sucursal`)
    REFERENCES `suburbia`.`sucursal` (`id_sucursal`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO `suburbia`.`empleado` (nombre_empleado, apellido_empleado, telefono, correo, direccion, id_sucursal) VALUES
('Empleado1', 'Apellido1', '5511000001', 'empleado1@mail.com', 'Direccion 1', 1),
('Empleado2', 'Apellido2', '5511000002', 'empleado2@mail.com', 'Direccion 2', 2),
('Empleado3', 'Apellido3', '5511000003', 'empleado3@mail.com', 'Direccion 3', 3),
('Empleado4', 'Apellido4', '5511000004', 'empleado4@mail.com', 'Direccion 4', 4),
('Empleado5', 'Apellido5', '5511000005', 'empleado5@mail.com', 'Direccion 5', 5),
('Empleado6', 'Apellido6', '5511000006', 'empleado6@mail.com', 'Direccion 6', 6),
('Empleado7', 'Apellido7', '5511000007', 'empleado7@mail.com', 'Direccion 7', 7),
('Empleado8', 'Apellido8', '5511000008', 'empleado8@mail.com', 'Direccion 8', 8),
('Empleado9', 'Apellido9', '5511000009', 'empleado9@mail.com', 'Direccion 9', 9),
('Empleado10', 'Apellido10', '5511000010', 'empleado10@mail.com', 'Direccion 10', 10),
('Empleado11', 'Apellido11', '5511000011', 'empleado11@mail.com', 'Direccion 11', 11),
('Empleado12', 'Apellido12', '5511000012', 'empleado12@mail.com', 'Direccion 12', 12),
('Empleado13', 'Apellido13', '5511000013', 'empleado13@mail.com', 'Direccion 13', 13),
('Empleado14', 'Apellido14', '5511000014', 'empleado14@mail.com', 'Direccion 14', 14),
('Empleado15', 'Apellido15', '5511000015', 'empleado15@mail.com', 'Direccion 15', 15),
('Empleado16', 'Apellido16', '5511000016', 'empleado16@mail.com', 'Direccion 16', 16),
('Empleado17', 'Apellido17', '5511000017', 'empleado17@mail.com', 'Direccion 17', 17),
('Empleado18', 'Apellido18', '5511000018', 'empleado18@mail.com', 'Direccion 18', 18),
('Empleado19', 'Apellido19', '5511000019', 'empleado19@mail.com', 'Direccion 19', 19),
('Empleado20', 'Apellido20', '5511000020', 'empleado20@mail.com', 'Direccion 20', 20);

-- TABLA caja
CREATE TABLE IF NOT EXISTS `suburbia`.`caja` (
  `id_caja` INT NOT NULL AUTO_INCREMENT,
  `estado_caja` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_caja`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO `suburbia`.`caja` (estado_caja) VALUES
('Abierta'), ('Cerrada'), ('En mantenimiento'), ('Abierta'), ('Cerrada'),
('Abierta'), ('Cerrada'), ('Abierta'), ('Cerrada'), ('Abierta'),
('Cerrada'), ('Abierta'), ('Cerrada'), ('Abierta'), ('Cerrada'),
('Abierta'), ('Cerrada'), ('Abierta'), ('Cerrada'), ('Abierta');

-- TABLA venta
CREATE TABLE IF NOT EXISTS `suburbia`.`venta` (
  `id_venta` INT NOT NULL AUTO_INCREMENT,
  `tipo_cliente` VARCHAR(45) NULL DEFAULT NULL,
  `id_cliente` INT NOT NULL,
  `id_empleado` INT NOT NULL,
  `codigo_articulo` VARCHAR(20) NOT NULL,
  `nombre_articulo` VARCHAR(45) NULL DEFAULT NULL,
  `cantidad` INT NULL DEFAULT NULL,
  `id_modo_pago` INT NOT NULL,
  `total` DECIMAL(10,2) NULL DEFAULT NULL,
  PRIMARY KEY (`id_venta`),
  INDEX `fk_venta_empleado_idx` (`id_empleado` ASC) VISIBLE,
  INDEX `fk_venta_cliente1_idx` (`id_cliente` ASC) VISIBLE,
  INDEX `fk_venta_articulo1_idx` (`codigo_articulo` ASC) VISIBLE,
  INDEX `fk_venta_metodo_pago1_idx` (`id_modo_pago` ASC) VISIBLE,
  CONSTRAINT `fk_venta_articulo1`
    FOREIGN KEY (`codigo_articulo`)
    REFERENCES `suburbia`.`articulo` (`codigo_articulo`),
  CONSTRAINT `fk_venta_cliente1`
    FOREIGN KEY (`id_cliente`)
    REFERENCES `suburbia`.`cliente` (`id_cliente`),
  CONSTRAINT `fk_venta_empleado`
    FOREIGN KEY (`id_empleado`)
    REFERENCES `suburbia`.`empleado` (`id_empleado`),
  CONSTRAINT `fk_venta_metodo_pago1`
    FOREIGN KEY (`id_modo_pago`)
    REFERENCES `suburbia`.`metodo_pago` (`id_modo_pago`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO `suburbia`.`venta` (tipo_cliente, id_cliente, id_empleado, codigo_articulo, nombre_articulo, cantidad, id_modo_pago, total) VALUES
('General', 1, 1, 'ART001', 'Articulo 1', 2, 1, 236.00),
('Particular', 2, 2, 'ART002', 'Articulo 2', 1, 2, 174.00),
('General', 3, 3, 'ART003', 'Articulo 3', 3, 3, 696.00),
('Particular', 4, 4, 'ART004', 'Articulo 4', 1, 4, 290.00),
('General', 5, 5, 'ART005', 'Articulo 5', 4, 5, 1392.00),
('Particular', 6, 6, 'ART006', 'Articulo 6', 2, 6, 812.00),
('General', 7, 7, 'ART007', 'Articulo 7', 5, 7, 2320.00),
('Particular', 8, 8, 'ART008', 'Articulo 8', 1, 8, 522.00),
('General', 9, 9, 'ART009', 'Articulo 9', 3, 9, 1740.00),
('Particular', 10, 10, 'ART010', 'Articulo 10', 2, 10, 1276.00),
('General', 11, 11, 'ART011', 'Articulo 11', 1, 1, 696.00),
('Particular', 12, 12, 'ART012', 'Articulo 12', 4, 2, 2704.00),
('General', 13, 13, 'ART013', 'Articulo 13', 1, 3, 784.00),
('Particular', 14, 14, 'ART014', 'Articulo 14', 2, 4, 1740.00),
('General', 15, 15, 'ART015', 'Articulo 15', 3, 5, 2784.00),
('Particular', 16, 16, 'ART016', 'Articulo 16', 1, 6, 904.00),
('General', 17, 17, 'ART017', 'Articulo 17', 5, 7, 5400.00),
('Particular', 18, 18, 'ART018', 'Articulo 18', 2, 8, 2288.00),
('General', 19, 19, 'ART019', 'Articulo 19', 1, 9, 1160.00),
('Particular', 20, 20, 'ART020', 'Articulo 20', 3, 10, 3672.00);
