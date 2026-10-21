#### NC Plus One

This is a my first Northcoders project where I am building a REST API for an events platform. This will allow users register, browse events, RSVP and manage attendance. Organisers will be able to create and manage events and view statistics about their users.

This is only a backend project but I will be taking frontend into consideration when building. This is the data layer of a full stack application and will affect how a frontend dev interacts with it later on.

### Database Setup
To create a new nc_plus_one database and clear any existing info in the table run the command psql -U username -d postgres -f db/setup.sql in the terminal to DROP DATABASE and CREATE DATABASE.

### Database Conection
To connect to the database using the connection.py file you will first need to copy the .env.example file and create your own .env with local database credentials.