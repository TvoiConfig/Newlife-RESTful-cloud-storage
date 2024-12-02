# Newlife-REST - Cloud Storage with File Access Management

**Project Description:**
Newlife-Without-SimpleJWT is a RESTful cloud storage API that allows users to upload, edit, delete, and manage access permissions to their files. The project is designed to provide secure file storage with granular access control features, ensuring that only authorized users can manage and share files. This project does not use SimpleJWT for authentication, instead leveraging Django’s built-in `TokenAuthentication` for secure user access. This project created for championship World Skills Russia.

---
## Features

### For Unauthorized Users:
- **Registration:** Create a new account with an email, first name, last name, and a valid password.
- **Authorization:** Log in using email and password to get a token for authenticated access.

### For Authorized Users:
- **Logout:** Securely log out by invalidating the token.
- **File Management:**
  - **Upload files** to the cloud storage.
  - **Edit file details** such as file name.
  - **Delete files** permanently.
  - **Access control:** Grant or revoke file access to other users with specific permissions (e.g., author, co-author).

## Technology Stack
- **Backend:** Django 5.x / Django REST Framework (DRF)
- **Authentication:** Token-based authentication (via `django-rest-framework.authtoken`)
- **Database:** MySQL
- **Storage:** Local file storage

## Project structure
- **database** - contain models and register them in admin-panel
- **files** - contain FileUpload and FileEmploy(Edit, Delete, Download) functions of API
- **newlife** - contain django configuration
- **set_files_access** - contain files accesses(Add permission, Delete permission, View user files, View shared files) functions of API
- **users** - contain authorization, registration and logout users functions of API

## Installation

### Prerequisites
- Python 3.x
- Django 5.x
- Django REST Framework

### Steps to Install and Run the Project on Windows

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Newlife-Without-SimpleJWT.git
   
2. **Install requirements.txt**
    ```bash
   pip install -r requirements.txt
   
3. **Edit database settings**
    ```
    go to newlife/newlufe/settings.py
    edit DATABASES parameter (set db server or use SQLite)
    ```
4. **Open newlife**
    ```bash
    cd ./newlife/

5. **Makemigrations**

    **For Windows**
    ```bash
    python manage.py makemigrations
    ```
   **For linux**
    ```bash
   python3 manage.py makemigrations
6. **Migrate**

    **For windows**
    ```bash
   python manage.py migrate
    ```
    **For linux**
    ```bash 
   python3 manage.py migrate
7. **Run**
    
    **For windows**
    ```bash
   python manage.py runserver
    ```
   **For linux**
    ```bash
   python3 manage.py runserver

## Endpoints for Testing

Below are the available API endpoints for testing the functionality of the **Newlife-REST** project. Use tools like **Postman** or **curl** to interact with the API.

---
### Users
#### **Authentication**
- **Endpoint:** `POST /authorization/`
- **Description:** Login user into account.
- **Headers**
    ```headers
    Content-Type: application/json
- **Request Body:**
    ```json
  {
    "email": "user@example.com",
    "password": "E1x",
  }
  
#### **Register a New User**
- **Endpoint:** `POST /registration/`
- **Description:** Creates a new user account.
- **Headers**
    ```headers
    Content-Type: application/json
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "E1x",
    "first_name": "John",
    "last_name": "Doe"
  }

#### **Logout**
- **Endpoint:** `GET /logout/`
- **Description:** Logout user from account.
- **Headers**
    ```headers
    Authorization: token <past your token here>

### Files
#### **Post files**
- **Endpoint:** `POST /files/`
- **Headers**
    ```headers
    Content-Type: multipart/form-data
    Authorization: token <past your token here>
- **FormData:**
  ```FormData
  files[]: <your files array here>
  
#### **Edit file**
- **Endpoint:** `PATCH /files/<your file id here>/`
- **Description:** Rename file_name.
- **Headers**
    ```headers
    Content-Type: application/json
    Authorization: token <past your token here>
- **Request Body:**
  ```json
  {
    "name": "new Name"
  }

#### **Delete file**
- **Endpoint:** `DELETE /files/<your file id here>/`
- **Description:** Delete file.
- **Headers**
    ```headers
    Content-Type: application/json
    Authorization: token <past your token here>

#### **Download file**
- **Endpoint:** `GET /files/<your file id here>/`
- **Description:** Download file.
- **Headers**
    ```headers
    Authorization: token <past your token here>

#### **Add file accesses**
- **Endpoint:** `POST /files/<your file id here>/accesses/`
- **Description:** Add access to file.
- **Headers**
    ```headers
    Content-Type: application/json
    Authorization: token <past your token here>
- **Request Body:**
  ```json
  {
    "email": "user@user.ru"
  }

#### **Delete file accesses**
- **Endpoint:** `DELETE /files/<your file id here>/accesses/`
- **Description:** Delete access to file.
- **Headers**
    ```headers
    Content-Type: application/json
    Authorization: token <past your token here>
- **Request Body:**
  ```json
  {
    "email": "user@user.ru"
  }

#### **View user files**
- **Endpoint:** `GET /files/disk/`
- **Description:** Return user files.
- **Headers**
    ```headers
    Content-Type: application/json
    Authorization: token <past your token here>

#### **View shared files**
- **Endpoint:** `GET  /shared/`
- **Description:** Return shared files for user.
- **Headers**
    ```headers
    Content-Type: application/json
    Authorization: token <past your token here>
