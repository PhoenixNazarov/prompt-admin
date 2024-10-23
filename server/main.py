import uvicorn

from promptadmin_server.api.app import app
from settings import SETTINGS

if __name__ == "__main__":
    uvicorn.run(app, host=SETTINGS.host, port=SETTINGS.port)  # , log_config=None
