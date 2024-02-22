import uvicorn


def main():
    uvicorn.run(
        "key_control_server.server:app",
        host="0.0.0.0",
        port=80,
        log_level="info",
    )
