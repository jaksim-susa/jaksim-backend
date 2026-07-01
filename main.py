from fastapi import FastAPI

app = FastAPI(title="JAKSHIM SUSA API")

@app.get("/")
async def root():
    return {"message": "JAKSHIM SUSA API is running! 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}