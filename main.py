from flask import Flask, request, render_template_string
import requests
import json
import time

app = Flask(__name__)

# HTML Template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 AAHAN TOKEN CHECKER 🔥</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            font-family: 'Rajdhani', sans-serif;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ffff;
            border-radius: 15px;
            padding: 30px;
            max-width: 1200px;
            margin: 0 auto;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(0, 255, 255, 0.3);
        }
        
        .title {
            font-family: 'Orbitron', monospace;
            font-size: 2.8rem;
            font-weight: 900;
            background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        }
        
        .subtitle {
            color: #888;
            font-size: 1.2rem;
            font-weight: 300;
        }
        
        .mode-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            background: rgba(0, 255, 255, 0.1);
            padding: 10px;
            border-radius: 10px;
        }
        
        .mode-btn {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 8px;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.1);
            color: #888;
        }
        
        .mode-btn.active {
            background: linear-gradient(45deg, #ff00ff, #00ffff);
            color: #000;
        }
        
        .mode-btn:hover {
            transform: translateY(-2px);
        }
        
        .mode-section {
            display: none;
        }
        
        .mode-section.active {
            display: block;
        }
        
        .single-token-section {
            background: rgba(0, 255, 255, 0.1);
            border: 2px dashed #00ffff;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
        }
        
        .token-input {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid #00ffff;
            border-radius: 8px;
            color: white;
            font-family: monospace;
            font-size: 1rem;
            margin-bottom: 15px;
            resize: vertical;
            min-height: 100px;
        }
        
        .token-input::placeholder {
            color: #888;
        }
        
        .upload-section {
            background: rgba(0, 255, 255, 0.1);
            border: 2px dashed #00ffff;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        
        .upload-section:hover {
            background: rgba(0, 255, 255, 0.2);
        }
        
        .file-input {
            margin: 15px 0;
        }
        
        .submit-btn {
            background: linear-gradient(45deg, #ff00ff, #00ffff);
            border: none;
            border-radius: 8px;
            color: #000;
            padding: 15px 30px;
            font-size: 1.2rem;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 0, 255, 0.4);
        }
        
        .submit-btn:disabled {
            background: #666;
            cursor: not-allowed;
            transform: none;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 25px 0;
        }
        
        .stat-card {
            background: rgba(0, 255, 255, 0.1);
            border: 2px solid;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        
        .stat-total { border-color: #00ffff; }
        .stat-valid { border-color: #00ff00; }
        .stat-invalid { border-color: #ff0000; }
        .stat-groups { border-color: #ff00ff; }
        
        .stat-number {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            font-weight: 900;
            margin-bottom: 5px;
        }
        
        .stat-total .stat-number { color: #00ffff; }
        .stat-valid .stat-number { color: #00ff00; }
        .stat-invalid .stat-number { color: #ff0000; }
        .stat-groups .stat-number { color: #ff00ff; }
        
        .token-results {
            margin-top: 20px;
        }
        
        .token-card {
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
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
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
        }
        
        .status-valid {
            background: rgba(0, 255, 0, 0.2);
            color: #00ff00;
        }
        
        .status-invalid {
            background: rgba(255, 0, 0, 0.2);
            color: #ff0000;
        }
        
        .user-profile {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 15px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        
        .profile-pic {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: 3px solid #00ffff;
            object-fit: cover;
        }
        
        .profile-info {
            flex: 1;
        }
        
        .profile-name {
            font-size: 1.4rem;
            font-weight: 700;
            color: #00ffff;
            margin-bottom: 5px;
        }
        
        .profile-id {
            color: #888;
            font-family: monospace;
            margin-bottom: 5px;
        }
        
        .profile-link a {
            color: #ff00ff;
            text-decoration: none;
        }
        
        .profile-link a:hover {
            text-decoration: underline;
        }
        
        .user-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-bottom: 15px;
        }
        
        .detail-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 5px;
        }
        
        .detail-label {
            color: #888;
            font-size: 0.9rem;
        }
        
        .detail-value {
            color: #00ffff;
            font-weight: 600;
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
        
        .groups-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 10px;
            max-height: 300px;
            overflow-y: auto;
            padding: 10px;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 8px;
        }
        
        .group-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid #ff00ff;
        }
        
        .group-name {
            color: #00ffff;
            font-weight: 500;
            margin-bottom: 5px;
        }
        
        .group-id {
            color: #888;
            font-family: monospace;
            font-size: 0.8rem;
        }
        
        .loading {
            text-align: center;
            padding: 30px;
            color: #00ffff;
            display: none;
        }
        
        .spinner {
            border: 4px solid rgba(0, 255, 255, 0.3);
            border-radius: 50%;
            border-top: 4px solid #00ffff;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(0, 255, 255, 0.3);
            color: #888;
        }
        
        .glow {
            text-shadow: 0 0 10px #00ffff;
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
        
        .action-btn:hover {
            transform: translateY(-2px);
        }
    </style>
    <script>
        function switchMode(mode) {
            // Update buttons
            document.querySelectorAll('.mode-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Update sections
            document.querySelectorAll('.mode-section').forEach(section => {
                section.classList.remove('active');
            });
            document.getElementById(mode + '-mode').classList.add('active');
            
            // Update form action
            document.getElementById('main-form').action = '/' + (mode === 'single' ? '?mode=single' : '?mode=multi');
        }
        
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.querySelector('.submit-btn').disabled = true;
            document.querySelector('.submit-btn').innerHTML = '🔍 SCANNING TOKENS...';
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
            copyToClipboard(validTokens.join('\n'));
        }
        
        function copyInvalidTokens() {
            const invalidTokens = [];
            document.querySelectorAll('.token-invalid .token-preview').forEach(el => {
                invalidTokens.push(el.textContent);
            });
            copyToClipboard(invalidTokens.join('\n'));
        }
        
        function copyAllTokens() {
            const allTokens = [];
            document.querySelectorAll('.token-preview').forEach(el => {
                allTokens.push(el.textContent);
            });
            copyToClipboard(allTokens.join('\n'));
        }
        
        function handleFileSelect(event) {
            const file = event.target.files[0];
            const fileName = document.getElementById('fileName');
            const submitBtn = document.querySelector('.submit-btn');
            
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
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🔥 AAHAN TOKEN CHECKER 🔥</h1>
            <p class="subtitle">PREMIUM FACEBOOK TOKEN VALIDATOR WITH PROFILE ANALYSIS</p>
        </div>
        
        <!-- Mode Selector -->
        <div class="mode-selector">
            <button class="mode-btn active" onclick="switchMode('single')">🔍 SINGLE TOKEN</button>
            <button class="mode-btn" onclick="switchMode('multi')">📁 MULTI TOKENS</button>
        </div>
        
        <form method="post" enctype="multipart/form-data" id="main-form" onsubmit="showLoading()">
            <!-- Single Token Mode -->
            <div class="mode-section active" id="single-mode">
                <div class="single-token-section">
                    <h3 style="color: #00ffff; margin-bottom: 15px;">🔍 CHECK SINGLE TOKEN</h3>
                    <textarea 
                        class="token-input" 
                        name="singleToken" 
                        placeholder="Paste your Facebook token here...&#10;Example: EAABwzLixnjYBO...&#10;&#10;Or paste multiple tokens (one per line) for quick check"
                        rows="6"
                    >{{ single_token if single_token else '' }}</textarea>
                    <p style="color: #888; font-size: 0.9rem; text-align: center;">
                        Paste single token or multiple tokens (one per line)
                    </p>
                </div>
            </div>
            
            <!-- Multi Token Mode -->
            <div class="mode-section" id="multi-mode">
                <div class="upload-section">
                    <h3 style="color: #00ffff; margin-bottom: 15px;">📁 UPLOAD TOKENS FILE</h3>
                    <input class="file-input" type="file" name="tokenFile" accept=".txt" onchange="handleFileSelect(event)">
                    <div id="fileName" style="color: #888; font-size: 0.9rem; margin-top: 10px;">
                        No file selected
                    </div>
                    <p style="color: #888; font-size: 0.9rem;">Upload .txt file with one token per line</p>
                </div>
            </div>
            
            <button class="submit-btn" type="submit">
                🚀 START VALIDATION
            </button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 15px; font-size: 1.1rem;">
                🔍 Scanning Tokens & Fetching Information...
            </p>
            <p style="color: #888; margin-top: 5px;">
                This may take a few moments...
            </p>
        </div>
        
        {% if results %}
        <div class="stats">
            <div class="stat-card stat-total">
                <div class="stat-number">{{ results.total }}</div>
                <div>Total Tokens</div>
            </div>
            <div class="stat-card stat-valid">
                <div class="stat-number">{{ results.valid }}</div>
                <div>Valid Tokens</div>
            </div>
            <div class="stat-card stat-invalid">
                <div class="stat-number">{{ results.invalid }}</div>
                <div>Invalid Tokens</div>
            </div>
            <div class="stat-card stat-groups">
                <div class="stat-number">{{ results.total_groups }}</div>
                <div>Total Groups</div>
            </div>
        </div>
        
        <!-- Action Buttons -->
        {% if results.total > 1 %}
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
        {% endif %}
        
        <div class="token-results">
            {% for token_data in results.tokens %}
            <div class="token-card {% if token_data.valid %}token-valid{% else %}token-invalid{% endif %}">
                <div class="token-header">
                    <div class="token-status {% if token_data.valid %}status-valid{% else %}status-invalid{% endif %}">
                        {% if token_data.valid %}✅ VALID TOKEN{% else %}❌ INVALID TOKEN{% endif %}
                    </div>
                    <div class="token-preview" style="color: #888; font-family: monospace;">{{ token_data.token[:60] }}...</div>
                </div>
                
                {% if token_data.valid %}
                <!-- User Profile Section -->
                <div class="user-profile">
                    <img src="{{ token_data.user_info.profile_pic }}" alt="Profile" class="profile-pic" 
                         onerror="this.src='https://graph.facebook.com/{{ token_data.user_info.id }}/picture?type=large'">
                    <div class="profile-info">
                        <div class="profile-name">{{ token_data.user_info.name }}</div>
                        <div class="profile-id">ID: {{ token_data.user_info.id }}</div>
                        <div class="profile-link">
                            <a href="https://facebook.com/{{ token_data.user_info.id }}" target="_blank">
                                🔗 View Facebook Profile
                            </a>
                        </div>
                    </div>
                </div>
                
                <!-- User Details -->
                <div class="user-details">
                    <div class="detail-item">
                        <div class="detail-label">📧 Email</div>
                        <div class="detail-value">{{ token_data.user_info.email }}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">👤 First Name</div>
                        <div class="detail-value">{{ token_data.user_info.first_name }}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">👥 Last Name</div>
                        <div class="detail-value">{{ token_data.user_info.last_name }}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">🆔 User ID</div>
                        <div class="detail-value">{{ token_data.user_info.id }}</div>
                    </div>
                </div>
                
                <!-- Groups Section -->
                <div class="groups-section">
                    <div class="groups-title">
                        👥 JOINED GROUPS ({{ token_data.groups|length }})
                    </div>
                    {% if token_data.groups %}
                    <div class="groups-grid">
                        {% for group in token_data.groups %}
                        <div class="group-item">
                            <div class="group-name">{{ group.name }}</div>
                            <div class="group-id">ID: {{ group.id }}</div>
                        </div>
                        {% endfor %}
                    </div>
                    {% else %}
                    <div style="color: #888; text-align: center; padding: 20px;">
                        No groups found or access denied
                    </div>
                    {% endif %}
                </div>
                {% else %}
                <div style="color: #ff0000; background: rgba(255, 0, 0, 0.1); padding: 15px; border-radius: 5px;">
                    <strong>Error:</strong> {{ token_data.error }}
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <div class="footer">
            <p class="glow">⚡ POWERED BY AAHAN TOKEN CHECKER ⚡</p>
            <p>Advanced Facebook Token Validation System</p>
        </div>
    </div>
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
    """Get detailed token information including profile picture and groups"""
    try:
        # Get basic user info with more fields
        user_url = "https://graph.facebook.com/me"
        user_params = {
            'access_token': access_token,
            'fields': 'id,name,email,first_name,last_name,picture.type(large)'
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
            # Get profile picture URL
            profile_pic = f"https://graph.facebook.com/{user_response['id']}/picture?type=large&width=200&height=200"
            
            # Basic user information
            user_data = {
                'id': user_response.get('id', 'N/A'),
                'name': user_response.get('name', 'N/A'),
                'email': user_response.get('email', 'Not Available'),
                'first_name': user_response.get('first_name', 'N/A'),
                'last_name': user_response.get('last_name', 'N/A'),
                'profile_pic': profile_pic,
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
                    expiry_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expires_at))
                    expires_at_str = expiry_date
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
    single_token = ""
    mode = request.args.get('mode', 'single')
    
    if request.method == "POST":
        mode = request.form.get('mode', 'single')
        
        if mode == 'single':
            # Single token mode
            single_token = request.form.get('singleToken', '').strip()
            if single_token:
                tokens_list = [token.strip() for token in single_token.split('\n') if token.strip()]
                if tokens_list:
                    results = process_multiple_tokens(tokens_list)
            else:
                return "No token provided", 400
                
        else:
            # Multi token mode
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
            else:
                return "Invalid file type. Please upload .txt file", 400
    
    return render_template_string(html_template, results=results, single_token=single_token, mode=mode)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
