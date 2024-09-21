from promptadmin.types import Settings as PromptAdminSettings


class Settings(PromptAdminSettings):
    app: str = 'prompt-admin'
    anthropic_key: str = ''
    aws_secret_key: str = ''
    aws_access_key: str = ''
    aws_region: str = ''


SETTINGS = Settings()
