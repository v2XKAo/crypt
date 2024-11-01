#!/bin/bash
if [ "$#" -lt 1 ]; then
    echo "Illegal number of parameters. Usage: encrypt.sh SOURCE_FILE_NAME"
	exit 1
fi

SOURCE_FILE="$1"
DEST_FILE="$1.enc"

openssl enc -aes-256-cbc -md sha512 -pbkdf2 -a -salt -in "$SOURCE_FILE" -out "$DEST_FILE"

echo "DONE"
echo "Don't forget to remove $SOURCE_FILE for security purposes"
