#!/bin/bash
echo "Enter your password, a blank line and then CTRL+D"
argon2 amirvaultpass1 -id -t 1000 -m 22 -p 8 -l 16

