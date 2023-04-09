# Mailtome
Mailtome is a simple website based on Django. It solves the problem of needing to save work while working remotely. One solution is to log in with Gmail and save the work on Google Drive, but trusting someone else with your Google account is not ideal. Another solution is to email the work to yourself as an attachment, but this also requires signing in to Gmail. To solve this problem, Mailtome offers a service where you can send an email with attachments to yourself without having to sign in to your Gmail account. This works on small size files.
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
## Prerequisites
To run this project, you need to have installed the following:

* Python 3.8 or above
* Django 3.2 or above
* Pip 20.0 or above
* Docker
## Installing
### Creating virtual environment
* Clone this repository on your local machine.
* Create a virtual environment with Python 3.8 or above.
```python
python3 -m venv env
source env/bin/activate
```

* Install the required dependencies
* Run the server

### Using Docker
[Docker Image Link] (docker push chinmay1718/mailtome-server:1)

Run the container from the image.
## Usage
Regiser as a new user.
Log in with your credentials.
Send email with attachments to yourself without signing in to your Gmail account.
Logout when you're done.
## Built With
Django - The web framework used
Bootstrap - The CSS framework used
