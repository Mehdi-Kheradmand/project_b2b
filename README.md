# B2B Credit and Recharge Platform

A Django-based backend project for managing user credit requests and phone recharge services. This project is designed as a sample for demonstrating my skills in backend development, with a focus on handling financial transactions, asynchronous task management, and API development.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [License](#license)

## Features

- **User Authentication**: Secure login and registration for sellers and administrators using JWT token.
- **Credit Request Management**: Sellers can request credit, and admins can approve or reject these requests.
- **Phone Recharge Service**: Sellers can recharge their phones using their available credits.
- **Transaction History**: View detailed records of credit and recharge transactions.
- **Atomic Transactions**: Ensures data integrity during critical operations, such as credit approvals and phone recharges.
- **Asynchronous Task Handling**: Celery is used to handle time-consuming tasks like phone recharge requests asynchronously.
- **Swagger API Documentation**: Auto-generated API documentation using DRF Spectacular.
- **Atomic Transactions and F Expressions**: Ensures data integrity during critical operations, such as credit approvals and phone recharges. It helps prevent race conditions when multiple requests are processed concurrently.


## Technologies Used

- **Python**: The core programming language.
- **Django**: Main web framework for building the backend.
- **Django Rest Framework (DRF)**: For creating robust RESTful APIs.
- **Celery**: For asynchronous task processing.
- **Redis**: As a message broker for Celery.
- **Docker & Docker Compose**: For containerizing the application and its services.
- **GitHub Actions**: For CI/CD pipeline (if applicable).
- **Atomic Transactions**: To ensure the integrity of complex database operations.


## Setup and Installation

To run this project locally, follow these steps:

### Prerequisites

- **Python 3.10+**
- **Docker and Docker Compose**
- **Redis** (installed via Docker)
- **RabitMQ** (installed via Docker)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/mehdi-kheradmand/project_b2b.git
   cd project_b2b
 
2. **Create a .env file based on the .env.example**:
cp .env.example .env
Configure your environment variables in .env.

3. **Run the application using Docker Compose**:
docker-compose up --build

4. **Run migrations and create superuser**:
docker-compose exec b2b_django python manage.py migrate
docker-compose exec b2b_django python manage.py createsuperuser

5. **Access the application**:
The API documentation is available at: http://localhost:8000/
The admin panel is available at: http://localhost:8000/admin/

## API Endpoints
Here is a list of the main API endpoints available in the project:

### Credit Request Endpoints
- POST /api/accounting/credit-request/: Create a new credit request.
- PATCH /api/accounting/credit-requests/<id>/process/: Approve or reject a credit request.
- Recharge Endpoints
- POST /api/accounting/recharge-request/: Make a phone recharge request.
- GET /api/accounting/recharge-history/: Retrieve recharge history.
### Transaction Endpoints
- GET /api/accounting/transactions/: Retrieve all credit and recharge transactions.

## Testing
This project includes unit tests to ensure the functionality of critical components.

### Running Tests
To run tests, make sure Docker services are up and running, then execute:

docker-compose exec b2b_django python manage.py test


**Note**: The tests use mock objects for Celery tasks to avoid dependency on the actual message broker.