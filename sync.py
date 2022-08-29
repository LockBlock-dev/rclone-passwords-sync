#!/bin/env python


# Important note:
# If you don't synchronize but then edit the other file,
# the newer modification time on the second file edited
# will cause data to be overridden.
# The solution would be to merge manually
# (Database --> Merge from database).

from os import path, system
from subprocess import check_output
from re import search
from datetime import datetime


DRIVE = ""
DB_FILE_NAME = "Passwords.kdbx"
LOCAL_FOLDER = ""
REMOTE_FOLDER = ""

# Compose full path to local and remote database files
LOCAL_PATH = path.join(LOCAL_FOLDER, DB_FILE_NAME)
REMOTE_PATH = path.join(REMOTE_FOLDER, DB_FILE_NAME)
# Compose import and export commands
EXPORT_CMD = f"rclone copy {LOCAL_PATH} {DRIVE}:{REMOTE_FOLDER}"
IMPORT_CMD = f"rclone copy {DRIVE}:{REMOTE_PATH} {LOCAL_FOLDER}"


# Get local passwords file modification time
def local_modification_time():
    try:
        return path.getmtime(LOCAL_PATH)
    except Exception as e:
        print(f"ERROR! Local mtime set to -1! {e}")
        return -1


# Parse remote passwords file modification time using Rclone's lsl command
# See: https://rclone.org/commands/rclone_lsl/
def remote_modification_time():
    try:
        res = (
            check_output(["rclone", "lsl", f"{DRIVE}:{REMOTE_FOLDER}"])
            .decode("utf-8")
            .split("\n")
        )
        res = list(filter(lambda file: search(DB_FILE_NAME, file), res))

        date = search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6}", res[0]).group(0)
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")

        return datetime.timestamp(date)
    except Exception as e:
        print(f"ERROR! Remote mtime set to -1! {e}")
        return -1


def sync_passwords():
    local_mtime = int(local_modification_time())
    remote_mtime = int(remote_modification_time())

    if remote_mtime == -1:
        print("No remote passwords database found!")
        print("Exporting...")
        system(EXPORT_CMD)
        print("Done: Local => Remote")

        return
    elif local_mtime == -1:
        print("No local passwords database found!")
        print("Importing...")
        system(IMPORT_CMD)
        print("Done: Remote => Local")

        return

    print("Local modification time:", datetime.fromtimestamp(local_mtime))
    print("Remote modification time:", datetime.fromtimestamp(remote_mtime))

    if local_mtime > remote_mtime:
        print("\nLocal passwords file found to be newer than remote!")
        print("Exporting...")
        system(EXPORT_CMD)
        print("Done: Local => Remote")
    elif local_mtime < remote_mtime:
        print("\nLocal passwords file found to be older than remote!")
        print("Importing...")
        system(IMPORT_CMD)
        print("Done: Remote => Local")
    else:
        print("\nPassword files are already synchronized.")


sync_passwords()
