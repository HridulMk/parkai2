# User Registration API

## Endpoint
```
POST /api/auth/register/
```

## Request Body
```json
{
  "username": "string (required)",
  "email": "string (required)",
  "full_name": "string (required)",
  "phone": "string (optional)",
  "user_type": "customer|vendor (optional, defaults to 'customer')",
  "password": "string (required, min 6 characters)",
  "password_confirm": "string (required, must match password)"
}
```

## Response (Success - 201 Created)
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "user_type": "customer"
  }
}
```

## Response (Error - 400 Bad Request)
```json
{
  "username": ["A user with that username already exists."],
  "email": ["Enter a valid email address."],
  "non_field_errors": ["Passwords do not match"]
}
```

## Frontend Integration

The registration form collects:
- Full Name (split into first_name and last_name)
- Email (used as username for login)
- Phone Number
- User Type (Customer or Vendor)
- Password with confirmation

## Example Usage

```javascript
const registerUser = async (userData) => {
  try {
    const response = await fetch('/api/auth/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData)
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Registration successful:', result);
      // Navigate to login page
    } else {
      const errors = await response.json();
      console.error('Registration failed:', errors);
      // Display errors to user
    }
  } catch (error) {
    console.error('Network error:', error);
  }
};
```