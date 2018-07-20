[![Build Status](https://travis-ci.org/koechkevin/myDiary.svg?branch=challenge2)](https://travis-ci.org/koechkevin/myDiary)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Maintainability](https://api.codeclimate.com/v1/badges/184b7b2cf89a0111c784/maintainability)](https://codeclimate.com/github/koechkevin/myDiary/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/koechkevin/myDiary/badge.svg?branch=challenge2)](https://coveralls.io/github/koechkevin/myDiary?branch=master)
# myDiary
myDiary is a set of API endpoints that uses data structures to store data in memory.<br/>
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/2e72df446f43c421121f) 

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