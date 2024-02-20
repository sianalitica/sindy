drop table if exists documentos_brutos;
drop table if exists documentos_info;
drop table if exists empresas;


create table empresas (

    id bigint(255) primary key auto_increment,
    nome varchar(255) not null,
    cod_cvm varchar(20) not null,

    index (cod_cvm),
    unique(cod_cvm)

) engine=myisam default CHARSET=utf8mb4; 

insert into empresas values (null, 'Suzano S/A', 13986);

create table documentos_info (

    id bigint(255) primary key auto_increment,
    empresa_id bigint(255) not null,
    categoria varchar(255) not null,
    tipo varchar(255) not null,
    especie varchar(255) not null,
    data_referencia datetime,
    data_entrega datetime,
    status tinyint(1) not null,
    v int(10) not null,
    modalidade varchar(255) not null,
    link_documento varchar(150),
    link_type tinyint(1) not null,
    
    foreign key (empresa_id) 
    references empresas(id)

) engine=myisam default CHARSET=utf8mb4; 

create table documentos_brutos (

    id bigint(255) primary key auto_increment,
    documento_info_id bigint(255) not null,
    texto text not null,
    ext varchar(10) not null,

    foreign key (documento_info_id) 
    references documentos_info(id)

) engine=myisam default CHARSET=utf8mb4; 