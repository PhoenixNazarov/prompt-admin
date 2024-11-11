# Prompt-Admin

Prompt-Admin is a system designed for integrating prompt-based classes into your Python application. It allows you to
conveniently moderate your prompts through an admin panel.

## How Install
To get Prompt-Admin up and running, follow these installation steps:

### 1. Database Setup

First, you need to set up your database. Run the SQL script located at `server/promptadmin_server/data/init.sql`. This script will initialize your database, which is vital for the backend to function properly. Automation for this process is planned for future releases.

### 2. Docker Installation

Prompt-Admin uses Docker for easy deployment. Ensure Docker and Docker Compose are installed on your system. If not, please install them from [Docker's official site](https://docker.com).

Once Docker is set up, you can proceed with the deployment of Prompt-Admin using Docker Compose. Create a `docker-compose.yml` file in your project directory with the following configuration:

```yaml
services:
  prompt-admin:
    container_name: prompt-admin
    image: phoenixnazarov/prompt-admin:dev
    restart: always
    ports:
      - "80:80"
    environment:
      PA_DATABASE_USERNAME: postgres
      PA_DATABASE_PASSWORD: password
      PA_DATABASE_HOST: 192.168.0.1
      PA_DATABASE_PORT: 5432
      PA_DATABASE_DATABASE: prompt-admin
      PA_CONNECTION_PROJECT1: postgresql://postgres:password@192.168.0.2:5432/totalis
      PA_CONNECTION_PROJECT2: postgresql://postgres:password@192.168.0.3:5432/totalis
      PA_SYNC_ENDPOINT_PROJECT1: https://project1.ai/api/prompt-admin
      PA_SYNC_SECRET_PROJECT1: 1234
      PA_SYNC_ENDPOINT_PROJECT2: https://project2.ai/api/prompt-admin
      PA_SYNC_SECRET_PROJECT2: qwer
      # Optional
      PA_OPENAI_KEY: qwe
      PA_ANTHROPIC_KEY: qwe
      AWS_SECRET_KEY: qwe
      AWS_ACCESS_KEY: qwe
      AWS_REGION: qwe
```

## Projects

Prompt-Admin supports the integration of multiple projects, each of which can be configured within the environment variables using the format: `PA_CONNECTION_{PROJECT}`. For instance, a database connection can be established using a connection string like `postgresql://postgres:password@192.168.0.2:5432/totalis`. Currently, only PostgreSQL databases are supported.

Within the admin panel, users have the capability to manually specify where in the database the prompts are located. This is managed under the `Table` section of the admin panel, where users can simply fill out the Mapping to associate prompt data with specific database tables.

Additionally, for certain projects, it might be necessary to define synchronization and testing functionalities. This can be done using the following environment variables:
- `PA_SYNC_ENDPOINT_{PROJECT}`: Specifies the endpoint for automatic synchronization of prompts from the hosted application into the database.
- `PA_SYNC_SECRET_{PROJECT}`: Defines a secret key required for secure communication between the application and the synchronization endpoint.

These configurations allow for advanced operations such as:
1. Automated synchronization of prompts into the database from the application.
2. Automated testing processes to ensure prompt and application integrity and functionality.

Through this setup, Prompt-Admin offers a robust system for managing and maintaining multiple projects efficiently from a central admin panel, enhancing productivity and operational control.


## Library


The Prompt-Admin provides a Python library that facilitates automated synchronization between the admin panel and applications. This library is available on PyPI and can be installed using:

```
pip3 install prompt-admin
```

### Using the Library

Once you have installed the `prompt-admin` package, you can easily integrate prompt management into your applications by using decorators and service models provided by the library. This setup simplifies the process of using prompts in your application code.

Here’s how to set up and use the library:

#### Importing Necessary Modules

Start by importing the necessary classes and decorators from the library:

```python
from promptadmin.prompt_service.decorator import bind_prompt
from promptadmin.prompt_service.models import OpenaiModelService
from promptadmin.prompt_service.models.openai_model import OpenaiModelResponse
```

#### Setting Up the Model Service

Initialize your model service by specifying the type of prompt position and the model you are going to use. Here is an example using `gpt-4o-mini`:

```python
model_service = OpenaiModelService(prompt_position='system', model='gpt-4o-mini')
```

#### Creating a Service Class

You can define a service class that utilizes the `bind_prompt` decorator to associate class methods with specific database prompts. This structure allows for dynamic interaction with different prompts based on your requirements:

```python
class PublicPromptService:
    @bind_prompt(
        'table',
        'field',
        'field_name',
        'name',
        model_service=model_service,
    )
    async def demo(self) -> OpenaiModelResponse:
        """ 
        This method serves as a prompt handler in the system. It retrieves user inputs and utilizes model behavior to provide responses.
        """
```

#### Utilizing the Service

Finally, you can use instances of your service class to interact with the system and generate responses based on user input and historical data:

```python
public_prompt_service = PublicPromptService()

def find_prompt_from_database():
    ...

response = await public_prompt_service.demo(
    prompt=find_prompt_from_database(),
    history=history
)
```

The provided framework simplifies the integration of machine learning models and prompt management into your application, streamlining the development and deployment of AI-driven services.


## Prompts

### Overview

In the Prompt-Admin system, prompts act as customizable query templates that facilitate dynamic interactions between your application and its users. After endpoints for prompts are created, they are synchronized and displayed within the admin panel client, where they can be fully managed.

### Editing and Management

The admin panel provides a user-friendly interface for prompt management where you can edit and configure each prompt to meet specific needs of your project. It allows for versatile modifications including the addition of contextual information or specific conditions under which the prompts should be triggered.

### Contextual Execution

Prompts in Prompt-Admin can be executed based on specific contexts, enhancing their flexibility and application across different scenarios. Users can configure prompts to respond according to the varying conditions or queries presented by end users, ensuring a tailored interaction that improves user experience and engagement.

### Variable Insertion

To add an additional layer of customization, prompts support the insertion of variables using Jinja templating. This feature enables the dynamic insertion of environment-specific variables directly into the prompts. It allows prompts to be more adaptive and responsive to the changing conditions or data in the environment.

### Testing and Validation

Within the Prompt-Admin panel, you can also test your prompts to ensure they meet the required format and function as expected. This feature is crucial for maintaining the integrity and reliability of interactions driven by these prompts. The system allows you to validate the format correctness and functional behavior of the prompts before deploying them into a live environment.

Through these capabilities, Prompt-Admin ensures that managing and deploying prompts is a seamless and robust process, significantly boosting the efficiency and effectiveness of your application's interactions with its users.

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
