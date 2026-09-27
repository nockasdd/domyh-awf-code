import unreal
import base64
import traceback
import json
import sys
import threading
import queue
from io import StringIO
from http.server import BaseHTTPRequestHandler, HTTPServer

# Command queue for thread-safe Game Thread execution
request_queue = queue.Queue()

class PythonExecutorHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logging
        
    def do_POST(self):
        if self.path == '/execute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                req = json.loads(post_data)
                code_base64 = req.get("code_base64", "")
                
                # Create event and result placeholder
                event = threading.Event()
                task = {
                    "code_base64": code_base64,
                    "event": event,
                    "result": None
                }
                
                # Push to Game Thread
                request_queue.put(task)
                
                # Wait for Game Thread to process
                event.wait(timeout=30.0) 
                
                result = task["result"]
                if result is None:
                    result = {"ok": False, "output": "", "error": "Execution timed out"}
                    
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                err = {"ok": False, "output": "", "error": f"HTTP Handler Error: {str(e)}"}
                self.wfile.write(json.dumps(err).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()


def start_http_server():
    server = HTTPServer(('127.0.0.1', 30011), PythonExecutorHTTPHandler)
    server.serve_forever()

# Start background HTTP server
server_thread = threading.Thread(target=start_http_server, daemon=True)
server_thread.start()


def game_thread_tick(delta_time):
    while not request_queue.empty():
        task = request_queue.get()
        code_base64 = task["code_base64"]
        
        result = {"ok": False, "output": "", "error": ""}
        
        try:
            code = base64.b64decode(code_base64).decode("utf-8")
            
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            captured_out = StringIO()
            captured_err = StringIO()
            sys.stdout = captured_out
            sys.stderr = captured_err
            
            try:
                exec_globals = {
                    "__builtins__": __builtins__,
                    "unreal": unreal,
                }
                exec(code, exec_globals)
                
                result["ok"] = True
                result["output"] = captured_out.getvalue()
                stderr_val = captured_err.getvalue()
                if stderr_val:
                    result["error"] = stderr_val
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                
        except Exception as e:
            result["ok"] = False
            result["error"] = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            
        task["result"] = result
        task["event"].set()

# Register the Slate Tick to run on Game Thread
unreal.register_slate_post_tick_callback(game_thread_tick)

unreal.log("✅ [HSA Bridge] Python Native HTTP Server v2.0.0 running on port 30011 with Game Thread integration!")
