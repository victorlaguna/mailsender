#!/bin/bash

## se verifica si existe un archivo de start para continuar
if [ -f ./start.txt ]
then
    echo "exists on your filesystem the start file"
    start=$(cat start.txt)
else
    echo "no existe el archivo"
    echo 1 > start.txt
    start=$(cat start.txt)
fi

##Se sustituye la variable en el archivo mail.py
#sed s/\{\{TIME\}\}/$start/g ./python-bulk-mail-master/mail_template.py > ./python-bulk-mail-master/mail.py
##Se copia y 
cp ./bases/output/date_$start.csv ./python-bulk-mail-master/mail_beta.csv
sed -i '1s/^/cvx\.vlaguna\@gmail\.com\n/' ./python-bulk-mail-master/mail_beta.csv
sed -i s/^/,/g ./python-bulk-mail-master/mail_beta.csv
sed -i s/$/,/g ./python-bulk-mail-master/mail_beta.csv
sed -i '1s/^/Name\,Email\,URL\n/' ./python-bulk-mail-master/mail_beta.csv

#se dispara el script en python que envia los correos
python3 ./python-bulk-mail-master/mail.py
#cat ./python-bulk-mail-master/mail_beta.csv|head
##al final se suma uno para echo $((++start))
start=$((1+start))
echo $start > start.txt