from promptadmin.types import Settings as PromptAdminSettings


class Settings(PromptAdminSettings):
    app: str = 'prompt-admin'
    anthropic_key: str = ''


SETTINGS = Settings()
