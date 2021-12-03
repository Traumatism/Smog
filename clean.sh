for path in `/usr/bin/find . -type d | /usr/bin/grep "__pycache__"`; do /bin/rm -rf $path; done;
