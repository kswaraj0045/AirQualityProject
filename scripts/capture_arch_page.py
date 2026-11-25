import subprocess
import time
import json
import base64
import urllib.request
import os
import websocket

def capture_arch_page():
    user_data_dir = r"C:\Users\LENOVO\AppData\Local\Temp\chrome_cdp_arch"
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
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
        req = urllib.request.Request("http://127.0.0.1:9222/json/new?http://localhost:8501", method="PUT")
        with urllib.request.urlopen(req) as response:
            target = json.loads(response.read().decode())
        
        ws_url = target.get("webSocketDebuggerUrl")
        ws = websocket.create_connection(ws_url)
        
        ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
        ws.send(json.dumps({"id": 2, "method": "Runtime.enable"}))
        time.sleep(5)
        
        # Click About Architecture radio button
        js_code = """
        (function() {
            const labels = Array.from(document.querySelectorAll('label'));
            const target = labels.find(l => l.innerText.includes('About Architecture'));
            if (target) {
                target.click();
                return 'Clicked About Architecture';
            }
            return 'Label not found';
        })();
        """
        ws.send(json.dumps({
            "id": 3,
            "method": "Runtime.evaluate",
            "params": {"expression": js_code, "returnByValue": True}
        }))
        res = json.loads(ws.recv())
        while res.get("id") != 3:
            res = json.loads(ws.recv())
        print("JS result:", res)
        
        time.sleep(3)
        
        # Scroll down
        scroll_js = """
        (function() {
            const container = document.querySelector('[data-testid="stAppViewContainer"]') || window;
            if (container.scrollTop !== undefined) {
                container.scrollTop = 500;
            } else {
                window.scrollTo(0, 500);
            }
            return 'Scrolled';
        })();
        """
        ws.send(json.dumps({
            "id": 4,
            "method": "Runtime.evaluate",
            "params": {"expression": scroll_js, "returnByValue": True}
        }))
        time.sleep(2)

        ws.send(json.dumps({"id": 5, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        res = json.loads(ws.recv())
        while res.get("id") != 5:
            res = json.loads(ws.recv())
            
        data = res["result"]["data"]
        img_bytes = base64.b64decode(data)
        out_path = os.path.abspath("results/charts/dashboard_arch_page.png")
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print("Saved architecture page screenshot to", out_path)
        ws.close()
    finally:
        proc.terminate()
        proc.wait(timeout=5)

if __name__ == "__main__":
    capture_arch_page()
