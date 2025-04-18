# CS 167 Project 1 Introduction
## Project Summary

This web application is a Flask-based user management system with basic CRUD functionality and city-based data lookup. Users can add their name and a city they want to visit, and the app stores this data in a database. It also includes features to update, delete, and display users, as well as a tool to find the country a city is located in.

Key features include:

* Add, display, update, and delete users (username + city)

* Store user data in AWS DynamoDB or SQL database

* Lookup a city and return the country it’s located in

## Technologies used

* Python with Flask (web framework)

* HTML (to create templates)

* MySQL/AWS DynamoDB (database for storing user/city info)

* boto3 (for DynamoDB interaction)

* Flask Flash (for user messages and notifications)

## Setup and run instructions

* Go to your web browser and search http://54.159.251.11:8080/

    * To add yourself the the database, click on 'Add User' from the home page and enter your username and city you would like to go to. 
 
        * You will then be directed to a web page to find out what country the city is in. Enter a city and hit 'Find Country'. 
 
    * To update the city you would like to go to, click on 'Update User' from the home page and enter your username and the new city.

    * To see all of your friends' cities they want to go to, click on 'Display all users' from the home page. You can now compare everyone's responses to determine where the crew should travel to next!
 
    * Finally, to delete yourself from the database, click on 'Delete User' from the home page and enter your username. 