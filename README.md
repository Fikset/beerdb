# BeerDB - Craft Beer Data Management System

A comprehensive Python application for collecting, storing, analyzing, and serving craft beer data from the PunkAPI.


## Features

### ✅ 1. Web Application
- **Flask-based web server** (`src/app.py`)
- Interactive HTML form for user input
- Multiple endpoints: `/`, `/echo_user_input`, `/health`, `/metrics`
- Production-ready with Gunicorn WSGI server
- Containerized deployment support via Procfile

### ✅ 2. Basic Form & Reporting
- **HTML form interface** for user input submission
- Form data processing and echo functionality
- Health check endpoint for monitoring
- Metrics endpoint for operational insights

### ✅ 3. Data Collection
- **External API integration** with PunkAPI (`src/data_fetcher/fetcher.py`)
- Automated data fetching from `https://api.punkapi.com/v2/beers`
- Configurable pagination and batch processing
- JSON data persistence to local file system
- Dockerized fetcher service with dedicated requirements

### ✅ 4. Data Analyzer
- **Comprehensive analysis engine** (`src/data_analyzer/analyzer.py`)
- ABV (Alcohol By Volume) distribution analysis
- Hops popularity and ingredient analysis
- Statistical summaries and insights generation
- JSON data processing and aggregation

### ✅ 5. Unit Tests
- **Complete test suite** covering all major components
- Data fetcher tests (`test/data_fetcher/test_fetcher.py`)
- Mock-based testing (`test/test_mocks.py`)
- Application endpoint testing (`test/test_app.py`)
- Client-server communication tests

### ✅ 6. Data Persistence
- **SQLite database integration** (`src/database/db_manager.py`)
- Structured beer data storage with schema management
- CRUD operations for beer entities
- Batch data processing capabilities
- In-memory database support for testing

### ✅ 7. REST API/Collaboration
- **Internal API endpoints** for data access
- RESTful service architecture
- Client-server communication via sockets (`src/Client.py`, `src/Server.py`)
- External API integration with PunkAPI
- Health check and metrics endpoints

### ✅ 8. Production Environment
- **Heroku deployment configuration** (Procfile)
- Production WSGI server (Gunicorn)
- Environment-specific configuration management
- Production-ready dependency management
- Cloud deployment automation

### ✅ 9. Integration Tests
- **End-to-end testing suite** (`test/integration/test_integration.py`)
- Full data pipeline testing (fetch → store → analyze)
- Web application endpoint integration testing
- Cross-component interaction validation
- Production-like test scenarios

### ✅ 10. Mock Objects & Test Doubles
- **Comprehensive mocking strategy** (`test/test_mocks.py`)
- HTTP request mocking for external API calls
- Database operation mocking
- File system operation mocking
- Isolated unit testing with dependency injection

### ✅ 11. Continuous Integration
- **GitHub Actions workflow** (`.github/workflows/main.yml`)
- Automated testing on push/PR events
- Multi-stage CI pipeline (test → deploy)
- Python environment setup and dependency caching
- Comprehensive test execution across all modules

### ✅ 12. Production Monitoring & Instrumentation
- **Prometheus metrics integration** (`src/app.py`)
- Request processing time tracking
- Custom metrics collection and exposure
- Prometheus configuration (`prometheus.yml`)
- Health check endpoints for monitoring
- Production observability setup

### ✅ 13. Event Collaboration & Messaging
- **Event-driven architecture** (`src/messaging/event_publisher.py`)
- Asynchronous event publishing and subscription
- Background event processing with threading
- Decoupled component communication
- Event-based data flow coordination

