import subprocess
import threading
import uvicorn

# Run FastAPI
def run_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

# Run Streamlit
def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py", "--server.port", "10000"])

if __name__ == "__main__":
    threading.Thread(target=run_fastapi).start()
    run_streamlit()
