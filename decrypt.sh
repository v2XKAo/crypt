#!/bin/bash
if [ "$#" -lt 1 ]; then
    echo "Illegal number of parameters. Usage: decrypt.sh SOURCE_FILE_NAME"
	exit 1
fi

SOURCE_FILE="$1"
DEST_FILE=$(echo "$SOURCE_FILE" | sed 's/.enc//g')

openssl enc -d -aes-256-cbc -md sha512 -pbkdf2 -a -in "$SOURCE_FILE" -out "$DEST_FILE"

echo "DONE"

