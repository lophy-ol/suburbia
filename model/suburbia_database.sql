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

-- -----------------------------------------------------
-- Table `suburbia`.`almacen`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `suburbia`.`almacen` (
  `idalmacen` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `ubicacion` VARCHAR(45) NOT NULL,
  `capacidad_maxima` INT NOT NULL,
  `estado` ENUM('Activo', 'Inactivo') NOT NULL,
  PRIMARY KEY (`idalmacen`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `suburbia`.`caja`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `suburbia`.`caja` (
  `idcaja` INT NOT NULL AUTO_INCREMENT,
  `saldo_inicial` DECIMAL(10,2) NOT NULL,
  `fecha_apertura` DATETIME NOT NULL,
  `saldo_final` DECIMAL(10,2) NOT NULL,
  `fecha_cierre` DATETIME NOT NULL,
  PRIMARY KEY (`idcaja`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `suburbia`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `suburbia`.`cliente` (
  `id_cliente` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(100) NULL DEFAULT NULL,
  `Apellido` VARCHAR(100) NULL DEFAULT NULL,
  `Telefono` VARCHAR(20) NULL DEFAULT NULL,
  `Correo` VARCHAR(100) NULL DEFAULT NULL,
  `Direccion` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`id_cliente`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `suburbia`.`sucursal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `suburbia`.`sucursal` (
  `id_sucursal` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `direccion` VARCHAR(45) NOT NULL,
  `ciudad` VARCHAR(45) NOT NULL,
  `estado` VARCHAR(45) NOT NULL,
  `codigo_postal` VARCHAR(45) NOT NULL,
  `telefono` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_sucursal`),
  UNIQUE INDEX `telefono_UNIQUE` (`telefono` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `suburbia`.`empleado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `suburbia`.`empleado` (
  `ID_Empleado` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(45) NOT NULL,
  `Apellido` VARCHAR(45) NOT NULL,
  `Cargo` VARCHAR(45) NOT NULL,
  `Fecha_Contratacion` DATE NOT NULL,
  `Salario` DECIMAL(10,0) NOT NULL,
  `ID_Sucursal` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`ID_Empleado`),
  INDEX `fk_Empleado_Sucursal1_idx` (`ID_Sucursal` ASC),
  CONSTRAINT `fk_Empleado_Sucursal1`
    FOREIGN KEY (`ID_Sucursal`)
    REFERENCES `suburbia`.`sucursal` (`id_sucursal`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `suburbia`.`metodo_pago`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `suburbia`.`metodo_pago` (
  `idmetodo_pago` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  `descripcion` VARCHAR(100) NULL DEFAULT NULL,
  `activo` ENUM('Sí', 'No') NOT NULL DEFAULT 'Sí',
  PRIMARY KEY (`idmetodo_pago`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `suburbia`.`proveedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `suburbia`.`proveedor` (
  `id_proveedor` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `telefono` VARCHAR(45) NOT NULL,
  `correo` VARCHAR(45) NOT NULL,
  `direccion` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_proveedor`),
  UNIQUE INDEX `correo_UNIQUE` (`correo` ASC),
  UNIQUE INDEX `telefono_UNIQUE` (`telefono` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;