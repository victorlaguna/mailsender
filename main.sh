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

##menu principal
echo -n "\nMENU envio de mensajes masivos"
    echo "\n1. Cargar archivo de base de datos de correos(solo mail)"
    echo "2. Cargar archivo de base de datos de correos(nombre y mail)"
    echo "3. Ver base cargada y tipo de base"
    echo "4. Ver estado de envios"
    echo "5. Programar envios de correos"
    echo "6. Ver programacion actual de los envios"
    echo "7. SALIR"
    read -p "Ingresa una opcion: " opcion
    case $opcion in
        1)
            clear
            echo -n "\nIngresa la ruta absoluta del archivo con los correos:"
            read only_mail_absolute_route
            echo -n "\nLa ruta cargada es $only_mail_absolute_route:"
            read -p "Es correcto?(S/N): " confirm_answer
            if [ "$confirm_answer" = "s" ] || [ "$confirm_answer" = "S" ]; then
                echo $only_mail_absolute_route > only_mail_absolute_route.txt
            else
                clear
                echo "Por favor ingrese al menu nuevamente"
                sh main.sh
            fi
            ;;
        2)
            clear
            echo -n "\nIngrese"
            echo -n "\n"
            read -p "INICIO(AAAAMMDD): " start_date
            read -p "FIN(AAAAMMDD): " end_date
            echo "se modifico el archivo de la siguiente manera"
            echo $start_date $end_date
            echo $start_date $end_date > daterange.txt
            sh main.sh
            ;;
        3)
            clear
            cat mail.txt
            echo "\n"
            sh main.sh
            ;;
        4)
            clear
            echo -n "\nIngrese"
            echo -n "\n"
            read -p "CORREO: " mail
            echo "se modifico el archivo de la siguiente manera"
            echo $mail
            echo $mail > mail.txt
            sh main.sh
            ;;
        5)
            clear
            echo "se ejecutara el script"
            sh get_files.sh
            ;;

        6)
            clear
            echo "se construira el script a partir de los archivos"
            echo "\n"
            sh construct.sh
            ;;
        7)
            clear
            exit 1
            ;;
        *)
            clear
            echo "OPCION INVALIDA"
            sh main.sh
        esac


##al final se suma uno para echo $((++start))
start=$((1+start))
echo $start > start.txt