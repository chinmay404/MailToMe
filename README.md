# MailToMe

Mailtome is a simple website based on Django. It solves the problem of needing to save work while working remotely. One solution is to log in with Gmail and save the work on Google Drive, but trusting someone else with your Google account is not ideal. Another solution is to email the work to yourself as an attachment, but this also requires signing in to Gmail. To solve this problem, Mailtome offers a service where you can send an email with attachments to yourself without having to sign in to your Gmail account.This will works on small size of files.



Server Overview
The server is a Python script that listens for incoming connections and processes incoming email data. It utilizes the socket library to listen for connections and the smtplib library to send the email. The email data is stored in an SQLite database.

Dependencies
The following Python libraries are used in this server script:

socket: For creating a socket and listening for incoming connections
sqlite3: For managing the SQLite database
ssl: For creating a secure connection with the SMTP server
threading: For handling multiple incoming connections simultaneously
smtplib: For sending emails through the SMTP server
pickle: For serializing/deserializing data for sending over the socket
os: For interacting with the operating system and environment variables
email.message: For creating the email message object
email.mime.text: For creating the email message body
email.mime.multipart: For creating email messages with attachments
email.mime.application: For attaching files to email messages
Database
The SQLite database is used to store the email data. The email table has the following columns:

id: Primary key for the table, automatically generated
subject: The subject of the email
body: The body of the email
recipient: The email address of the recipient
attachment_name: The name of any attachments
The database is created if it doesn't already exist and is connected to in a try block to handle any errors that may occur.

SMTP Server
The server logs in to the SMTP server using the provided email address and password. This login is done using SSL encryption to secure the connection.

Sending Emails
When a connection is established with the server, the server reads the incoming data from the socket, deserializes it using pickle, and extracts the subject, body, recipient, and attachment data (if any). The email message is then created using the email.message library, with the specified subject, body, and recipient. If an attachment is present, it is added to the email message using the email.mime.application library. The email message is then sent to the recipient using the SMTP server.

After the email is sent, the email data is added to the database using an INSERT statement.

Handling Multiple Connections
The server is designed to handle multiple connections simultaneously using threading. When a connection is accepted, a new thread is created to handle that connection. The thread runs the handle_client function, which receives the incoming email data and sends the email. Once the email is sent, the connection is closed and the thread is terminated.

Docker Container
