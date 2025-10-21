# String Analysis API

A RESTful API service that analyzes strings and stores their computed properties including length, palindrome detection, character frequency, and more.

## Features

- **String Analysis**: Automatically computes 6 properties for each string
- **CRUD Operations**: Create, read, and delete string entries
- **Advanced Filtering**: Filter strings by multiple criteria
- **Natural Language Queries**: Query using plain English
- **SHA-256 Identification**: Unique hash-based IDs for each string

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd string-analysis-api
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Locally

Start the Flask development server:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Create/Analyze String
**POST** `/strings`

Request:
```json
{
  "value": "hello world"
}
```

Response (201):
```json
{
  "id": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
  "value": "hello world",
  "properties": {
    "length": 11,
    "is_palindrome": false,
    "unique_characters": 8,
    "word_count": 2,
    "sha256_hash": "b94d27b9...",
    "character_frequency_map": {
      "h": 1,
      "e": 1,
      "l": 3,
      "o": 2,
      " ": 1,
      "w": 1,
      "r": 1,
      "d": 1
    }
  },
  "created_at": "2025-10-20T10:00:00Z"
}
```

### 2. Get Specific String
**GET** `/strings/{string_value}`

Example: `GET /strings/hello%20world`

Response (200): Same as create response

### 3. Get All Strings with Filtering
**GET** `/strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a`

Query Parameters:
- `is_palindrome`: boolean (true/false)
- `min_length`: integer
- `max_length`: integer
- `word_count`: integer
- `contains_character`: single character

Response (200):
```json
{
  "data": [ /* array of string objects */ ],
  "count": 15,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5
  }
}
```

### 4. Natural Language Filtering
**GET** `/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings`

Supported queries:
- "all single word palindromic strings"
- "strings longer than 10 characters"
- "palindromic strings that contain the first vowel"
- "strings containing the letter z"

Response (200):
```json
{
  "data": [ /* matching strings */ ],
  "count": 3,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}
```

### 5. Delete String
**DELETE** `/strings/{string_value}`

Response (204): No content

## Testing Examples

### Using curl

Create a string:
```bash
curl -X POST http://localhost:5000/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'
```

Get a string:
```bash
curl http://localhost:5000/strings/racecar
```

Get all palindromes:
```bash
curl "http://localhost:5000/strings?is_palindrome=true"
```

Natural language query:
```bash
curl "http://localhost:5000/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings"
```

Delete a string:
```bash
curl -X DELETE http://localhost:5000/strings/racecar
```

## Error Codes

- `200 OK`: Successful GET request
- `201 Created`: String successfully created
- `204 No Content`: String successfully deleted
- `400 Bad Request`: Invalid request body or query parameters
- `404 Not Found`: String not found
- `409 Conflict`: String already exists
- `422 Unprocessable Entity`: Invalid data type or conflicting filters

## Dependencies

- **Flask**: Web framework for building the API
- **Werkzeug**: WSGI utility library (comes with Flask)

No database required - uses in-memory storage for simplicity.

## Environment Variables

No environment variables required for basic operation. The API runs on:
- Host: `0.0.0.0`
- Port: `5000`

## Project Structure

```
string-analysis-api/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Notes

- Data is stored in-memory and will be lost when the server restarts
- The API uses SHA-256 hashing to generate unique IDs
- Palindrome detection is case-insensitive
- Natural language parsing supports common query patterns
- All timestamps are in UTC ISO 8601 format

