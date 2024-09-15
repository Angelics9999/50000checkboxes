from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('checkboxes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Retrieve the current state of checkboxes from the database
def get_checkbox_state():
    conn = get_db_connection()
    checkboxes = conn.execute('SELECT id, checked FROM checkboxes').fetchall()
    conn.close()
    return [checkbox['checked'] for checkbox in checkboxes]

# Update a specific checkbox state in the database
def update_checkbox_state(checkbox_id, checked):
    conn = get_db_connection()
    conn.execute('UPDATE checkboxes SET checked = ? WHERE id = ?', (checked, checkbox_id))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('checkbox_click')
def handle_checkbox_click(data):
    checkbox_id = data['id']
    checked = data['checked']

    # Update the database with the new checkbox state
    update_checkbox_state(checkbox_id, checked)

    # Notify all connected clients of the update
    emit('update_checkbox', data, broadcast=True)

    # Check if all checkboxes are selected
    checkbox_state = get_checkbox_state()
    if all(checkbox_state):
        emit('all_checked', broadcast=True)

@app.route('/state')
def get_state():
    checkbox_state = get_checkbox_state()
    return jsonify(checkbox_state)

if __name__ == '__main__':
    socketio.run(app, host='0.25', port=5000, debug=True)
