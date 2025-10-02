# Dummy FastAPI Project

A simple FastAPI project demonstrating basic CRUD operations with an in-memory data store.

## Features

- **CRUD Operations**: Create, Read, Update, Delete items
- **Pydantic Models**: Type-safe data validation
- **Auto-generated Documentation**: Interactive API docs with Swagger UI
- **Search Functionality**: Search items by name
- **Filtering**: Get only available items

## API Endpoints

### Core Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /items` - Get all items
- `GET /items/{item_id}` - Get item by ID
- `POST /items` - Create new item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

### Additional Endpoints
- `GET /items/search/{name}` - Search items by name
- `GET /items/available` - Get only available items

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
# Using uvicorn directly
uvicorn main:app --reload

# Or run the main.py file
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Usage Examples

### Create an Item
```bash
curl -X POST "http://localhost:8000/items" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Laptop",
       "description": "Gaming laptop",
       "price": 999.99,
       "is_available": true
     }'
```

### Get All Items
```bash
curl -X GET "http://localhost:8000/items"
```

### Update an Item
```bash
curl -X PUT "http://localhost:8000/items/1" \
     -H "Content-Type: application/json" \
     -d '{
       "price": 899.99,
       "is_available": false
     }'
```

### Delete an Item
```bash
curl -X DELETE "http://localhost:8000/items/1"
```

## Data Model

### Item
```json
{
  "id": 1,
  "name": "string",
  "description": "string (optional)",
  "price": 0.0,
  "is_available": true
}
```

## Project Structure

```
fastapi_project/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Next Steps

This is a basic FastAPI project. To make it production-ready, consider:

1. **Database Integration**: Replace in-memory storage with a real database (PostgreSQL, SQLite, etc.)
2. **Authentication**: Add user authentication and authorization
3. **Error Handling**: Implement comprehensive error handling
4. **Testing**: Add unit and integration tests
5. **Logging**: Add proper logging
6. **Environment Configuration**: Use environment variables for configuration
7. **Docker**: Containerize the application
8. **CI/CD**: Set up continuous integration and deployment

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications
