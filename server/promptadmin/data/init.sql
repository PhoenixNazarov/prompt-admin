create table pa_macro
(
    id          serial
        constraint pa_macro_pk
            primary key,
    time_create timestamp              default now(),
    macro       varchar(120)  not null,
    macro_value varchar(500)  not null,
    description varchar(1000) not null default ''
);

create table pa_mapping
(
    id              serial
        constraint pa_mapping_pk
            primary key,
    time_create     timestamp default now(),
    "table"         varchar(128)  not null,
    field           varchar(128)  not null,
    description     varchar(1000) not null,
    field_name      varchar(128),
    connection_name varchar(128)  not null
);

create unique index pa_mapping_table_field_uind on pa_mapping
    ("table", field, connection_name);


create table pa_variable
(
    id          serial
        constraint pa_variable_pk
            primary key,
    time_create timestamp default now(),
    name        varchar(128) not null,
    description varchar(128) not null,
    value       varchar(128) not null,
    template    boolean   default FALSE
);


create table pa_mapping_entity
(
    id              serial
        constraint pa_mapping_entity_pk
            primary key,
    time_create     timestamp default now(),
    connection_name varchar(128),
    "table"         varchar(128),
    field           varchar(128),
    "name"          varchar(128),
    mapping_id      integer
        constraint pa_mapping_entity__id_fk
            references pa_mapping
            on delete SET NULL,
    entity          varchar(128) not null,
    entity_id       integer      not null
);

create table pa_output
(
    id          serial
        constraint pa_output_pk
            primary key,
    time_create timestamp default now(),
    "output"    varchar(1000)
);



-- PA_ACCOUNT
create table pa_account
(
    id               serial
        constraint pa_account_pk
            primary key,
    time_create      timestamp   default now(),
    login            varchar(45) not null,
    password         varchar(64)
);


-- PA_ACCESS_TOKEN
create table pa_access_token
(
    id           serial
        constraint pa_access_token_pk
            primary key,
    time_create  timestamp default now(),
    token        varchar(45) not null,
    access_level integer   default 0,
    time_active  timestamp default CURRENT_TIMESTAMP,
    account_id   integer
        constraint pa_authentication_account_id__fk
            references pa_account
);