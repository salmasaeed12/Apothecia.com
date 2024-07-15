if __name__ == "__main__":
    import uvicorn
    #! in the production mode, we need to change the Log level to "info" and reload to False
    uvicorn.run("app:app", host="127.0.0.1", port=5000, log_level="debug", reload=True)
