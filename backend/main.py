from fastapi import FastAPI

app = FastAPI(
    title="Agentic AI for Tata Capital",
    description="mock backend",
    version="1.0.0"
)

# health check endpoint
@app.get("/")
def read_root():
    return{"status": "ok",
           "message": "Mock APi test"
           }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)