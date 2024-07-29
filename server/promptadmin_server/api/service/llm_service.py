import openai


class LlmService:
    def __init__(self):
        pass

    async def request(self):
        pass

    async def request_openai(self):
        output = await openai.AsyncClient(api_key=None).chat.completions.create(

        )

    async def request_anthropic(self):
        pass
