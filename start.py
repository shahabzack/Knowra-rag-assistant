# start.py
import subprocess
import threading

def run_fastapi():
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"])

def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"])

if __name__ == "__main__":
    t1 = threading.Thread(target=run_fastapi)
    t2 = threading.Thread(target=run_streamlit)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
