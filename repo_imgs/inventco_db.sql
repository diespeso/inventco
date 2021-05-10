create database INVENTCO;
use INVENTCO;

drop table producto;
create table producto(
	nombre varchar(50) not null,
    costo_pedido double not null,
    costo_faltante double not null,
    costo_inventario double not null,
    inventario_inicial int not null,
    primary key (nombre)
);

drop table prediccion;
create table prediccion(
	nombre_producto varchar(50) not null,
    mes varchar(20) not null,
    demanda int,
    primary key (nombre_producto, mes),
    foreign key (nombre_producto) references producto(nombre)
);

drop table experimento;
create table experimento(
	nombre_producto varchar(50) not null,
    numero int not null,
    punto_reorden int not null,
    cantidad_orden int not null,
    primary key (nombre_producto, numero),
    foreign key (nombre_producto) references producto(nombre)
);

drop table simulacion;
create table simulacion(
	nombre_producto varchar(50) not null,
    no_experimento int not null,
    mes varchar(20) not null,
    inv_inicial int not null,
    inv_final int not null,
    faltante int,
    orden int,
    primary key (nombre_producto, no_experimento, mes),
    foreign key (mes) references prediccion(mes)
);