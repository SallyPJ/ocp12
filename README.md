# Epic Events CRM

## Project Overview
Epic Events CRM is a command-line application designed to manage customer relationships for event planning. 

## Features
- **Event Management** : Create, update, and delete events, assign support staff, and track participants.
- **Client Management** : Register, update, and manage client details, including contacts and enterprise info.
- **Contract Management** : Create, update, and track contracts linked to clients and events, including payment status.
- **Employee Management** : Manage employees and assign roles (Sales, Support, Management).
- **User Roles & Permissions** : Enforce access control with permissions for Sales, Support, and Management users.
- **Audit Logging** : Log user activities, including contract signatures, employee modifications, and system errors.
- **Database Persistence** : Uses **MySQL** with **SQLAlchemy ORM** for efficient data storage and retrieval.
- **Secure Authentication** : Uses **JWT** for token-based authentication and **Argon2** for password hashing.
- **CLI Interface** : Command-line based interactions with rich text formatting using **Click** and **Rich-Click**.

## Software
- **Python**: Main programming language.
- **SQLAlchemy**: ORM for database management and queries.
- **MySQL**: Relational database for data storage.
- **Sentry**: Logging, error tracking, and performance monitoring.
- **Click**: CLI framework for user interactions.
- **Rich & Rich-Click**: Enhanced CLI output formatting.
- **Pipenv**: Virtual environment and dependency management.
- **Keyring**: Secure storage for authentication tokens.
- **Passlib (Argon2)**: Secure password hashing.
- **JWT (PyJWT)**: Token-based authentication.

## Architecture
This project follows a **DAO** approach with a MCV model:

- **models/**: SQLAlchemy models defining database structures.
- **dao/**: Data Access Objects (DAO) for database interactions.
- **services/**: Business logic, validation, and permission management.
- **controllers/**: Handles application logic and user requests.
- **views/**: Manages the command-line interface (CLI) output formatting.
- **cli/**: CLI commands using `click` for user interaction.
- **decorators/**: Authentication and permission control decorators.
- **config/**: Configuration settings, including database and environment variables.
- **seeders/**: Scripts to populate the database with initial data.

## Installation
```sh
# Clone the repository
git clone https://github.com/SallyPJ/ocp12.git
cd ocp12

# Install Pipenv if necessary
pip install pipenv

# Create a virtual environment
pipenv install --dev

```
## Sentry Configuration
Sentry helps monitor and diagnose errors in your application.

1. Create an account on [Sentry](https://sentry.io/).
2. Create a new project and select Python as the platform.
3. Copy the DSN provided by Sentry.
## Environment Variables
Create a `.env` file in the root directory (ocp12) with the following content:
```ini
#Create secured secret keys for JWT authentication
JWT_SECRET=<your_secret_key_here>
JWT_REFRESH_SECRET=<your_refresh_secret_key_here>
# Update with your credentials 
DATABASE_URL=mysql+pymysql://username:password@localhost/epic_events_crm_dev
# Update with you sentry DSN 
SENTRY_DSN=<your_sentry_dsn_here>
```

## Database Setup

### Install MySQL SGBD and create a root user (if necessary)

### Create the MySQL Database
Connnect to MySQL (if necessary, add Mysql in your environment path)
```sh
mysql -u root -p
```
Then, in the MySQL shell:
```sql
CREATE DATABASE epic_events_crm_dev;
```
Then 
```sql
EXIT;
```

### Initialize and seed the Database
In the ocp12 folder, activate the virtual environment :
```sh
pipenv shell
```
Run the following command to create and seed tables with permissions 
and test employees, customers, contracts and events:
```sh
python -m crm.seeders.seed_all
```
## Running the Application
Go to the crm folder : 
```sh
cd crm
```
Launch the application :
```sh
python main.py
```

## User Roles
- **Sales**: Can manage clients and contracts.
- **Support**: Can access and update event details.
- **Management**: Can manage employees, create and edit contracts, can edit events.
- **Admin**: Full access 

## Test data and permissions constants location

Permissions : crm/services/constants.py  
Tests data : crm/seeders/seed_data

##  Main Command List
| Command                              | Description                           |
|--------------------------------------|---------------------------------------|
| `python main.py customer list`       | Show all customers                    |
| `python main.py customer get <id>`   | Show details of a specific customer   |
| `python main.py customer create`     | Register a new client                 |
| `python main.py customer update <id>` | Modify client details                 |
| `python main.py event list`          | Display all events (options)          |
| `python main.py event get <id>`      | Show details of a specific event      |
| `python main.py event create`        | Add a new event                       |
| `python main.py event update <id>`   | Modify an event                       |
| `python main.py contract list`       | Display all contracts (options)       |
| `python main.py contract get <id>`   | Show details of a specific contract   |
| `python main.py contract create`     | Create a new contract                 |
| `python main.py contract update <id>` | Modify contract details               |
| `python main.py user list`           | Show all employees                    |
| `python main.py user get <id>`       | Show details of a specific employee   |
| `python main.py user create`         | Register a new employee               |
| `python main.py user update <id>`    | Modify an employee's details          |
| `python main.py user deactivate <id>` | Deactivate an employee account        |
| `python main.py auth login`          | Authenticate and store session tokens |
| `python main.py auth logout`         | Logout and remove stored session      |


## Entity-Relationship Diagram (ERD)
![img_1.png](ER_Diagram.png)


## Logging & Debugging (Sentry)
Errors and application logs are tracked using **Sentry**. Ensure your **SENTRY_DSN** is correctly configured in the `.env` file to receive logs in the Sentry dashboard.



