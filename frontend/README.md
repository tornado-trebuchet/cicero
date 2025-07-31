Cicero Frontend

Integration Points
The key integration areas between frontend and backend:

Core Services Layer:

Create service classes that map 1:1 with your FastAPI routers
Group them by domain (context, text, common)
Models Layer:

Define TypeScript interfaces matching your FastAPI DTOs
Maintain the same property names for consistency
Feature Modules:

Each feature module corresponds to a domain area in the backend
