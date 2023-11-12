from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB="mydb"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @staticmethod
    def validate_user(user):
        is_valid = True
        if user["first_name"] == "" or user["last_name"] == "" or user["email"] == "" or user["password"] == "" or user["pass_confirm"] =="":
            flash("All fields required.")
            is_valid = False
        elif len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        elif len(user['last_name']) < 2:
            flash("Last name be at least 2 characters.")
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        elif len(user["password"]) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        elif user["pass_confirm"] != user["password"]:
            flash("Password and confirm password must match.")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data ):
        query = """INSERT INTO users (first_name,last_name,email,password) 
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result

    @staticmethod
    def validate_login(user):
        is_valid = True
        if user["first_name"] == "" or user["last_name"] == "" or user["email"] == "" or user["password"] == "":
            flash("All fields required.")
            is_valid = False
        elif len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        elif len(user['last_name']) < 2:
            flash("Last name be at least 2 characters.")
            is_valid = False
        elif user["password"] < 8:
            flash("Password incorrect.")
            is_valid = False
        return is_valid

    @classmethod
    def get_one(cls, data):
        query  = """SELECT * FROM users WHERE id = %(id)s"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * from users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:    #This means that if the query gets run through the DB and no email come back matching the one that was entered, login will not be allowed.
            return False
        return cls(results[0])