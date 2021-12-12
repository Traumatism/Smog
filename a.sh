for _path in $(/usr/bin/find . -type d | /usr/bin/grep "__pycache__"); 
    do /bin/rm -rf $_path;
done;

git add .
git commit -a
git push
