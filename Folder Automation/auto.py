from watchdog.observers import Observer
import time
from watchdog.events import FileSystemEventHandler
import os
import json
import fnmatch
import shutil

def gen_find(filepat,top):
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist,filepat):
            yield os.path.join(path,name)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        
        htmlFileName = "test.html"
        
        time.sleep(20)
        # Move css files in the main folder
        filesToMove = gen_find("*css", folder_to_track)
        for name in filesToMove:
            shutil.move(name, folder_to_track)

        time.sleep(3)
        # Get the html file name
        for filename in os.listdir(folder_to_track):
            if filename.endswith(".html"):
                htmlFileName = filename

        time.sleep(3)  
        # Move the html and css files in the destination folder     
        for filename in os.listdir(folder_to_track):
            
            if filename.endswith(".html"):
                src = folder_to_track + "/" + filename
                new_destination = folder_destination + "/" + filename
                os.rename(src, new_destination)

            if filename.endswith(".css"):
                new_name = os.path.splitext(htmlFileName)[0] + ".css"
                src = folder_to_track + "/" + filename
                new_destination = folder_destination + "/" + new_name
                os.rename(src, new_destination)
        
        time.sleep(3)
        # Remove the remaining files from the initial folder
        for filename in os.listdir(folder_to_track):
            file_path = os.path.join(folder_to_track, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

folder_to_track = 'F:/Desktop/Indesign Output'
folder_destination = 'F:/Desktop/Final Output'
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()