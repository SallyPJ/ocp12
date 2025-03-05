# Epic Events CRM

## Project Overview
Epic Events CRM is a command-line application designed to manage customer relationships for event planning. The application follows the **MVC pattern with a DAO-only structure**. It is built using **Python and SQLAlchemy**, with department-based access control for different types of users.

## Features
- **Event Management**: Create, update, and delete events.
- **Client Management**: Register and modify client information.
- **Contract Management**: Track contracts associated with events.
- **User Roles & Permissions**: Different access levels for users (e.g., Sales, Support, Management).
- **Audit Logging**: Logs interactions for security and debugging.
- **Database Persistence**: Uses **MySQL** for data storage.

## Software Used
- **Python**: Main programming language.
- **SQLAlchemy**: ORM for database management.
- **MySQL**: Database storage.
- **Sentry**: Logging and error tracking.
- **Typer**: CLI framework.
- **Pipenv**: Virtual environment and dependency management.

## Architecture
This project follows the **DAO-only** approach:
- **models/**: SQLAlchemy models.
- **dao/**: Database access objects.
- **services/**: Business logic and permission handling.
- **controllers/**: Application logic.
- **views/**: Command-line interface.

## Entity-Relationship Diagram (ERD)
![img_1.png](img_1.png)

## Installation
```sh
# Clone the repository
git clone https://github.com/SallyPJ/ocp12.git
cd epic_events_crm

# Install Pipenv
pip install pipenv

# Create and activate a virtual environment
pipenv install --dev
pipenv shell
```

## Environment Variables
Create a `.env` file in the root directory with the following content:
```ini
DATABASE_URL=mysql+pymysql://username:password@localhost/epic_events  # Update with your credentials
SENTRY_DSN=<your_sentry_dsn_here>
```

## Database Setup
### Create the MySQL Database
```sh
mysql -u root -p
```
Then, in the MySQL shell:
```sql
CREATE DATABASE epic_events;
CREATE USER 'epic_user'@'localhost' IDENTIFIED BY 'securepassword';
GRANT ALL PRIVILEGES ON epic_events.* TO 'epic_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Initialize the Database
Run the following command to create tables:
```sh
python setup_database.py
```

### Seed the Database with Initial Data
To populate the database with initial test data:
```sh
python seed_database.py
```

## Running the Application
```sh
python main.py
```

## User Roles
- **Sales**: Can manage clients and contracts.
- **Support**: Can access and update event details.
- **Management**: Full access to all resources.

## Command List
| Command                          | Description |
|----------------------------------|-------------|
| `python main.py create-client`  | Register a new client |
| `python main.py update-client`  | Modify client details |
| `python main.py create-event`   | Add a new event |
| `python main.py update-event`   | Modify an event |
| `python main.py create-contract`| Create a new contract |
| `python main.py update-contract`| Modify contract details |
| `python main.py list-events`    | Display all events |
| `python main.py list-clients`   | Display all clients |
| `python main.py list-contracts` | Display all contracts |

## Running Tests
```sh
pytest tests/
```

## Logging & Debugging (Sentry)
Errors and application logs are tracked using **Sentry**. Ensure your **SENTRY_DSN** is correctly configured in the `.env` file to receive logs in the Sentry dashboard.

## License
This project is licensed under the MIT License.

## Contact
For further inquiries, please contact **SallyPJ** at [GitHub](https://github.com/SallyPJ).

