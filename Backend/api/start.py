from main import app
import uvicorn

uvicorn.run(app, port = 8000, host='0.0.0.0')