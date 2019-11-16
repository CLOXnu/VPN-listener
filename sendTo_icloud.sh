#!/bin/bash

echo "mail sending...";
echo "$2" > /root/Documents/mail/mailCc.txt;
mail -s "$1" cloxnu@icloud.com < "/root/Documents/mail/mailCc.txt";
#php phpmail.php cloxnu@icloud.com $1 "$2"

echo "mail sent."
