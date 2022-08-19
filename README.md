# Rclone passwords sync

[![GitHub stars](https://img.shields.io/github/stars/LockBlock-dev/rclone-passwords-sync.svg)](https://github.com/LockBlock-dev/rclone-passwords-sync/stargazers)

A simple passwords file synchronizer using [Rclone](https://rclone.org/)

## How to use

• Download the project or clone it

• Edit the top of the file:

```python
DRIVE = ""
DB_FILE_NAME = "Passwords.kdbx"
LOCAL_FOLDER = ""
REMOTE_FOLDER = ""
```

• Run the python script in a command prompt :

```bash
python3 sync.py
```

## Credits

[Original bash version](https://gist.github.com/ZviBaratz/a4a51544c3d876543d37abfd0c6ee2a3#file-sync-passwords-sh).

## Copyright

See the [license](/LICENSE).
