# Simple API

A basic API project designed for demonstration and learning purposes.

## Table of Contents

- [Description](#description)
- [Architecture](#architecture)
- [How to Run](#how-to-run)
- [Testing](#testing)
- [Functional Requirements](#functional-requirements)
- [Limitations](#limitations)
- [Possible Improvements](#possible-improvements)

---

## Description

This project implements a simple RESTful API using **FastAPI** in Python. It serves as a template for building maintainable backend services, focusing on simplicity, scalability, and ease of use for learning purposes.

---

## Architecture

- **Framework**: FastAPI
- **Endpoints**: Accessible through `http://localhost:3000/docs` (available when the application is running)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Structure**: 3-layer architecture (API, Domain, Infrastructure)

### Architectural Decision Records (ADRs)

**ADR.01: 3-Layer Architecture**  
The 3-layer architecture (API, Domain, Infrastructure) was chosen for its simplicity, ensuring the delivery of core functionalities in a scalable and maintainable way.

**ADR.02: Async Database Engine**  
An asynchronous database engine was selected over a synchronous one to optimize performance for I/O-bound operations. Async operations enable concurrent database queries without blocking, improving throughput and reducing latency, especially under high load.

**ADR.03: Generic Base Repository Pattern**  
A generic base repository pattern was implemented to provide a consistent interface for data access operations. This reduces code duplication, standardizes database interactions, and simplifies maintenance by centralizing common CRUD operations in a reusable component.

**ADR.04: Pydantic BaseModel**  
Pydantic's `BaseModel` is used for data validation, transfer, and documentation. It integrates seamlessly with Swagger for API documentation and provides robust validation for input/output data.

**ADR.05: Database Seeding**  
A database seeding script will execute on the first application startup. The seeder will **not run in production** and will **only execute once** to prevent duplicate data.

**ADR.06: Pagination**  
While the challenge required only filtering, pagination was added to listing endpoints to improve performance and manage (hypothetical)large datasets efficiently.

---

## How to Run

Follow these steps to set up and run the API locally:

1. **Clone the Repository**  
   ```bash
   git clone <repository-url>
   cd fast-api-example
   ```

2. **Install Poetry**  
   Ensure Poetry is installed. If not, install it using:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   poetry --version
   ```

3. **Activate Poetry Virtual Environment**  
   ```bash
   poetry shell
   ```
   or use
   ```bash
   poetry env activate
   ```

5. **Install Dependencies**  
   Install project dependencies using Poetry:
   ```bash
   poetry install
   ```

6. **Set Up the Database**
   Outside Poetry's virtual environment, use your terminal(Ubuntu) to create a PostgreSQL database and user with these commands:
   ```sql
   sudo -u postgres psql
   CREATE DATABASE simple_api_db;
   \c simple_api_db
   CREATE USER admin WITH PASSWORD '123';
   DROP SCHEMA public CASCADE;
   CREATE SCHEMA public;
   ALTER SCHEMA public OWNER TO admin;
   GRANT ALL PRIVILEGES ON SCHEMA public TO admin;
   ```

7. **Configure Environment Variables**  
   Create a `.env` file based on the template below:
   ```env
   ENV="dev" # or "prod"
   APP_NAME="Simple API"
   DATABASE_URL=postgresql+asyncpg://admin:123@localhost/simple_api_db
   ```

8. **Run Database Migrations**
   While inside Poetry’s virtual environment, export DATABASE_URL and run the migrations:
   ```bash
   export DATABASE_URL="postgresql+asyncpg://admin:123@localhost/simple_api_db"
   alembic upgrade head
   ```

9. **Run the Application**  
   While inside Poetry’s virtual environment, start the FastAPI server:
   ```bash
   cd simple_api
   poetry run uvicorn main:app --reload
   ```

10. **Access the API**  
   Open a browser and navigate to:
   ```
   http://localhost:3000/docs
   ```

---

## Testing

To test the API, use the interactive Swagger UI at `http://localhost:3000/docs` to explore and test endpoints. Ensure the application and database are running before testing.

### Unit Testing
This application tests its core domain with unit tests.
To run the unit tests, make sure you are in the root directory of the project. You can execute all tests using **pytest** with verbose output:

```bash
pytest -v
```

---

## Functional Requirements

### 1. Property Creation
- Endpoint to create a new property

### 2. List Properties
- Endpoint to list all available properties in the system
- Supports filtering by:
  - Neighborhood, city, or state
  - Maximum capacity
  - Maximum price
- Filtering by neighborhood, city, or state returns all matching properties
- Pagination is supported for list endpoints


### 3. Create a Booking
- User can create a booking for a property
- System validations:
  - Property availability for requested dates
  - Guest count does not exceed property capacity
  - Booking dates are valid (end date after start date, no bookings in the past)
  - Prevent overlapping bookings, considering check-in/check-out logic:
    - If a booking ends on day 10, a new booking can start on day 10
    - If a booking starts on day 1, another booking can end on day 1
- If validations pass, the booking is created; otherwise, the API returns a costumized domain error
- The total price is automatically calculated as the sum of nightly rates multiplied by the number of nights

### 4. List Bookings
- Endpoint to list all bookings for:
  - A specific property
  - A specific client (by email)
- Pagination is supported

### 5. Cancel a Booking
- Endpoint to cancel an existing booking

### 6. Check Availability
- Endpoint to check property availability for a given date range
- Considers existing bookings and ensures no overlap according to check-in/check-out logic


---

## Limitations

- **Manual Migration Setup**: The `.env` file must be exported in the terminal before running Alembic migrations.
- **Local Environment Only**: The application currently runs only on `localhost` with no deployment setup.
- **Separate Initialization**: The database and application must be initialized separately.

---

## Possible Improvements

- **Containerization**: Use Docker to containerize the application and database for easier environment setup.
- **Architecture Upgrade**: Transition to a Hexagonal (Ports and Adapters) architecture with Domain-Driven Design (DDD) and a Modular Monolith approach for scalability:
  - Implement interfaces between layers.
  - Enrich the domain with entities and value objects.
  - Apply the Facade design pattern for model interactions.
- **Semantic**: Moving check availability endpoint to property router
- **Testing**: Add integration tests.
- **Fitness Functions**: Implement fitness functions to ensure architectural quality.
- **Validation**: Add checks for duplicate properties in data models.
