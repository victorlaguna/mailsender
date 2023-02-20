## importing neccesary libraries
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import logging
import MySQLdb
import mysql.connector as msql
from mysql.connector import Error
import csv
from os import system, name
import time
import traceback
import ssl

# define our clear function
def clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# basic configuration for application logs
logging.basicConfig(filename='mailsender.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# Verify and connect to the database
def connectdb(host,user,password):
    logging.info('DB connection init')
    # example conn = msql.connect(host='192.168.1.3', user='root', password='Vick-2016')
    conn = msql.connect(host=host, user=user, password=password)
    try:
        conn
    except MySQLdb.connector.Error as error:
            logging.warning('DB no connected, please verify inputs')
            print("cannot connect to the DB")
            logging.error('DB no connected')
            return(print('DB no connected'))
    else:
        logging.info('DB connected success')
        print('\nDB connected success')
        response = conn.is_connected()
        return response

# Funtion to send email one by one
def sendmail(asunto,destinatario,destino,password,email_smtp):
    logging.info('Email send init')
    # Create an email message object
    message = EmailMessage()
    email_subject = asunto 
    sender_email_address = destinatario 
    receiver_email_address = destino 
    # Configure email headers 
    message['Subject'] = email_subject 
    message['From'] = sender_email_address 
    message['To'] = receiver_email_address
    with open('c:/Users/vj900/Desktop/Proyectos programacion/mailsender/python-bulk-mail-master/mail.html', 'r', encoding="utf8") as file:
        data = file.read().replace('\n', '')
    html = data.format()
    message.attach(MIMEText(html, "html"))
    message.set_content(html, subtype='html')
    # Set smtp server and port 
    server = smtplib.SMTP(email_smtp, '587') 
    # Identify this client to the SMTP server 
    server.ehlo() 
    # Secure the SMTP connection 
    server.starttls() 
    # Login to email account 
    server.login(sender_email_address, password) 
    # Send email 
    response = server.send_message(message) 
    # Close connection to server 
    server.quit()
    logging.info('Email sent end')
    return(response)

# Funtion to put into the mysql database all the mail from a csv list
def load_mail_list(host,user,password,file_path):
    # example conn = msql.connect(host='192.168.1.3', user='root', password='Vick-2016')
    #conn = msql.connect(host, user, password)
    conn = msql.connect(host=host, user=user, password=password)
    try:
        conn
    except NameError:
        logging.error('DB no connected')
        print('DB no connected')
    else:
        logging.info('DB connection init')
        logging.info('DB connected success')
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS mailsender")
        conn.database = 'mailsender'
        cursor.execute('CREATE TABLE IF NOT EXISTS `mail_list` (`id` INT(12) NOT NULL AUTO_INCREMENT, `nombre` VARCHAR(50), `mail` VARCHAR(50), `accountid` INT(12),`historyid` INT(12),`created` DATE, PRIMARY KEY (id))')
        #get_list_fromdb = list(cursor.execute("SELECT * FROM `mailsender`.`mail_list`;"))
        my_file = Path(file_path)
        if my_file.is_dir() and my_file.is_file():
            with open(file_path, newline='') as f:
                reader = csv.reader(f)
            read_list_frompath = list(reader)
            account_list = [fila[2] for fila in read_list_frompath]    
            mails_list = [fila[1] for fila in read_list_frompath]
            name_list = [fila[0] for fila in read_list_frompath]
            cursor.execute('INSERT INTO mail_list (nombre,mail,accountid) VALUES (?);', [','.join(name_list)], [','.join(mails_list.title())], [','.join(account_list)])
            cursor.execute('INSERT INTO mail_list (name) VALUES (?);', [','.join(name_list.title())])
            cursor.execute('INSERT INTO mail_list (urls) VALUES (?);', [','.join(account_list)])
            cursor.commit()
            print(cursor.rowcount, "Record inserted successfully into Laptop table")
            logging.info('Record inserted successfully into Laptop table')
            conn.close()
        else:
            print("\nFile not exists")
            logging.info('File not exists')
   
# ejecucion principal
if __name__ == '__main__':
    clear()
    print("\nWelcome to the mailsender menu, please select the requeriment:")
    ans=True
    response=False
    while ans:
        print ("""
        1.Connect with Database connection
        2.Verify DB connection
        3.Upload to database the CSV mail list
        4.Configure path for mail html template
        5.Send all the pending mail for this account
        6.Exit/Quit
        """)
        ans=str(input("What would you like to do? ")) 
        if ans=="1": 
            print("\n Please set this ")
            host = str(input ("  please input the host for the mysql database: "))
            user = str(input ("  please input the user for the mysql database: "))
            password = str(input ("  please input the password for the mysql database: "))
            #print(host, user, password)
            response = connectdb(host,user,password)
        elif ans=="2":
            #print(response)
            if response == True:
                logging.info('DB connected success')
                print("\nConnection to DB connected success")
            else:
                logging.error('DB no connected')
                print('\nDB no connected')
        elif ans=="3":
            if response == True:
                #print(host,user,password,response)
                file_path = str(input ("please input the path csv list on the host: "))
                print(file_path)
                load_mail_list(host,user,password,file_path)
            else:
                print('\nDB no connected, please select the option 1 and do the connection')
        elif ans=="4":
            print("\nClosing DB connection")
            if response == True:
                conn.close()
            else:
                print("DB not connected is not necessary close")
        elif ans=="5":
            print("\n Student Record Found") 
        elif ans=="6":
            print("\n Goodbye")
            exit() 
        elif ans !="":
            print("\n Not Valid Choice Try again")