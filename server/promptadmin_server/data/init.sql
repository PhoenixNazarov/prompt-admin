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

create table pa_input
(
    id           serial
        constraint pa_input_pk
            primary key,
    time_create  timestamp              default now(),
    macro        varchar(120)  not null,
    macro_value  varchar(500)  not null,
    description  varchar(1000) not null default '',

    default_type varchar(20)   not null default 'str',
    "default"    varchar(1000) not null default 'str'
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
    field_name      varchar(128)  not null,
    field_order     varchar(128),
    "desc"          boolean   default false,
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
            on delete CASCADE,
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
    id          serial
        constraint pa_account_pk
            primary key,
    time_create timestamp default now(),
    login       varchar(45) not null,
    password    varchar(64)
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


-- PA_PROMPT_AUDIT
create table pa_prompt_audit
(
    id          serial
        constraint pa_prompt_audit_pk
            primary key,
    time_create timestamp default now(),

    "table"     varchar(128)   not null,
    field       varchar(128)   not null,
    "name"      varchar(128),
    mapping_id  integer
        constraint pa_prompt_audit_mapping_id_fk
            references pa_mapping
            on delete SET NULL,
    prompt_id   integer        not null,
    "value"     varchar(20000) not null,
    account_id  integer
        constraint pa_prompt_audit_account_id_fk
            references pa_account
            on delete SET NULL
);


-- PA_BLOG_GROUP
create table pa_blog_group
(
    id          serial
        constraint pa_blog_group_pk
            primary key,
    time_create timestamp default now(),

    project     varchar(200) not null,
    title       varchar(200) not null
);


-- PA_BLOG_POST
create table pa_blog_post
(
    id          serial
        constraint pa_blog_post_pk
            primary key,
    time_create timestamp default now(),

    project     varchar(200)   not null,
    title       varchar(200)   not null,
    content     varchar(40000) not null,
    group_id    integer
        constraint pa_blog_post_group_id_fk
            references pa_blog_group
            on delete SET NULL
);


-- PA_SYNC_DATA
create table pa_sync_data
(
    id                        serial
        constraint pa_sync_data_pk
            primary key,
    time_create               timestamp default now(),

    service_model_info        varchar(30000)  not null,
    template_context_type     varchar(50000)  not null,
    template_context_default  varchar(100000) not null,
    history_context_default   varchar(30000)  not null,
    parsed_model_type         varchar(30000),
    parsed_model_default      varchar(30000),
    fail_parse_model_strategy varchar(50)
);


-- PA_UNIT_TEST
create table pa_unit_test
(
    id                  serial
        constraint pa_unit_test_pk
            primary key,
    time_create         timestamp   default now(),

    sync_data_id        integer
        constraint pa_unit_test__sync_id_fk
            references pa_sync_data
            on delete CASCADE,
    "name"              varchar(128),

    test_status         varchar(15) default 'wait' not null,
    test_preview        varchar(50000),
    test_response_model varchar(30000),
    test_exception      varchar(10000)
);