# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add README.md
- Add CHANGELOG.md
- Add permission entity
- Add logic access permission service
- Add fetch columns, upgrade filters, and select columns in a list component
- Add joins for tables in a list component
- Add save and update images in an item component
- [Add information notifications](https://github.com/PhoenixNazarov/prompt-admin/compare/dev...dev-notifications)
- [Add widget for view self-permissions](https://github.com/PhoenixNazarov/prompt-admin/pull/25)
- [Add widget for moderate users permissions](https://github.com/PhoenixNazarov/prompt-admin/pull/25)
- [Create HealthCheck status system](https://github.com/PhoenixNazarov/prompt-admin/pull/27)
- [Upgrade status time react, add description](https://github.com/PhoenixNazarov/prompt-admin/pull/27)
- Update design: Add borders, add resizable
- Add Charts for healthCheck

### Changed

- Change update parameters watcher for a list table component
- Union requests dto in base dto request with project field
- [Change Vars, Prompts, Projects, Config endpoints with permissions](https://github.com/PhoenixNazarov/prompt-admin/pull/25)
- Unit test no need test complete unit tests
- Update filtered menu prompts with search
- [Move business logic from tables endpoints to tables services](https://github.com/PhoenixNazarov/prompt-admin/pull/25)
- [Move all get connections to ConnectionMixin](https://github.com/PhoenixNazarov/prompt-admin/pull/25)
- [Change Github actions for development and production](https://github.com/PhoenixNazarov/prompt-admin/compare/dev...dev-notifications)
- Attach menu and hint to resizable 

### Deprecated

- Format module

### Removed

- [Remove entity_data from abstract def bind_view](https://github.com/PhoenixNazarov/prompt-admin/pull/25)
- [Remove bind_view and create BaseConfigService](https://github.com/PhoenixNazarov/prompt-admin/pull/25)

### Fixed

- Fix start loading a list table component without a filter
- Bugfix load popup tables, back home, ident for test_case
- [Fix /auth/me return user password, now return password: null](https://github.com/PhoenixNazarov/prompt-admin/pull/25) 
- Fix health check, add timezone