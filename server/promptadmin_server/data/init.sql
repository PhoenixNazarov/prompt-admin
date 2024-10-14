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

create unique index pa_account__login__uindex
    on pa_account (login);


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

create unique index pa_access_token__token__uindex
    on pa_access_token (token);

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
    template_context_default  varchar(150000) not null,
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
    test_response_model varchar(50000),
    test_exception      varchar(10000)
);

create unique index pa_unit_test__sync_data_id__uindex
    on pa_unit_test (sync_data_id, "name");


-- PA_TEST_RESULT
create table pa_test_result
(
    id              serial
        constraint pa_test_result_pk
            primary key,
    time_create     timestamp default now(),

    connection_name varchar(128) not null,

    created         float        not null,
    duration        float        not null,
    passed          integer      not null,
    skipped         integer      not null,
    "error"         integer      not null,
    failed          integer      not null,
    total           integer      not null,
    collected       integer      not null
);
create unique index pa_test_result_ident_uindex
    on pa_test_result (connection_name, created, duration);

-- PA_TEST_RESULT_RAW
create table pa_test_result_raw
(
    id             serial
        constraint pa_test_result_raw_pk
            primary key,
    time_create    timestamp default now(),

    test_result_id integer
        constraint pa_test_result_raw__test_res_fk
            references pa_test_result
            on delete CASCADE      not null,
    raw_file       varchar(300000) not null
);

create unique index pa_test_result_raw__test_res__uindex
    on pa_test_result_raw (test_result_id);


-- PA_TEST_CASE
create table pa_test_case
(
    id                serial
        constraint pa_test_case_pk
            primary key,
    time_create       timestamp default now(),

    test_result_id    integer
        constraint pa_test_case__test_res_fk
            references pa_test_result
            on delete CASCADE      not null,

    nodeid            varchar(200) not null,
    lineno            integer      not null,
    outcome           varchar(12)  not null,

    metadata_url      varchar(200),
    metadata_scenario varchar(200),

    setup_duration    float        not null,
    setup_outcome     varchar(12)  not null,

    call_duration     float,
    call_outcome      varchar(12),

    teardown_duration float        not null,
    teardown_outcome  varchar(12)  not null
);

create index pa_test_case__test_result__index
    on pa_test_case (test_result_id);

create unique index pa_test_case__test_result_node__uindex
    on pa_test_case (test_result_id, nodeid);


-- PA_TEST_CASE_INFO
create table pa_test_case_info
(
    id                 serial
        constraint pa_test_case_info_pk
            primary key,
    time_create        timestamp default now(),

    test_case_id       integer
        constraint pa_test_case_info__test_case_fk
            references pa_test_case
            on delete CASCADE not null,

    setup_longrepr     varchar(5000),
    call_crash_path    varchar(200),
    call_crash_lineno  integer,
    call_crash_message varchar(300),
    request            varchar(10000),
    response           varchar(10000)
);

create unique index pa_test_case_info__test_case__index
    on pa_test_case_info (test_case_id);


create table pa_table_schema
(
    id           serial
        constraint pa_table_schema_pk
            primary key,
    time_create  timestamp default now(),

    project      varchar(100) not null,
    table_schema json         not null
);

create unique index pa_table_schema__project_uindex
    on pa_table_schema (project);
