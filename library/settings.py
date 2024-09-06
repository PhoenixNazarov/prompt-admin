from promptadmin.types import Settings as PromptAdminSettings


class Settings(PromptAdminSettings):
    app: str = 'prompt-admin'
    anthropic_key: str = ''
    test_rerun_timeout: int = 60 * 60 * 6


SETTINGS = Settings()
