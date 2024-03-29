# Copyright (c) 2023 Gianmaria Castaldini

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# In order to start the app, simply run this file.
# Modify first the capitalized parameter to match preferences!!!



import uvicorn
from app.main import app
import psutil 
import sys
# used to retrive openapi schema from fastAPI and save it in a file
import requests

### Parameters for uvicorn server
# HOST = "127.0.0.1"
HOST = "0.0.0.0"
PORT = 12345
WORKERS = 1
OVERRIDE = False # Force close any other service on the same port (Not a good practice, must be used carefully or modified)

# Check if the application is frozen (built with PyInstaller)
if getattr(sys, 'frozen', False):
    # Application is running from a PyInstaller bundle
    RELOAD = False
else:
    # Application is running in a development environment
    RELOAD = True
APPPATH = "app.main:app"

### Parameters for openapi schema autosave
OPENAPI = False # If True, save a local copy of the openapi schema created by fastAPI
FILEPATH = "/openapi.json"  # the file path



def serve(host: str, port: int, workers: int, override: bool = False, reload: bool = False, appPath: str = ""):
    """This method start the FastAPI application using uvicorn

    Args:
        host (str): the app ip address
        port (int): the app port
        workers (int): if need multiprocess. 
        override (bool, optional): !!!NOT THE BEST PRACTICE!!! If want to terminate a process that is already running on the port. Defaults to False.
        reload (bool, optional): is passed as the reload parameter of uvicorn. auto restart the app at any changes in the code.
        appPath (str, optional): if reload is True, the app argument must be passed as a string (like the one used directly in terminal)
    """    
    if override:
        # !!!NOT THE BEST PRACTICE!!! Check if a process is already running on the specified port and terminate it if found 
        if is_process_running_on_port(port):
            terminate_process_on_port(port)

    # Start the Uvicorn server
    if reload:
        if appPath == "":
            raise RuntimeError("The parameter appPath must be defined when reload is True! (something like app.main:app)")
        uvicorn.run(appPath, port=port, host=host, workers=workers, reload=reload)
    else:
        uvicorn.run(app, port=port, host=host, workers=workers, reload=reload)




def is_process_running_on_port(port: int) -> bool:
    """Try to connect on a service on a specific port and return True if the service is running
    Args:
        port (int): TCP/UDP PORT

    Returns:
        bool: is the service running on that port?
    """    
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr.port == port:
            return True
    return False

def terminate_process_on_port(port: int, startWith: str = ""):
    """Terminate a service on a specific TCP/UDP port.

    Args:
        port (int): TCP/UDP port.
        startWith (str, optional): If provided, only terminate processes whose name starts with this string.
    """    

    def _kill(process, target_port):
        """Terminate a process if it's using the specified port."""
        for conn in process.connections(kind="inet"):
            if conn.laddr.port == target_port:
                print(f"Terminating process {process.pid}")
                try:
                    process.terminate()
                except psutil.Error as e:
                    print(f"Error terminating process {process.pid}: {e}")

    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if startWith and proc.info["name"].startswith(startWith):
                _kill(proc, port)
            elif not startWith:
                _kill(proc, port)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def hideConsole():
    """when packaged with pyinstaller (console mode), if you want to hide (not close) the console, use this method
    """    
    try:
        import ctypes
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)
    except:
        pass


def generateAPIdocs(api_url: str, output_file: str):
    """Auto calls the /openapi.json endpoint of fastAPI and save the content in a json file.

    Args:
        api_url (str): the application openapi.json endpoint
        output_file (str): the name of the output file (relative path allowed)
    """    
    response = requests.get(api_url)
    
    with open('openapi.json', 'w') as f:
        f.write(response.text)



if __name__ == "__main__":

    # hideConsole()  #hide console. will work only on packaged distribution
    process = serve(HOST, PORT, WORKERS, OVERRIDE, reload=RELOAD, appPath=APPPATH)
    if OPENAPI:
        generateAPIdocs(f'http://{HOST}:{PORT}/openapi.json', FILEPATH)

    