from flask import Flask, render_template, request, jsonify, make_response, redirect

# Flask ko bata rahe hain ki HTML files 'templates' folder mein hain
app = Flask(__name__, template_folder='../templates')

# --- CONFIGURATION ---
ADMIN_PASS = "admin123"  # Yahan apna password set karein

# Note: Vercel par restart hone par ye keys gayab ho sakti hain (Database use karein better stability ke liye)
generated_keys = [] 

# --- PAGE ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    # Agar pehle se login hai to sidha admin panel bhejo
    if request.cookies.get('logged_in') == 'true':
        return redirect('/admin')
    return render_template('login.html')

@app.route('/admin')
def admin_panel():
    # Check karein ki banda login hai ya nahi
    if request.cookies.get('logged_in') == 'true':
        return render_template('admin.html')
    return redirect('/login')

# --- API LOGIC (Javascript se connect karne ke liye) ---

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    if data.get('pass') == ADMIN_PASS:
        resp = make_response(jsonify({"status": "success"}))
        # Cookie set kar rahe hain 24 ghante ke liye
        resp.set_cookie('logged_in', 'true', max_age=86400)
        return resp
    return jsonify({"status": "fail"}), 401

@app.route('/api/generate', methods=['POST'])
def api_generate():
    if request.cookies.get('logged_in') != 'true':
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    import random, string
    data = request.json
    duration = data.get('duration', '1h')
    
    # Random Key Banao
    rand_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    new_key = f"EXE-{rand_str}-{duration.upper()}"
    
    generated_keys.append(new_key)
    return jsonify({"status": "success", "key": new_key})

@app.route('/api/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.set_cookie('logged_in', '', expires=0)
    return resp

# Vercel ke liye zaroori line
if __name__ == '__main__':
    app.run(debug=True)

