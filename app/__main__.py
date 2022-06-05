import uvicorn


uvicorn.run(
    'app.app:app_instance',
    reload=True,
    port=8002,
)
