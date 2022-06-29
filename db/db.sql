CREATE DATABASE IF NOT EXISTS conciliacion;


CREATE TABLE raw_data_decidir_card (
  id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_operacion varchar(100) NOT NULL,
  fecha_original datetime NOT NULL,
  monto float NOT NULL,
  cuotas int(11) NOT NULL,
  tarjeta varchar(100) NOT NULL,
  site varchar(100) NOT NULL,
  cod_aut varchar(100) NOT NULL,
  nro_tarjeta varchar(100) NOT NULL,
  titular varchar(255) NOT NULL,
  motivo varchar(255) DEFAULT NULL,
  validacion_domicilio varchar(50) NOT NULL,
  validacion_titular varchar(100) DEFAULT NULL,
  email varchar(255) DEFAULT NULL,
  fecha_bajada_archivo DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
  usuario varchar(255) NOT NULL,
  confirmed BOOLEAN NOT NULL DEFAULT false,
  matched BOOLEAN NOT NULL DEFAULT false,
  fecha_cierre datetime DEFAULT NULL,
  estado_cierre varchar(100) NOT NULL,
  autent_externa varchar(100) DEFAULT NULL,
  fecha_vto_cuota_1 varchar(255) DEFAULT NULL,
  lote varchar(255) DEFAULT NULL,
  timestamp varchar(100) NOT NULL,
  UNIQUE (id_operacion)
);


CREATE TABLE raw_data_decidir_pmc (
  id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_operacion varchar(100) NOT NULL,
  fecha_ultima_modificacion datetime NOT NULL,
  fecha_original datetime NOT NULL,
  monto float NOT NULL,
  cuotas int(11) NOT NULL,
  estado varchar(100) NOT NULL,
  resultado_cs varchar(100) DEFAULT NULL,
  estado_final varchar(100) DEFAULT NULL,
  autent_vbv varchar(100) DEFAULT NULL,
  tarjeta varchar(100) NOT NULL,
  site varchar(100) NOT NULL,
  cod_aut varchar(100) NOT NULL,
  nro_tarjeta varchar(100) NOT NULL,
  titular varchar(255) NOT NULL,
  tipo_doc varchar(100) NOT NULL,
  nro_doc varchar(50) NOT NULL,
  motivo varchar(255) DEFAULT NULL,
  motivo_adicional varchar(255) DEFAULT NULL,
  origen varchar(100) NOT NULL,
  validacion_domicilio varchar(50) NOT NULL,
  validacion_titular varchar(100) DEFAULT NULL,
  email varchar(255) DEFAULT NULL,
  fecha_bajada_archivo DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
  usuario varchar(255) NOT NULL,
  confirmed BOOLEAN NOT NULL DEFAULT false,
  matched BOOLEAN NOT NULL DEFAULT false,
  timestamp varchar(100) NOT NULL,  
  UNIQUE (id_operacion)
);


CREATE TABLE IF NOT EXISTS raw_data_gire(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	raw_data VARCHAR(255) NOT NULL, 
	fecha VARCHAR(50) NOT NULL,
	barcode VARCHAR(255) NOT NULL,
	importe VARCHAR(50) NOT NULL,
	archivo VARCHAR(100) NOT NULL,
	fecha_bajada_archivo DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
	usuario VARCHAR(255) NOT NULL,
	confirmed BOOLEAN NOT NULL DEFAULT false,
	matched BOOLEAN NOT NULL DEFAULT false,
	timestamp varchar(100) NOT NULL,
	unique(raw_data)
);

CREATE TABLE IF NOT EXISTS raw_data_sir(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	transaccion VARCHAR(255) NOT NULL,
	medio_de_pago VARCHAR(100) NOT NULL,
	monto FLOAT NOT NULL,	
	fecha_de_pago DATETIME NULL,	
	estado_en_sir BOOLEAN NULL,	
	dominio TEXT NULL,
	cantidad_de_dominios INTEGER NULL,
	id_tad VARCHAR(255) NULL,
	codigo_de_tramite_id VARCHAR(255) NULL,
	tipo_de_tramite VARCHAR(255) NULL,
	numero_de_factura VARCHAR(255) NULL,	
	fecha_bajada_archivo DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
	usuario VARCHAR(255) NOT NULL,
	confirmed BOOLEAN NOT NULL DEFAULT false,
	matched BOOLEAN NOT NULL DEFAULT false,
	timestamp varchar(100) NOT NULL,
	unique(transaccion),
	FOREIGN KEY (codigo_de_tramite_id) REFERENCES operation_types(id)	
);

CREATE TABLE IF NOT EXISTS operation_types(
	id varchar(50) NOT NULL PRIMARY KEY,
	name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS conciliacion(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	transaccion VARCHAR(255) NOT NULL,
	medio_de_pago VARCHAR(100) NOT NULL,
	monto FLOAT NOT NULL,
	id_tad INTEGER NOT NULL,
	fecha_de_pago DATETIME NULL,
	dominios TEXT NOT NULL,
	codigo_de_tramite_id VARCHAR(50) NOT NULL,
  numero_de_factura VARCHAR(255) NULL,
  estado_en_sir BOOLEAN NULL,	
	processed_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	unique(transaccion),
	FOREIGN KEY (codigo_de_tramite_id) REFERENCES operation_types(id)	
);


CREATE TABLE IF NOT EXISTS results(
	id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	month INTEGER NOT NULL,
	year INTEGER NOT NULL,
	amount FLOAT NOT NULL DEFAULT 0,
	payment_method VARCHAR(100) NOT NULL
);


