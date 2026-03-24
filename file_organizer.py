import os
import shutil
log_file = open("move_log.txt", "a")

folder = folder = os.path.join(os.path.expanduser("~"), "Downloads")

files = os.listdir(folder)

for file in files:
    if not os.path.isfile(folder + "/" + file):
     continue

    if file.endswith(".jpg") or file.endswith(".png"):
        destination = folder + "/Images"

    elif file.endswith(".pdf") or file.endswith(".txt"):
        destination = folder + "/Documents"

    elif file.endswith(".mp3"):
        destination = folder + "/Music"

    elif file.endswith(".mp4") or file.endswith(".mov"):
        destination = folder + "/Videos"

    elif file.endswith(".zip"):
        destination = folder + "/Compressed files"
        
    elif file.endswith(".py"):
        destination = folder + "/programming python files"         

    else:
        continue

    os.makedirs(destination, exist_ok=True)
    source = folder + "/" + file
    destination_file = destination + "/" + file

    shutil.move(source, destination_file)

    log_file.write(source + "|" + destination_file + "\n")

    shutil.move(folder + "/" + file, destination + "/" + file)

log_file.close()

print("Files organized!")