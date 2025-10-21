from flask import Flask, request, jsonify
from datetime import datetime
import hashlib
import re

app = Flask(__name__)

# In-memory storage
strings_db = {}

def compute_sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def is_palindrome(text):
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

def character_frequency_map(text):
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    return freq

def analyze_string(value):
    return {
        "length": len(value),
        "is_palindrome": is_palindrome(value),
        "unique_characters": len(set(value)),
        "word_count": len(value.split()),
        "sha256_hash": compute_sha256(value),
        "character_frequency_map": character_frequency_map(value)
    }

def parse_natural_language(query):
    query_lower = query.lower()
    filters = {}
    
    # Parse word count
    if "single word" in query_lower:
        filters["word_count"] = 1
    elif "two word" in query_lower or "2 word" in query_lower:
        filters["word_count"] = 2
    
    # Parse palindrome
    if "palindrom" in query_lower:
        filters["is_palindrome"] = True
    
    # Parse length constraints
    length_match = re.search(r'longer than (\d+)', query_lower)
    if length_match:
        filters["min_length"] = int(length_match.group(1)) + 1
    
    shorter_match = re.search(r'shorter than (\d+)', query_lower)
    if shorter_match:
        filters["max_length"] = int(shorter_match.group(1)) - 1
    
    # Parse character containment
    if "first vowel" in query_lower:
        filters["contains_character"] = "a"
    
    contains_match = re.search(r'contain(?:ing|s)? (?:the )?letter ([a-z])', query_lower)
    if contains_match:
        filters["contains_character"] = contains_match.group(1)
    
    return filters

def apply_filters(strings_list, filters):
    result = strings_list
    
    if "is_palindrome" in filters:
        result = [s for s in result if s["properties"]["is_palindrome"] == filters["is_palindrome"]]
    
    if "min_length" in filters:
        result = [s for s in result if s["properties"]["length"] >= filters["min_length"]]
    
    if "max_length" in filters:
        result = [s for s in result if s["properties"]["length"] <= filters["max_length"]]
    
    if "word_count" in filters:
        result = [s for s in result if s["properties"]["word_count"] == filters["word_count"]]
    
    if "contains_character" in filters:
        char = filters["contains_character"]
        result = [s for s in result if char in s["value"]]
    
    return result

@app.route('/strings', methods=['POST'])
def create_string():
    data = request.get_json()
    
    # Validate  the request body
    if not data:
        return jsonify({"error": "Invalid request body"}), 400
    
    if "value" not in data:
        return jsonify({"error": "Missing 'value' field"}), 400
    
    value = data["value"]
    
    # Validate the data type
    if not isinstance(value, str):
        return jsonify({"error": "'value' must be a string"}), 422
    
    # Check if string already exists
    sha256_hash = compute_sha256(value)
    if sha256_hash in strings_db:
        return jsonify({"error": "String already exists"}), 409
    
    # Create and store string
    properties = analyze_string(value)
    created_at = datetime.utcnow().isoformat() + "Z"
    
    string_obj = {
        "id": sha256_hash,
        "value": value,
        "properties": properties,
        "created_at": created_at
    }
    
    strings_db[sha256_hash] = string_obj
    
    return jsonify(string_obj), 201

@app.route('/strings/<string:string_value>', methods=['GET'])
def get_string(string_value):
    sha256_hash = compute_sha256(string_value)
    
    if sha256_hash not in strings_db:
        return jsonify({"error": "String not found"}), 404
    
    return jsonify(strings_db[sha256_hash]), 200

@app.route('/strings', methods=['GET'])
def get_all_strings():
    # Get query parameters
    filters = {}
    
    if 'is_palindrome' in request.args:
        val = request.args.get('is_palindrome').lower()
        if val not in ['true', 'false']:
            return jsonify({"error": "Invalid value for is_palindrome"}), 400
        filters["is_palindrome"] = val == 'true'
    
    if 'min_length' in request.args:
        try:
            filters["min_length"] = int(request.args.get('min_length'))
        except ValueError:
            return jsonify({"error": "Invalid value for min_length"}), 400
    
    if 'max_length' in request.args:
        try:
            filters["max_length"] = int(request.args.get('max_length'))
        except ValueError:
            return jsonify({"error": "Invalid value for max_length"}), 400
    
    if 'word_count' in request.args:
        try:
            filters["word_count"] = int(request.args.get('word_count'))
        except ValueError:
            return jsonify({"error": "Invalid value for word_count"}), 400
    
    if 'contains_character' in request.args:
        filters["contains_character"] = request.args.get('contains_character')
    
    # Apply filters and get all strings
    all_strings = list(strings_db.values())
    filtered_strings = apply_filters(all_strings, filters)
    
    return jsonify({
        "data": filtered_strings,
        "count": len(filtered_strings),
        "filters_applied": filters
    }), 200

@app.route('/strings/filter-by-natural-language', methods=['GET'])
def filter_by_natural_language():
    query = request.args.get('query', '')
    
    if not query:
        return jsonify({"error": "Missing 'query' parameter"}), 400
    
    try:
        parsed_filters = parse_natural_language(query)
        
        # Check for conflicting filters
        if "min_length" in parsed_filters and "max_length" in parsed_filters:
            if parsed_filters["min_length"] > parsed_filters["max_length"]:
                return jsonify({"error": "Conflicting filters: min_length > max_length"}), 422
        
        # Apply filters
        all_strings = list(strings_db.values())
        filtered_strings = apply_filters(all_strings, parsed_filters)
        
        return jsonify({
            "data": filtered_strings,
            "count": len(filtered_strings),
            "interpreted_query": {
                "original": query,
                "parsed_filters": parsed_filters
            }
        }), 200
    except Exception as e:
        return jsonify({"error": "Unable to parse natural language query"}), 400

@app.route('/strings/<string:string_value>', methods=['DELETE'])
def delete_string(string_value):
    sha256_hash = compute_sha256(string_value)
    
    if sha256_hash not in strings_db:
        return jsonify({"error": "String not found"}), 404
    
    del strings_db[sha256_hash]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)