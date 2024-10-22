# Prompt-Admin

## Projects

#TODO

## Prompts

#TODO

## Blog

#TODO

## Status

#TODO

## Tables

#TODO

## User Permissions

For all permissions value mapping table

| Value | Meaning                              |
|-------|--------------------------------------|
| `0`   | Disable                              |
| `1`   | Enable, Can read                     |
| `2`   | Enable, Can read and write (process) |

### Global permissions exclude projects

| Permission key    | Default | Description                                               |
|-------------------|---------|-----------------------------------------------------------|
| _config_tables_   | `1`     | Edit config mappings, mappings entity and etc             |
| _config_accounts_ | `0`     | Edit account permissions configs                          |
| _healthcheck_     | `1`     | Access to monitor healthcheck and add new check endpoints |

### Projects permissions

If does not set `project` permission, all related `project_*` permission will no active

| Permission key          | Default | Description                                       |
|-------------------------|---------|---------------------------------------------------|
| _project_               | `0`     | Access to the project in general                  |
| _project_prompt_        | `1`     | Access to view or edit in workplace prompts       |
| _project_blog_          | `1`     | Access to view or edit project`s blog             |
| _project_variables_     | `1`     | Access to view or edit project`s variables        |
| _project_status_        | `1`     | Access to view project status and run unit status |
| _project_synchronize_   | `0`     | Access to manual synchronize                      |
| _project_tables_upload_ | `1`     | Access to manual change tables schema             |
| _project_tables_        | `1`     | Access to write or edit project`s tables          |
