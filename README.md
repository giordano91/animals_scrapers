# charlie_feeder

## Introduction
Aim of this project is to collect data from some external platforms to feed Charlie web application.  
At the moment the idea is to implement three scrapers; one for `subito.it`, one for `pet24` and one for `annunci_animali`.  
Each scraper is responsible for taking data from the site and saving all the information in a MySQL table.  
Charlie will fetch data from a materialized view, which will be populated via a store procedure.  

Scrapers (and the MySQL database) have been implemented to run as a docker service.  

## How to run the project
To start the project, the only prerequisite is to have `Docker` installed on the machine.  

Once the project has been cloned, it will be necessary to create and compile some configuration files.  
The project provides sample files as the information to be compiled is sensitive.  
To do this, you need to duplicate each `.env_<service_name>.sample` file in the `env_files` folder.  
Now you need to remove the `.sample` from the copied file and fill in the required information.

### mysql env file
At the time of writing this file there are only three variables to compile.  
Here is a list with their meanings:  
- MYSQL_USER: a user with this name will be created at the start-up of the project
- MYSQL_PASSWORD: this is the password for the user created (see MYSQL_USER)
- MYSQL_ROOT_PASSWORD: this is the root password

*IMPORTANT*
Please insert data without double/single quotes.  
Example: MYSQL_PASSWORD=mypassword

---

When all configuration files have been compiled, you can start the project with the following docker commands 
(from the project root):

```commandline
docker-compose build
docker-compose up
```
