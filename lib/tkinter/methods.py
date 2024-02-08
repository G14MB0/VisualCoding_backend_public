from tkinter import Tk, filedialog
from queue import Queue
import threading

def thread_safe_file_dialog(q, file_type):
    try:
        root = Tk()
        root.withdraw()  # Hide the main window
        root.attributes("-topmost",True)

        if file_type:
            file_path = filedialog.askopenfilename(filetypes=[(f"{file_type} files", f"*.{file_type}")])
        else:
            file_path = filedialog.askopenfilename()
        root.destroy()
        q.put(file_path)
    except:
        return

async def run_file_dialog(file_type: str = "") -> str:
    q = Queue()
    dialog_thread = threading.Thread(target=thread_safe_file_dialog, args=(q, file_type), daemon=True)
    dialog_thread.start()
    dialog_thread.join()  # Wait for the thread to finish
    return q.get()
    


def thread_safe_folder_dialog(q):
    try:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        root.overrideredirect(True)
        folder = filedialog.askdirectory()
        root.destroy()
    except Exception as e:
        print(e)
        folder = ""
    q.put(folder)


async def run_folder_dialog() -> str:
    q = Queue()
    dialog_thread = threading.Thread(target=thread_safe_folder_dialog, args=(q,), daemon=True)
    dialog_thread.start()
    dialog_thread.join()  # Wait for the thread to finish
    return q.get()
    

def thread_safe_save_as_dialog(q, file_types):
    try:
        root = Tk()
        root.withdraw()  # Hide the Tkinter root window
        root.attributes("-topmost", True)  # Ensure the dialog is on top of other windows
        file_path = filedialog.asksaveasfilename(defaultextension=file_types[0][1], filetypes=file_types)
        root.destroy()
    except Exception as e:
        print(e)  # Optionally print the exception to stderr or handle it
        file_path = ""
    q.put(file_path)  # Use the queue to return the file path

async def run_save_as_dialog(file_types=[('All Files', '*.*')]) -> str:
    q = Queue()
    dialog_thread = threading.Thread(target=thread_safe_save_as_dialog, args=(q, file_types), daemon=True)
    dialog_thread.start()
    dialog_thread.join()  # Wait for the thread to finish
    return q.get()  # Retrieve the file path from the queue
