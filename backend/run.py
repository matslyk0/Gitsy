import uvicorn
from main import create_app

app = create_app()

config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, reload=True)
server = uvicorn.Server(config)
server.run()