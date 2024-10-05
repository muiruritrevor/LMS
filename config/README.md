# Library Management API

A comprehensive RESTful API for managing library resources, built with Django and Django REST Framework. This API allows for efficient book management, user authentication, and transaction handling.

## Features

* User Authentication (registration and login)
* Book Management (CRUD operations)
* Transaction Handling (Checkouts and Returns)
* Browsable API Interface
* User Profiles for Managing Personal Data
* Search and Filter Books by Title, Author, or ISBN
* Pagination for Book Lists

## Technologies

* **Django 5.1**: Web framework for building the API
* **Django REST Framework 3.15.2**: Toolkit for building Web APIs
* **MySQL**: Database for storing user data and books
* **Simple JWT 5.3.1**: JWT authentication for Django REST Framework
* **django-filter 24.3**: Dynamic queryset filtering
* **Python 3.x**: Programming language

## Getting Started

Follow these steps to set up the project locally.

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/muiruritrevor/LMS.git
   cd library-management-api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - On Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database**:
   - Update the database settings in `settings.py` if needed
   - Run migrations:
     ```bash
     python manage.py migrate
     ```

6. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Add sample data** (optional):
   ```bash
   python manage.py add_sample_books
   ```

### Running the API

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the API**:
   - Browsable API: Open your browser to `http://127.0.0.1:8000/api/`
   - Admin interface: `http://127.0.0.1:8000/admin/`

## API Endpoints

### Authentication
- `POST /auth/` - Obtain JWT token
- `POST /auth/token/refresh/` - Refresh JWT token
- `POST /api-auth/login/` - Session-based login for browsable API

### Books
- `GET /api/books/` - List all books
- `POST /api/books/` - Add a new book (Admin only)
- `GET /api/books/{id}/` - Retrieve a specific book
- `PUT /api/books/{id}/` - Update a book (Admin only)
- `DELETE /api/books/{id}/` - Delete a book (Admin only)

### Transactions
- `POST /api/books/{id}/checkout/` - Checkout a book
- `POST /api/books/{id}/return/` - Return a book
- `GET /api/transactions/` - List user's transactions

## Testing
To test the API run the command below

```bash
python manage.py test api
```

## Deployment

This API is currently deployed on PythonAnywhere. For deployment instructions, refer to the [PythonAnywhere documentation](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/).

## Contributing

Contributions are welcome, If you would like to contribute;
1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is free to use and belongs to Trevor Muiruri, contact muiruriitrevor@gmail.com for usage details.

## Acknowledgements
- Django documentation
- Django REST Framework documentation
- PythonAnywhere for hosting
