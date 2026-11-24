import subprocess
import time
import json
import base64
import urllib.request
import os

try:
    import websocket
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "websocket-client"])
    import websocket

def capture_dashboard_screenshot():
    user_data_dir = r"C:\Users\LENOVO\AppData\Local\Temp\chrome_cdp"
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # Start Chrome with remote debugging
    cmd = [
        chrome_path,
        "--headless=new",
        "--remote-debugging-port=9222",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={user_data_dir}",
        "--window-size=1920,1200"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(2)
    
    try:
        # Create target
        req = urllib.request.Request("http://127.0.0.1:9222/json/new?http://localhost:8501", method="PUT")
        with urllib.request.urlopen(req) as response:
            target = json.loads(response.read().decode())
        
        ws_url = target.get("webSocketDebuggerUrl")
        print("Connected to WebSocket:", ws_url)
        
        ws = websocket.create_connection(ws_url)
        
        # Enable page
        ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
        ws.recv()
        
        print("Waiting 10 seconds for Streamlit charts to render...")
        time.sleep(10)
        
        # Capture screenshot
        ws.send(json.dumps({"id": 2, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        result = json.loads(ws.recv())
        
        # Sometimes extra events arrive, wait for id 2
        while result.get("id") != 2:
            result = json.loads(ws.recv())
            
        data = result["result"]["data"]
        img_bytes = base64.b64decode(data)
        
        out_path = os.path.abspath("results/charts/dashboard_overview_screenshot.png")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(img_bytes)
            
        print(f"Successfully saved screenshot to {out_path} ({len(img_bytes)} bytes)")
        ws.close()
        
    finally:
        proc.terminate()
        proc.wait(timeout=5)

if __name__ == "__main__":
    capture_dashboard_screenshot()
