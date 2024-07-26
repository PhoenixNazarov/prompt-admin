
from pydantic import BaseModel, computed_field

from promptadmin.prompt_service.decorator import bind_prompt
from promptadmin.prompt_service.models.anthropic import AnthropicModelResponse
from promptadmin.sync.collector import collect


class Coach(BaseModel):
    name: str


class User(BaseModel):
    name: str

    ha: str = '123'

    @computed_field
    @property
    def test(self) -> str:
        return self.ha + 'test'


class UserContext(BaseModel):
    user: User
    coach: Coach


class PromptService:
    @bind_prompt('po_prompt', 'name', 'extracting_doc_structure')
    async def extracting_doc_structure(self, user_context: UserContext) -> AnthropicModelResponse:
        """ Method for extract doc structure """


prompt_service = PromptService()

# user_context_example = UserContext(user=User(name='123'))

print([i.dict() for i in collect()])


async def main():
    await prompt_service.extracting_doc_structure(user_context_example, prompt='asd')
    result = await prompt_service.extracting_doc_structure(user_context=user_context_example, prompt='asd')

# asyncio.run(main())
