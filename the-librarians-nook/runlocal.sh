#!/bin/sh

npm run build
sudo docker build -f Dockerfile_local . -t the_librarians_nook
sudo docker run -p 8080:8080 the_librarians_nook
