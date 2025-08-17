# Simple API

A basic API project designed for demonstration and learning purposes.

## Summary

- [**Description:**](#description) Overview of the project and its purpose.
- [**Architecture:**](#architecture) Main components and structure.
- [**Testing:**](#testing) How to test the project.
- [**How to Run:**](#how-to-run) Steps to start the API.
- [**Limitations:**](#limitations) Known issues or constraints.
- [**Possible Improvements:**](#possible-improvements) Suggestions for future enhancements.

---

## Description

This project implements a simple RESTful API using python FastAPI. It serves as a template for building maintainable backend services.

## Architecture

- **Framework:** FastAPI
- **Endpoints:** Acessible through ```http://localhost:3000/docs``` (you have to be running the application)
- **Database:** PostgreSQL + ORM (SQLAlchemy)
- **Structure:** 3 layer architecture (api-domain-infra)

ADR.01: The choice of the 3 layer architecture was given by the simplicity of the challenge, focusing on delivering all main functionalities in a simple but scalable and mantainable manner. 

ADR.02: The decision to use an async database engine over synchronous was made to optimize performance in I/O-bound operations. Async operations allow the API to handle multiple database queries concurrently without blocking, resulting in better throughput and reduced latency, especially under high load scenarios.
ADR.02: The decision to use an async database engine over synchronous was made to optimize performance in I/O-bound operations. Async operations allow the API to handle multiple database queries concurrently without blocking, resulting in better throughput and reduced latency, especially under high load scenarios.

ADR.03: Implementation of a generic base repository pattern provides a consistent interface for data access operations. This approach reduces code duplication, standardizes database interactions, and simplifies maintenance by centralizing common CRUD operations in a single, reusable component. The base repository can be extended for specific entity requirements while maintaining a uniform data access pattern across the application.

ADR.04: Usage of pydantics BaseModel for data validation, transfer and documentation. The use of pydantics easily satisfy all these requirements and provides a simple way of integrating with swagger and validating data input / output

## Testing


## How to Run

## Limitations

- To generate a new migration you have to export the .env in the current terminal before running the alembic command
- There is no current deploy for this application. You have to run through localhost and test it locally.
- Both the DB and the application have to be initialized separatelly (check improvements - docker session)

## Possible Improvements

- Use docker to containerize application and facilitate set up of environments
- Upgrade Architecture to Hexagonal + DDD + Modular Monolith approach (Only if there is prevision for growth)
    - Apply Interfaces between layers (Ports and adapters)
    - Enrich domain with its own entity and value Objects
    - Apply the FACADE Design Pattern between models
- Add of Integration Tests
- Implementation of Fitness Functions
- Validation for duplicate properties


psql -U postgres
CREATE DATABASE simple_api_db;
\c simple_api_db
CREATE USER admin WITH PASSWORD '123';
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
ALTER SCHEMA public OWNER TO admin;
GRANT ALL PRIVILEGES ON SCHEMA public TO admin;
export DATABASE_URL=your_url
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
