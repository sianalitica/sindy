
create table if not exists empresas (

    id bigint(255) primary key auto_increment,
    nome varchar(255) not null,
    cod_cvm varchar(20) not null,

    index (cod_cvm),
    unique(cod_cvm)

) engine=myisam default CHARSET=utf8mb4; 


create table if not exists documentos_info (

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


create table if not exists documentos_brutos (

    id bigint(255) primary key auto_increment,
    documento_info_id bigint(255) not null,
    texto longtext not null,
    ext varchar(10) not null,

    foreign key (documento_info_id) 
    references documentos_info(id)

) engine=myisam default CHARSET=utf8mb4; 


create table if not exists dados_brutos_analisados_documentos (

    id bigint(255) primary key auto_increment,
    documento_bruto_id bigint(255) not null,
    dado_bruto text not null,

    foreign key (documento_bruto_id) 
    references documentos_brutos(id)

) engine=myisam default CHARSET=utf8mb4; 


create table if not exists indicadores_empresa (

    id bigint(255) not null,
    empresa_id bigint(255) not null,
    nome varchar(255) not null,
    slug varchar(255) not null,

    foreign key(empresa_id)
    references empresas(id)

 ) engine=myisam default CHARSET=utf8mb4; 


create table if not exists valor_indicador_empresa (

    id bigint(255) not null,
    indicador_empresa_id bigint(255) not null,
    valor decimal(19,9),
    tipo varchar(100),
    data_ini date not null,
    data_fim date not null,
    referencia varchar(100),

    unique(referencia),

    foreign key(indicador_empresa_id)
    references indicadores_empres(id)

 ) engine=myisam default CHARSET=utf8mb4; 



