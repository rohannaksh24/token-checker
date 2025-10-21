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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 99H9N MULTI TOKEN MASTER 🔥</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            font-family: 'Rajdhani', sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .container {
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            border: 2px solid #00ffff;
            border-radius: 20px;
            padding: 40px 30px;
            width: 100%;
            max-width: 95%;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.3),
                        inset 0 0 20px rgba(0, 255, 255, 0.1);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.1), transparent);
            animation: shine 3s linear infinite;
        }
        
        @keyframes shine {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .header {
            margin-bottom: 30px;
            position: relative;
            z-index: 2;
        }
        
        .title {
            font-family: 'Orbitron', monospace;
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
            margin-bottom: 10px;
            letter-spacing: 2px;
        }
        
        .subtitle {
            color: #888;
            font-size: 1.1rem;
            font-weight: 300;
            letter-spacing: 1px;
        }
        
        .upload-section {
            margin-bottom: 30px;
            position: relative;
            z-index: 2;
        }
        
        .file-upload {
            background: rgba(0, 255, 255, 0.1);
            border: 2px dashed #00ffff;
            border-radius: 15px;
            padding: 40px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        
        .file-upload:hover {
            background: rgba(0, 255, 255, 0.2);
            border-color: #ff00ff;
        }
        
        .file-input {
            display: none;
        }
        
        .submit-btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(45deg, #ff00ff, #00ffff);
            border: none;
            border-radius: 12px;
            color: #000;
            font-size: 1.3rem;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 2px;
            position: relative;
            overflow: hidden;
            margin-top: 20px;
        }
        
        .submit-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(255, 0, 255, 0.4);
        }
        
        .submit-btn:disabled {
            background: #666;
            cursor: not-allowed;
            transform: none;
        }
        
        .submit-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            transition: 0.5s;
        }
        
        .submit-btn:hover:not(:disabled)::before {
            left: 100%;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .spinner {
            border: 4px solid rgba(0, 255, 255, 0.3);
            border-radius: 50%;
            border-top: 4px solid #00ffff;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .results-section {
            margin-top: 30px;
            position: relative;
            z-index: 2;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .stat-card {
            background: rgba(0, 255, 255, 0.1);
            border: 2px solid #00ffff;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }
        
        .stat-number {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            font-weight: 900;
            margin-bottom: 5px;
        }
        
        .stat-total { color: #00ffff; }
        .stat-valid { color: #00ff00; }
        .stat-invalid { color: #ff0000; }
        .stat-groups { color: #ff00ff; }
        
        .stat-label {
            color: #888;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .token-results {
            max-height: 600px;
            overflow-y: auto;
            margin-top: 20px;
        }
        
        .token-card {
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            text-align: left;
        }
        
        .token-valid {
            border-color: #00ff00;
            background: rgba(0, 255, 0, 0.1);
        }
        
        .token-invalid {
            border-color: #ff0000;
            background: rgba(255, 0, 0, 0.1);
        }
        
        .token-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .token-status {
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 1.1rem;
            padding: 5px 15px;
            border-radius: 20px;
        }
        
        .status-valid {
            background: rgba(0, 255, 0, 0.2);
            color: #00ff00;
        }
        
        .status-invalid {
            background: rgba(255, 0, 0, 0.2);
            color: #ff0000;
        }
        
        .token-preview {
            color: #888;
            font-family: monospace;
            font-size: 0.9rem;
        }
        
        .user-info {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 10px 20px;
            margin-bottom: 15px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }
        
        .info-label {
            color: #888;
            font-weight: 300;
        }
        
        .info-value {
            color: #00ffff;
            font-weight: 600;
            word-break: break-all;
        }
        
        .groups-section {
            margin-top: 15px;
        }
        
        .groups-title {
            color: #ff00ff;
            font-weight: 700;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }
        
        .groups-list {
            max-height: 200px;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 8px;
            padding: 10px;
        }
        
        .group-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 12px;
            margin: 5px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 6px;
            border-left: 3px solid #ff00ff;
        }
        
        .group-name {
            color: #00ffff;
            font-weight: 500;
        }
        
        .group-id {
            color: #888;
            font-family: monospace;
            font-size: 0.8rem;
        }
        
        .no-groups {
            color: #888;
            text-align: center;
            padding: 20px;
            font-style: italic;
        }
        
        .error-message {
            color: #ff0000;
            background: rgba(255, 0, 0, 0.1);
            border: 1px solid #ff0000;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            text-align: left;
        }
        
        .footer {
            margin-top: 40px;
            position: relative;
            z-index: 2;
        }
        
        .footer-text {
            color: #888;
            font-size: 0.9rem;
            font-weight: 300;
            letter-spacing: 1px;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        }
        
        .glow {
            text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff;
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        
        .copy-btn {
            background: rgba(0, 255, 255, 0.2);
            border: 1px solid #00ffff;
            color: #00ffff;
            padding: 8px 15px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
            margin-left: 10px;
            transition: all 0.3s ease;
        }
        
        .copy-btn:hover {
            background: rgba(0, 255, 255, 0.4);
        }
        
        .action-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .action-btn {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-valid {
            background: rgba(0, 255, 0, 0.2);
            color: #00ff00;
            border: 1px solid #00ff00;
        }
        
        .btn-invalid {
            background: rgba(255, 0, 0, 0.2);
            color: #ff0000;
            border: 1px solid #ff0000;
        }
        
        .btn-all {
            background: rgba(0, 255, 255, 0.2);
            color: #00ffff;
            border: 1px solid #00ffff;
        }
    </style>
    <script>
        function handleFileSelect(event) {
            const file = event.target.files[0];
            const fileName = document.getElementById('fileName');
            const submitBtn = document.getElementById('submitBtn');
            
            if (file) {
                if (file.name.endsWith('.txt')) {
                    fileName.textContent = `📁 Selected: ${file.name}`;
                    fileName.style.color = '#00ff00';
                    submitBtn.disabled = false;
                } else {
                    fileName.textContent = '❌ Please select a .txt file only!';
                    fileName.style.color = '#ff0000';
                    submitBtn.disabled = true;
                }
            }
        }
        
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('submitBtn').innerHTML = '🔍 SCANNING TOKENS...';
        }
        
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                alert('✅ Copied to clipboard!');
            }).catch(function(err) {
                alert('❌ Copy failed: ' + err);
            });
        }
        
        function copyValidTokens() {
            const validTokens = [];
            document.querySelectorAll('.token-valid .token-preview').forEach(el => {
                validTokens.push(el.textContent);
            });
            copyToClipboard(validTokens.join('\\n'));
        }
        
        function copyInvalidTokens() {
            const invalidTokens = [];
            document.querySelectorAll('.token-invalid .token-preview').forEach(el => {
                invalidTokens.push(el.textContent);
            });
            copyToClipboard(invalidTokens.join('\\n'));
        }
        
        function copyAllTokens() {
            const allTokens = [];
            document.querySelectorAll('.token-preview').forEach(el => {
                allTokens.push(el.textContent);
            });
            copyToClipboard(allTokens.join('\\n'));
        }
    </script>
</head>
<body>

<div class="container">
    <div class="header">
        <h1 class="title pulse">🔥 99H9N MULTI TOKEN MASTER 🔥</h1>
        <p class="subtitle">BULK TOKEN VALIDATOR WITH GROUP INFORMATION</p>
    </div>
    
    <form method="post" enctype="multipart/form-data" onsubmit="showLoading()">
        <div class="upload-section">
            <label class="file-upload" for="tokenFile">
                <div style="color: #00ffff; font-size: 1.2rem; font-weight: 700; margin-bottom: 10px;">
                    📁 UPLOAD TOKENS FILE
                </div>
                <div style="color: #888; font-size: 0.9rem;">
                    Click to upload .txt file containing Facebook tokens<br>
                    One token per line
                </div>
                <input type="file" id="tokenFile" name="tokenFile" class="file-input" accept=".txt" required onchange="handleFileSelect(event)">
            </label>
            <div id="fileName" style="color: #888; font-size: 0.9rem; margin-top: 10px;">
                No file selected
            </div>
        </div>
        
        <button class="submit-btn" id="submitBtn" type="submit" disabled>
            🚀 START BULK TOKEN SCAN
        </button>
    </form>
    
    <div class="loading" id="loading">
        <div class="spinner"></div>
        <p style="color: #00ffff; margin-top: 15px; font-size: 1.1rem;">
            🔍 Scanning Tokens & Fetching Group Information...
        </p>
        <p style="color: #888; margin-top: 5px;">
            This may take a few minutes depending on the number of tokens
        </p>
    </div>
    
    {% if results %}
    <div class="results-section">
        <!-- Statistics -->
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number stat-total">{{ results.total }}</div>
                <div class="stat-label">Total Tokens</div>
            </div>
            <div class="stat-card">
                <div class="stat-number stat-valid">{{ results.valid }}</div>
                <div class="stat-label">Valid Tokens</div>
            </div>
            <div class="stat-card">
                <div class="stat-number stat-invalid">{{ results.invalid }}</div>
                <div class="stat-label">Invalid Tokens</div>
            </div>
            <div class="stat-card">
                <div class="stat-number stat-groups">{{ results.total_groups }}</div>
                <div class="stat-label">Total Groups</div>
            </div>
        </div>
        
        <!-- Action Buttons -->
        <div class="action-buttons">
            <button class="action-btn btn-valid" onclick="copyValidTokens()">
                📋 Copy Valid Tokens
            </button>
            <button class="action-btn btn-invalid" onclick="copyInvalidTokens()">
                📋 Copy Invalid Tokens
            </button>
            <button class="action-btn btn-all" onclick="copyAllTokens()">
                📋 Copy All Tokens
            </button>
        </div>
        
        <!-- Token Results -->
        <div class="token-results">
            {% for token_data in results.tokens %}
            <div class="token-card {{ 'token-valid' if token_data.valid else 'token-invalid' }}">
                <div class="token-header">
                    <div class="token-status {{ 'status-valid' if token_data.valid else 'status-invalid' }}">
                        {% if token_data.valid %}✅ VALID TOKEN{% else %}❌ INVALID TOKEN{% endif %}
                    </div>
                    <div class="token-preview">{{ token_data.token[:50] }}...</div>
                </div>
                
                {% if token_data.valid %}
                <!-- User Information -->
                <div class="user-info">
                    <div class="info-label">👤 Name:</div>
                    <div class="info-value">{{ token_data.user_info.name }}</div>
                    
                    <div class="info-label">🆔 User ID:</div>
                    <div class="info-value">{{ token_data.user_info.id }}</div>
                    
                    {% if token_data.user_info.email and token_data.user_info.email != 'Not Available' %}
                    <div class="info-label">📧 Email:</div>
                    <div class="info-value">{{ token_data.user_info.email }}</div>
                    {% endif %}
                    
                    <div class="info-label">🔐 Token Type:</div>
                    <div class="info-value">{{ token_data.user_info.token_type }}</div>
                    
                    <div class="info-label">⏰ Expires:</div>
                    <div class="info-value" style="color: {% if token_data.user_info.is_expired %}#ff0000{% else %}#00ff00{% endif %};">
                        {{ token_data.user_info.expires_at }}
                    </div>
                </div>
                
                <!-- Groups Information -->
                <div class="groups-section">
                    <div class="groups-title">
                        👥 JOINED GROUPS ({{ token_data.groups|length }})
                    </div>
                    {% if token_data.groups %}
                    <div class="groups-list">
                        {% for group in token_data.groups %}
                        <div class="group-item">
                            <div class="group-name">{{ group.name }}</div>
                            <div class="group-id">ID: {{ group.id }}</div>
                        </div>
                        {% endfor %}
                    </div>
                    {% else %}
                    <div class="no-groups">
                        No groups found or access denied
                    </div>
                    {% endif %}
                </div>
                {% else %}
                <!-- Error Message for Invalid Tokens -->
                <div class="error-message">
                    <strong>Error:</strong> {{ token_data.error }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    
    <div class="footer">
        <p class="footer-text glow">⚡ POWERED BY 99H9N H3R3 ⚡</p>
        <p class="footer-text">ADVANCED BULK TOKEN ANALYZER</p>
    </div>
</div>

<script>
    // Add some cool effects
    const container = document.querySelector('.container');
    
    // File upload drag and drop
    const fileUpload = document.querySelector('.file-upload');
    const fileInput = document.getElementById('tokenFile');
    
    fileUpload.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUpload.style.background = 'rgba(0, 255, 255, 0.2)';
        fileUpload.style.borderColor = '#ff00ff';
    });
    
    fileUpload.addEventListener('dragleave', () => {
        fileUpload.style.background = 'rgba(0, 255, 255, 0.1)';
        fileUpload.style.borderColor = '#00ffff';
    });
    
    fileUpload.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUpload.style.background = 'rgba(0, 255, 255, 0.1)';
        fileUpload.style.borderColor = '#00ffff';
        
        if (e.dataTransfer.files.length) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect({ target: fileInput });
        }
    });
