from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

# Generate and store API keys
API_KEYS = {
    secrets.token_urlsafe(32): True,
    secrets.token_urlsafe(32): True,
    secrets.token_urlsafe(32): True
}

print("=" * 60)
print("API KEYS (for testing):")
print("=" * 60)
for i, key in enumerate(API_KEYS.keys(), 1):
    print(f"Key {i}: {key}")
print("=" * 60)

def verify_api_key(request):
    """Verify API key from request headers."""
    api_key = request.headers.get('X-API-Key')
    
    if not api_key:
        return False, "API key is missing"
    
    if api_key not in API_KEYS:
        return False, "Invalid API key"
    
    return True, "Valid"

@app.route('/process', methods=['POST'])
def process_text():
    """Process text endpoint with API key authentication."""
    try:
        # Verify API key
        is_valid, message = verify_api_key(request)
        
        if not is_valid:
            return jsonify({
                'error': message,
                'status': 'unauthorized'
            }), 401
        
        # Get JSON data
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text',
                'status': 'bad_request'
            }), 400
        
        # Process text (convert to uppercase)
        text = data['text']
        processed_text = text.upper()
        
        return jsonify({
            'input': text,
            'output': processed_text,
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'running'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
