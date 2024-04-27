# NewsQuest 
## A Django MVT Pattern Newspaper Web Application.
### Website Live: https://newsquest.onrender.com
#### Admin Credential : 
- Username: sara
- Password: 123

#### Editor Credential : 
- Username: sabrina
- Password: 111111$S

### Features-
- User registration and login using email.
- With User, EditorPanel.
- User can give rating.
- Editor can add news.
- Editor can edit and delete news(article).
- Admin can manage Users and Editor.
- Admin can approve, deny, or make news premium.
- Admin can make users, admin also editors.

### Resources & Credits


### Getting Started
To run NewsQuest locally, follow these steps:
- Clone the repository to your local machine.
- Install dependencies
- setup env file
```bash
  SECRET_KEY=use your own secret key from settings.py
  EMAIL=your email
  EMAIL_PASS=set password as you want
```
- Start the server
 ```bash
    py manage.py runserver
```
- setup requirement.txt
```bash
  pip install -r requirements. txt
```
- For migrations 
```bash
  py manage.py makemigrations
```
```bash
  py manage.py migrate
```
   
