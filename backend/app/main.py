from fastapi import FastAPI

app = FastAPI(
    title="Usher Ministry Management System API",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {"status": "ok"}
