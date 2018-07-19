[![Build Status](https://travis-ci.org/koechkevin/myDiary.svg?branch=master)](https://travis-ci.org/koechkevin/myDiary)
# myDiary
myDiary is a set of API endpoints that uses data structures to store data in memory 

### Set up the environment
This platform APIs is built on flask python framework. You must have python installed preferably version 3

Clone the repository
```sh
https://github.com/koechkevin/myDiary.git
```

Create a virtual environment on the directory that the cloned repository resides in

I used this command to create a virtual environment

```sh
py -3 -m venv venv
```
Activate the virtual environment
```sh
venv\Scripts\activate
```
```sh
pip install flask
```
Install requirements.txt file

```sh
pip install requirements
```
### Run the application

```sh
python myDiary_dataStructures.py
```
### APIs Endpoints

**`GET "/api/v1"`** *home page*

**`POST /api/v1/register`**    *Register user. Takes in a json object with keys as fname,lname,username,password,cpassword,email*

**`POST  /api/v1/login`**  *Login. Takes in a json object with keys as username and password*

**`POST /api/v1/create_entry`** *Post Entry. takes in a json object with key as comment provided you are logged in*

**`GET  /api/v1/entries`** *Get all entries made by user on session*

**`GET /api/v1/view_entry/<int:entryID>`** *Get an Entry with corresponding entryID*

**`PUT /api/v1/modify_entry/<int:entryId>`** *Update an Entry takes in jsonified dict with comment as key*

**`DELETE /api/v1/delete_entry/<int:entryId>`** *Delete an Entry of corresponding ID*

**`GET /api/v1/account`** *Get account details of user on session*

**`GET /api/v1/logout`** *Gets user on session out of session*