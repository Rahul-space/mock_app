import threading
import webbrowser
import os
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from flask import Flask, render_template, request, jsonify

# ==========================================
# FLASK WEB SERVER
# ==========================================
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, 
            template_folder=os.path.join(base_dir, 'templates'), 
            static_folder=os.path.join(base_dir, 'static'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    # Mock bot response
    bot_reply = f"Mock Policy Bot received: '{user_msg}'. Please consult the enterprise IT handbook."
    return jsonify({"reply": bot_reply})

def run_flask():
    # Runs quietly on localhost port 5050
    app.run(host='127.0.0.1', port=5050, debug=False, use_reloader=False)

# ==========================================
# SYSTEM TRAY
# ==========================================
def create_image():
    # Dynamically generate a simple blue icon for the system tray
    image = Image.new('RGB', (64, 64), color=(0, 122, 204))
    d = ImageDraw.Draw(image)
    d.text((15, 25), "BOT", fill=(255, 255, 255))
    return image

def open_browser(icon, item):
    webbrowser.open("http://127.0.0.1:5050")

def exit_app(icon, item):
    icon.stop()
    os._exit(0) # Hard exit to kill both the tray and the Flask thread

def run_tray():
    image = create_image()
    menu = (
        item('Open Chatbot', open_browser, default=True),
        item('Exit', exit_app)
    )
    icon = pystray.Icon("PolicyChatbot", image, "Enterprise Policy Bot", menu)
    icon.run()

if __name__ == "__main__":
    # 1. Start Flask in a background daemon thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # 2. Start System Tray in the main thread (Required by Windows)
    run_tray()