</script>

</body>
</html>
"""

def get_user_groups(access_token, user_id):
    """Get groups that the user has joined"""
    try:
        groups_url = f"https://graph.facebook.com/v19.0/{user_id}/groups"
        params = {
            'access_token': access_token,
            'fields': 'id,name,privacy,member_count',
            'limit': '100'
        }
        response = requests.get(groups_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            groups = data.get('data', [])
            
            # Format groups data
            formatted_groups = []
            for group in groups:
                formatted_groups.append({
                    'id': group.get('id', 'N/A'),
                    'name': group.get('name', 'N/A'),
                    'privacy': group.get('privacy', 'N/A'),
                    'member_count': group.get('member_count', 0)
                })
            
            return formatted_groups
        else:
            return []
            
    except Exception as e:
        print(f"Error fetching groups: {e}")
        return []

def get_token_details_with_groups(access_token):
    """Get detailed token information including groups"""
    try:
        # Get basic user info
        user_url = "https://graph.facebook.com/me"
        user_params = {
            'access_token': access_token,
            'fields': 'id,name,email,first_name,last_name'
        }
        user_response = requests.get(user_url, params=user_params, timeout=10).json()
        
        # Get token debug information
        debug_url = "https://graph.facebook.com/debug_token"
        debug_params = {
            'input_token': access_token,
            'access_token': access_token
        }
        debug_response = requests.get(debug_url, params=debug_params, timeout=10).json()
        
        user_data = {}
        groups = []
        
        if "id" in user_response:
            # Basic user information
            user_data = {
                'id': user_response.get('id', 'N/A'),
                'name': user_response.get('name', 'N/A'),
                'email': user_response.get('email', 'Not Available'),
                'first_name': user_response.get('first_name', 'N/A'),
                'last_name': user_response.get('last_name', 'N/A'),
                'is_valid': True
            }
            
            # Token debug information
            if 'data' in debug_response:
                debug_data = debug_response['data']
                expires_at = debug_data.get('expires_at', 0)
                is_expired = False
                
                if expires_at > 0:
                    current_time = int(time.time())
                    is_expired = expires_at < current_time
                    expiry_date = datetime.fromtimestamp(expires_at)
                    expires_at_str = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    expires_at_str = "Never"
                
                user_data.update({
                    'app_id': debug_data.get('app_id', 'N/A'),
                    'token_type': debug_data.get('type', 'N/A'),
                    'scopes': ', '.join(debug_data.get('scopes', [])),
                    'expires_at': expires_at_str,
                    'is_expired': is_expired
                })
            
            # Get user's groups
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
    """Process multiple tokens and return comprehensive results"""
    results = {
        'total': len(tokens_list),
        'valid': 0,
        'invalid': 0,
        'total_groups': 0,
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
            results['total_groups'] += len(token_data['groups'])
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
                # Read tokens from file
                tokens_content = file.stream.read().decode('utf-8')
                tokens_list = [token.strip() for token in tokens_content.split('\n') if token.strip()]
                
                if not tokens_list:
                    return "No tokens found in file", 400
                
                # Process tokens
                results = process_multiple_tokens(tokens_list)
                
            except Exception as e:
                return f"Error processing file: {str(e)}", 500
    
    return render_template_string(html_template, results=results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
