-- PA_VAR
create table pa_var
(
    id          serial
        constraint pa_var_pk
            primary key,
    time_create timestamp default now(),

    "key"       varchar(100)   not null,
    "value"     varchar(20000) not null
);

create unique index pa_var_key on pa_var
    ("key");

