# API Endpoint Tests (Pytest + Requests) — CI with GitHub Actions

This repository contains a small Proof of Concept (PoC) test suite that validates a REST API `/users` service using **pytest** and **requests**, executed in CI via **GitHub Actions**.  
The tests run against two environments exposed by the same container image:

- **/dev** (mapped locally to port `3001`)
- **/prod** (mapped locally to port `3002`)

The pipeline starts the API using Docker, waits for the service to become available, then runs the test suite.

---

## What This PoC Demonstrates

- **API contract validation** with pytest (`GET/POST/PUT/DELETE`)  
- **HTTP request testing** using `requests`
- **URL-safe path handling** using `urllib.parse.quote` (important for email identifiers)
- **CI automation** using GitHub Actions
- **Containerized integration testing** by starting the app under test with Docker

---

## Project Layout

``.
├── tests/
│   └── test_endpoints.py
└── .github/
└── workflows/
└── integration.yml

## API Endpoints Covered

The test suite validates the following flows:

### Users Collection
- `GET /{env}/users`  
  Expects **200** and a JSON **list**

- `POST /{env}/users`  
  - Success case expects **201**
  - Validation error expects **400** (missing fields)
  - Duplicate email expects **409**

### User Resource (email as identifier)
- `GET /{env}/users/{email}`  
  - Not found expects **404**
  - Success flow creates then retrieves user (**201 → 200**)

- `PUT /{env}/users/{email}`  
  - Update expects **200**
  - Not found expects **404**

### Delete Authorization Check
- `DELETE /{env}/users/{email}`  
  - Without auth expects **401**
  - With auth expects **204** (assumes a token is accepted)

> Note: The tests encode emails safely for URL paths:
> `quote(email, safe="")`

---

## Requirements

- Python 3.9+
- Docker
- pip

Python dependencies:
- pytest
- requests

---

## Run Locally

### 1) Start the API container

Dev environment:
```bash
docker run -d --name sdet_app_dev -p 3001:3000 ghcr.io/danielsilva-loanpro/sdet-interview-challenge:latest
