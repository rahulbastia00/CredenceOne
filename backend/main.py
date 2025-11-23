# ./main.py
if __name__ == '__main__':
    import uvicorn
    # Import the 'app' object defined in app/main.py
    from app.main import app 
    
    uvicorn.run(app, host="127.0.0.1", port=8000)