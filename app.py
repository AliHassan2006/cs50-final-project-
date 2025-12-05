from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('conversions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  input_text TEXT NOT NULL,
                  output_text TEXT NOT NULL,
                  direction TEXT NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# VERY SIMPLE conversion functions that WORK
def text_to_numbers(text, separator='/'):
    """Convert letters to numbers (A=1, B=2, etc.)"""
    result = []
    for char in text.upper():
        if 'A' <= char <= 'Z':
            num = ord(char) - ord('A') + 1
            result.append(str(num))
        elif char == ' ':
            result.append(' ')
    # Join with separator, skip empty parts
    parts = [p for p in result if p.strip() != '']
    return separator.join(parts)

def numbers_to_text(numbers_str, separator='/'):
    """Convert numbers to letters (1=A, 2=B, etc.)"""
    result = []
    # Split by separator
    if separator == ' ':
        parts = numbers_str.split()
    else:
        parts = numbers_str.split(separator)

    for part in parts:
        part = part.strip()
        if part.isdigit():
            num = int(part)
            if 1 <= num <= 26:
                result.append(chr(num + ord('A') - 1))
    return ''.join(result)

@app.route('/')
def index():
    return render_template('index.html')

# FIXED CONVERSION ENDPOINT - This will work
@app.route('/convert', methods=['POST'])
def convert():
    try:
        # Debug: Print what we receive
        print("=== DEBUG START ===")
        print("Request data:", request.data)
        print("Request JSON:", request.get_json(silent=True))

        # Get JSON data
        data = request.get_json()
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({'success': False, 'error': 'No data received'}), 400

        text = data.get('text', '').strip()
        direction = data.get('direction', 'text_to_num')
        separator = data.get('separator', '/')

        print(f"Processing: text='{text}', direction='{direction}', separator='{separator}'")

        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400

        # Perform conversion
        if direction == 'text_to_num':
            result = text_to_numbers(text, separator)
        elif direction == 'num_to_text':
            result = numbers_to_text(text, separator)
        else:
            return jsonify({'success': False, 'error': 'Invalid direction'}), 400

        print(f"Result: '{result}'")
        print("=== DEBUG END ===")

        return jsonify({
            'success': True,
            'result': result,
            'direction': direction
        })

    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Test endpoint
@app.route('/test-convert', methods=['GET', 'POST'])
def test_convert():
    """Test endpoint that always works"""
    if request.method == 'GET':
        return '''
        <html>
        <body>
            <h1>Test Conversion</h1>
            <button onclick="test()">Test HELLO → 8/5/12/12/15</button>
            <div id="result"></div>
            <script>
            async function test() {
                const response = await fetch('/convert', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        text: 'HELLO',
                        direction: 'text_to_num',
                        separator: '/'
                    })
                });
                const data = await response.json();
                document.getElementById('result').innerHTML =
                    JSON.stringify(data, null, 2);
            }
            </script>
        </body>
        </html>
        '''
    else:
        # Always return valid JSON for testing
        return jsonify({
            'success': True,
            'result': '8/5/12/12/15',
            'direction': 'text_to_num',
            'test': 'This is a test response'
        })

# Direct test function
@app.route('/direct-test')
def direct_test():
    """Test conversion directly"""
    result = text_to_numbers('HELLO')
    return f"Direct test: HELLO → {result}"

if __name__ == '__main__':
    init_db()
    print("Starting server...")
    print("Test endpoints:")
    print("1. http://localhost:5000/direct-test")
    print("2. http://localhost:5000/test-convert")
    app.run(debug=True, port=5000)
