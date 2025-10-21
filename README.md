⭐ **String Analyzer API: Unraveling Text with Intelligent Analysis**

## Overview
A robust Flask-based RESTful API service built with Python 3.8+ that provides advanced string analysis capabilities, storing computed properties in-memory and offering flexible querying, including natural language processing.

## Features
✅ **String Analysis**: Automatically computes 6 distinct properties for each string submitted, including length, palindrome status, unique character count, word count, SHA-256 hash, and a detailed character frequency map.
➕ **CRUD Operations**: Seamlessly create new string entries, retrieve existing ones by value, list all strings with filters, and delete unwanted entries.
🔍 **Advanced Filtering**: Enables precise filtering of stored strings based on various criteria such as palindrome status, minimum/maximum length, word count, and character containment.
🗣️ **Natural Language Queries**: Offers an intuitive search interface, allowing users to query strings using descriptive English sentences (e.g., "all single word palindromic strings").
🔑 **SHA-256 Identification**: Each string is uniquely identified and stored using its SHA-256 hash, ensuring data integrity and preventing duplicate entries.

## Technologies Used
This project leverages the following key technologies:

| Technology | Description                                         | Link                                    |
| :--------- | :-------------------------------------------------- | :-------------------------------------- |
| Python     | The core programming language for the backend logic. | [Python](https://www.python.org/)       |
| Flask      | A lightweight and flexible micro web framework used to build the API. | [Flask](https://flask.palletsprojects.com/) |
| Werkzeug   | A comprehensive WSGI toolkit that powers the Flask framework. | [Werkzeug](https://werkzeug.palletsprojects.com/) |

## Getting Started

### Installation
To get a copy of the project up and running on your local machine, follow these steps:

1.  👯‍♀️ **Clone the Repository**:
    ```bash
    git clone https://github.com/Olalolo22/HNG13_1.git
    cd HNG13_1
    ```

2.  🐍 **Create a Virtual Environment** (recommended to manage dependencies):
    ```bash
    python -m venv venv
    
    # On Windows
    venv\Scripts\activate
    
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  📦 **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Running Locally
After installation, you can start the Flask development server:
```bash
python app.py
```
The API will be accessible at `http://localhost:5000`.

### Environment Variables
No specific environment variables are explicitly required for the API's basic operation. It runs on `host='0.0.0.0'` and `port=5000` by default.

## API Documentation

### Base URL
`http://localhost:5000`

### Endpoints

#### POST /strings
Creates a new string entry, computes its properties, and stores it.

**Request**:
```json
{
  "value": "hello world"
}
```
**Response**:
```json
{
  "id": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
  "value": "hello world",
  "properties": {
    "length": 11,
    "is_palindrome": false,
    "unique_characters": 8,
    "word_count": 2,
    "sha256_hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
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

**Errors**:
- `400 Bad Request`: Invalid request body or missing `'value'` field.
- `409 Conflict`: String already exists.
- `422 Unprocessable Entity`: `'value'` field is not a string.

#### GET /strings/{string_value}
Retrieves a specific string entry by its original value.

**Request**:
No payload. `string_value` is URL-encoded.
Example: `GET /strings/hello%20world`

**Response**:
```json
{
  "id": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
  "value": "hello world",
  "properties": {
    "length": 11,
    "is_palindrome": false,
    "unique_characters": 8,
    "word_count": 2,
    "sha256_hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
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
**Errors**:
- `404 Not Found`: String not found.

#### GET /strings
Retrieves a list of all stored strings, with optional filtering based on string properties.

**Query Parameters**:
- `is_palindrome`: boolean (`true`/`false`)
- `min_length`: integer
- `max_length`: integer
- `word_count`: integer
- `contains_character`: single character

**Request**:
No payload. Parameters are passed as query strings.
Example: `GET /strings?is_palindrome=true&min_length=5&word_count=2`

**Response**:
```json
{
  "data": [
    {
      "id": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
      "value": "hello world",
      "properties": { /* ... */ },
      "created_at": "2025-10-20T10:00:00Z"
    }
  ],
  "count": 1,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 5,
    "word_count": 2
  }
}
```
**Errors**:
- `400 Bad Request`: Invalid value for query parameters.

#### GET /strings/filter-by-natural-language
Filters strings based on a natural language query.

**Query Parameters**:
- `query`: string (e.g., "all single word palindromic strings")

**Supported Queries (examples)**:
- "all single word palindromic strings"
- "strings longer than 10 characters"
- "palindromic strings that contain the first vowel"
- "strings containing the letter z"

**Request**:
No payload. Parameter is passed as a query string.
Example: `GET /strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings`

**Response**:
```json
{
  "data": [
    {
      "id": "7616f73461247ff572186968038753232a829e24df2f24c25f487e45e41209b5",
      "value": "madam",
      "properties": { /* ... */ },
      "created_at": "2025-10-20T10:05:00Z"
    }
  ],
  "count": 1,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "word_count": 1,
      "is_palindrome": true
    }
  }
}
```
**Errors**:
- `400 Bad Request`: Missing `'query'` parameter or inability to parse the natural language query.
- `422 Unprocessable Entity`: Conflicting filters in the natural language query (e.g., `min_length > max_length`).

#### DELETE /strings/{string_value}
Deletes a specific string entry.

**Request**:
No payload. `string_value` is URL-encoded.
Example: `DELETE /strings/delete%20me`

**Response**:
`204 No Content` (Empty response body upon successful deletion).

**Errors**:
- `404 Not Found`: String not found.

## Usage
Once the API is running, you can interact with it using `curl` or any API client. Here are some examples:

1.  **Create a String:**
    ```bash
    curl -X POST http://localhost:5000/strings \
      -H "Content-Type: application/json" \
      -d '{"value": "racecar"}'
    ```

2.  **Create Another String:**
    ```bash
    curl -X POST http://localhost:5000/strings \
      -H "Content-Type: application/json" \
      -d '{"value": "hello world"}'
    ```

3.  **Get a Specific String:**
    ```bash
    curl http://localhost:5000/strings/racecar
    ```

4.  **Get All Palindromic Strings:**
    ```bash
    curl "http://localhost:5000/strings?is_palindrome=true"
    ```

5.  **Get Strings Longer Than 10 Characters:**
    ```bash
    curl "http://localhost:5000/strings?min_length=11"
    ```

6.  **Query Using Natural Language (e.g., "all single word palindromic strings"):**
    ```bash
    curl "http://localhost:5000/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings"
    ```

7.  **Delete a String:**
    ```bash
    curl -X DELETE http://localhost:5000/strings/racecar
    ```

## License
This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/licenses/MIT) file for details.

## Author Info
Developed with dedication by a passionate backend enthusiast. Feel free to connect!

*   **LinkedIn**: [Your LinkedIn Profile](https://www.linkedin.com/in/your_username)
*   **Twitter**: [Your Twitter Handle](https://twitter.com/your_handle)

---

### Project Badges
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://www.npmjs.com/package/dokugen)