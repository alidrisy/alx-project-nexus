# User Registration API Documentation

## Overview
The User Registration API allows users to create new accounts with either a regular USER role or a RECRUITER role. This endpoint is part of the JobBoard platform's authentication system.

## Endpoint Details

- **URL**: `/api/accounts/register/`
- **Method**: `POST`
- **Authentication**: Not required (public endpoint)
- **Content-Type**: `application/json`

## Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `username` | string | ✅ Yes | - | Unique username (1-150 characters) |
| `email` | string | ❌ No | "" | Email address (optional) |
| `password` | string | ✅ Yes | - | Secure password (must meet Django validation) |
| `role` | string | ❌ No | "USER" | User role: "USER" or "RECRUITER" |

## Role Types

- **USER**: Regular user account (default)
- **RECRUITER**: Recruiter account with additional privileges

## Request Examples

### 1. Regular User Registration
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "role": "USER"
}
```

### 2. Recruiter Registration
```json
{
    "username": "recruiter_jane",
    "email": "jane@company.com",
    "password": "SecurePass123!",
    "role": "RECRUITER"
}
```

### 3. Default Role Registration
```json
{
    "username": "alice_smith",
    "email": "alice@example.com",
    "password": "SecurePass123!"
}
```
*Note: Role defaults to "USER" when not specified*

## Response Format

### Success Response (201 Created)
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "role": "USER"
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Error Response (400 Bad Request)
```json
{
    "error": "Validation failed",
    "details": {
        "username": ["Username already taken"],
        "password": ["This password is too short. It must contain at least 8 characters."]
    }
}
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 201 | User created successfully |
| 400 | Validation error (bad request) |
| 500 | Internal server error |

## Common Validation Errors

### Username Validation
- Username must be 1-150 characters
- Username must be unique
- Username cannot contain special characters

### Password Validation
- Minimum 8 characters
- Cannot be too common
- Cannot be entirely numeric
- Cannot be similar to username

### Email Validation
- Must be valid email format
- Must be unique if provided
- Optional field

## Testing the Endpoint

### Using cURL
```bash
# Register a regular user
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "role": "USER"
  }'

# Register a recruiter
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testrecruiter",
    "email": "recruiter@company.com",
    "password": "SecurePass123!",
    "role": "RECRUITER"
  }'
```

### Using Python requests
```python
import requests

# Register user
response = requests.post('http://localhost:8000/api/accounts/register/', json={
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'SecurePass123!',
    'role': 'USER'
})

if response.status_code == 201:
    print("User registered successfully!")
    print(response.json())
else:
    print("Registration failed:", response.json())
```

## Swagger Documentation

The API is fully documented with Swagger/OpenAPI. You can access the interactive documentation at:
- **Swagger UI**: `/api/docs/`
- **API Schema**: `/api/schema/`

## Security Features

- **CSRF Protection**: Enabled for web forms
- **Password Validation**: Django's built-in password validation
- **JWT Tokens**: Secure authentication tokens returned upon registration
- **Role-based Access**: Different user roles for different permissions

## Post-Registration

After successful registration:
1. User account is created and activated
2. JWT access and refresh tokens are returned
3. User can immediately authenticate using the returned tokens
4. User can access protected endpoints based on their role

## Troubleshooting

### CSRF Errors
If you encounter CSRF verification errors:
1. Ensure the domain is in `CSRF_TRUSTED_ORIGINS` in Django settings
2. For API calls, CSRF is typically not required
3. Check if you're using the correct content type

### Validation Errors
- Check password strength requirements
- Ensure username is unique
- Verify email format if provided
- Check role value is either "USER" or "RECRUITER"

### Server Errors
- Check Django logs for detailed error information
- Verify database connection
- Ensure all required packages are installed

## Support

For additional support or questions about the registration API:
- Check the Swagger documentation at `/api/docs/`
- Review Django logs for detailed error messages
- Contact the development team for technical issues 