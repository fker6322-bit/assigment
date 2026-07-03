from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
# អនុញ្ញាត CORS ដើម្បីកុំឲ្យមានបញ្ហាពេល host
socketio = SocketIO(app, cors_allowed_origins="*")

# ទំព័រសម្រាប់ Laptop (Viewer)
@app.route('/')
def viewer():
    return render_template('viewer.html')

# ទំព័រសម្រាប់ទូរស័ព្ទ (Remote)
@app.route('/remote')
def remote():
    return render_template('remote.html')

# ទទួលសញ្ញា 'next' ពីទូរស័ព្ទ ហើយបញ្ជូនទៅ Laptop
@socketio.on('next_slide')
def handle_next():
    emit('change_slide', {'direction': 'next'}, broadcast=True)

# ទទួលសញ្ញា 'prev' ពីទូរស័ព្ទ ហើយបញ្ជូនទៅ Laptop
@socketio.on('prev_slide')
def handle_prev():
    emit('change_slide', {'direction': 'prev'}, broadcast=True)

if __name__ == '__main__':
    # ប្រើ eventlet សម្រាប់ដំណើរការ WebSocket ឲ្យរលូន
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)