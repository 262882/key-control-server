import uvicorn

uvicorn.run("server:app", host="0.0.0.0", log_level="info")