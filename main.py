from flask import Flask, request, render_template_string
import requests
import json
import base64
from datetime import datetime
import time

app = Flask(__name__)

# HTML Template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Token Checker</title>
    <style>
        body { font-family: Arial; background: #f0f0f0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 5px; }
        .file-upload { margin: 20px 0; }
        .submit-btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .submit-btn:disabled { background: #ccc; }
        .results { margin-top: 20px; }
        .token-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .token-valid { background: #d4edda; }
        .token-invalid { background: #f8d7da; }
        .stats { display: flex; gap: 15px; margin: 15px 0; }
        .stat-card { padding: 10px; border-radius: 5px; text-align: center; flex: 1; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Token Checker</h1>
        
        <form method="post" enctype="multipart/form-data">
            <div class="file-upload">
                <input type="file" name="tokenFile" accept=".txt" required>
            </div>
            <button class="submit-btn" type="submit">Check Tokens</button>
        </form>
        
        {% if results %}
        <div class="results">
            <div class="stats">
                <div class="stat-card" style="background:#e3f2fd;">Total: {{ results.total }}</div>
                <div class="stat-card" style="background:#e8f5e8;">Valid: {{ results.valid }}</div>
                <div class="stat-card" style="background:#ffebee;">Invalid: {{ results.invalid }}</div>
            </div>
            
            {% for token_data in results.tokens %}
            <div class="token-card {% if token_data.valid %}token-valid{% else %}token-invalid{% endif %}">
                <strong>Token:</strong> {{ token_data.token[:50] }}...<br>
                {% if token_data.valid %}
                    <strong>Name:</strong> {{ token_data.user_info.name }}<br>
                    <strong>ID:</strong> {{ token_data.user_info.id }}<br>
                    <strong>Groups:</strong> {{ token_data.groups|length }}
                {% else %}
                    <strong>Error:</strong> {{ token_data.error }}
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def get_user_groups(access_token, user_id):
    try:
        groups_url = f"https://graph.facebook.com/v19.0/{user_id}/groups"
        params = {
            'access_token': access_token,
            'fields': 'id,name',
            'limit': '100'
        }
        response = requests.get(groups_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        return []
    except:
        return []

def get_token_details_with_groups(access_token):
    try:
        user_url = "https://graph.facebook.com/me"
        user_params = {
            'access_token': access_token,
            'fields': 'id,name'
        }
        user_response = requests.get(user_url, params=user_params, timeout=10).json()
        
        if "id" in user_response:
            user_data = {
                'id': user_response.get('id', 'N/A'),
                'name': user_response.get('name', 'N/A')
            }
            
            groups = get_user_groups(access_token, user_data['id'])
            
            return {
                'valid': True,
                'user_info': user_data,
                'groups': groups
            }
        else:
            return {
                'valid': False,
                'error': user_response.get('error', {}).get('message', 'Invalid token')
            }
    except Exception as e:
        return {
            'valid': False,
            'error': f'Error: {str(e)}'
        }

def process_multiple_tokens(tokens_list):
    results = {
        'total': len(tokens_list),
        'valid': 0,
        'invalid': 0,
        'tokens': []
    }
    
    for token in tokens_list:
        token = token.strip()
        if not token:
            continue
            
        token_data = get_token_details_with_groups(token)
        token_data['token'] = token
        
        if token_data['valid']:
            results['valid'] += 1
        else:
            results['invalid'] += 1
            
        results['tokens'].append(token_data)
    
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    
    if request.method == "POST":
        if 'tokenFile' not in request.files:
            return "No file uploaded", 400
            
        file = request.files['tokenFile']
        if file.filename == '':
            return "No file selected", 400
            
        if file and file.filename.endswith('.txt'):
            try:
                tokens_content = file.stream.read().decode('utf-8')
                tokens_list = [token.strip() for token in tokens_content.split('\n') if token.strip()]
                
                if not tokens_list:
                    return "No tokens found in file", 400
                
                results = process_multiple_tokens(tokens_list)
                
            except Exception as e:
                return f"Error: {str(e)}", 500
    
    return render_template_string(html_template, results=results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
