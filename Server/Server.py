from gevent import monkey; monkey.patch_all()
import base64
import gevent
import os
import sentry_sdk
import sqlite3
import stat
import sys
import time
import uuid
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file, after_this_request, render_template_string
from flask_socketio import SocketIO, join_room, leave_room
from pathlib import Path
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.utils import secure_filename



def is_exe():
    script_name = os.path.realpath(sys.argv[0])
    if script_name.endswith('.exe'):
        dir_of_app = os.path.dirname(os.path.abspath(sys.argv[0]))
        env_file = os.path.join(dir_of_app, '.env')
        if not os.path.exists(env_file):
            data = '''UPLOAD_SIZE_LIMIT=100 #Upload size limit in MB
FOLDER_SIZE_LIMIT=1 #Upload folder limit in GB
FILE_AGE_LIMIT=10 #File age limit in minutes before deletion
BASE_URL=http://localhost #Base URL for the server
PORT=5000 #Port for the server. In Docker it's the host port, that is bound to 5000
TEXT_EXTENSIONS=txt,pdf #Allowed text file extensions
IMG_EXTENSIONS=png,jpg,jpeg,gif #Allowed image file extensions
ZIP_EXTENSIONS=zip,7z,rar #Allowed zip file extensions
AUDIO_EXTENSIONS=mp3,wav,ogg,flac,aac,wma,m4a #Allowed audio file extensions
VIDEO_EXTENSIONS=mp4,mkv,avi,mov,wmv,flv,webm,vob,m4v,3gp,3g2 #Allowed video file extensions
DIVERSE_EXTENSIONS=exe #Allowed diverse file extensions
'''
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(data)
            input("Please edit the .env file and restart the server...")
            sys.exit("Please edit the .env file and restart the server.")
        else:
            load_dotenv(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), '.env'))
    else:
        load_dotenv()



# Init
is_exe()
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[
        FlaskIntegration(),
    ],
    profiles_sample_rate=1.0,
    traces_sample_rate=1.0,
    environment='Server'
)

if not os.path.isdir('temp'):
    os.mkdir('temp')
os.chmod('temp', stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP)

text_extensions = os.getenv('TEXT_EXTENSIONS').split(',')
img_extensions = os.getenv('IMG_EXTENSIONS').split(',')
zip_extensions = os.getenv('ZIP_EXTENSIONS').split(',')
audio_extensions = os.getenv('AUDIO_EXTENSIONS').split(',')
video_extensions = os.getenv('VIDEO_EXTENSIONS').split(',')
diverse_extensions = os.getenv('DIVERSE_EXTENSIONS').split(',')
ALLOWED_EXTENSIONS = set(text_extensions + img_extensions + zip_extensions + audio_extensions + video_extensions + diverse_extensions)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'temp')
app.config['MAX_FOLDER_SIZE'] = 1024 * 1024 * 1024 * int(os.getenv('FOLDER_SIZE_LIMIT'))
app.config['MAX_UPLOAD_SIZE'] = 1024 * 1024 * int(os.getenv('UPLOAD_SIZE_LIMIT'))
app.config['MAX_FILE_AGE'] = int(os.getenv('FILE_AGE_LIMIT'))
socketio = SocketIO(app, cors_allowed_origins="*")

BASE_URL = os.getenv('BASE_URL')
PORT = int(os.getenv('PORT'))
URL = f'{BASE_URL}:{PORT}'

def initialise_database():
    global conn
    conn = sqlite3.connect('chat.db', check_same_thread=False)
    c = conn.cursor()
    c.executescript("""
    DROP TABLE IF EXISTS rooms;
    DROP TABLE IF EXISTS clients;
    DROP TABLE IF EXISTS connection_status;
    CREATE TABLE IF NOT EXISTS rooms (room_id TEXT, key TEXT);
    CREATE TABLE IF NOT EXISTS clients (client_id TEXT, username TEXT, room TEXT);
    CREATE TABLE IF NOT EXISTS connection_status (client_id TEXT, status TEXT);
    """)
    conn.commit()
initialise_database()




class routes():
    @app.route('/', methods=['GET'])
    def index():
        readme_path = os.path.join(os.getcwd(), 'README.md')
        print(readme_path)

        with open(os.path.join(app.static_folder, 'index.html')) as f:
            html = f.read()
        with open(readme_path) as f:
            readme = f.read()
        return render_template_string(html, readme=readme), 200

    @app.route('/upload_file', methods=['POST'])
    def upload_file():
        def __allowed_file(filename):
            return '.' in filename and \
                   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        def __folder_size(path='.'):
            total = 0
            for entry in os.scandir(path):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += __folder_size(entry.path)
            return total

        required_attributes = ['file', 'room', 'user', 'only_filename', 'filesize', 'uuid']
        for attr in required_attributes:
            if attr not in request.files and attr not in request.form:
                return jsonify({'error': f'Missing attribute'}), 400

        file = request.files['file']
        only_filename = request.form.get('only_filename')
        filesize = int(request.form.get('filesize'))
        room = request.form.get('room')
        user = request.form.get('user')
        uuid_str = request.form.get('uuid')

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 422

        current_folder_size = __folder_size(app.config['UPLOAD_FOLDER'])
        if current_folder_size + filesize > app.config['MAX_FOLDER_SIZE']:
            return jsonify({'error': 'Folder size limit reached'}), 413

        if file and __allowed_file(only_filename):
            filename = secure_filename(only_filename.strip().replace(' ', ''))
            filename_new = f'{uuid.uuid4()}{Path(filename).suffix}'
            if filesize > app.config['MAX_UPLOAD_SIZE']:
                return jsonify({'error': 'File size too large'}), 413
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename_new)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            with open(file_path, 'wb') as f:
                chunk_size = 4096
                while True:
                    chunk = file.stream.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    f.write(chunk)
            if room and user:
                socketio.emit('file', {'room': room, 'user': user, 'filename': filename, 'url': f'{URL}/get_file?filename={filename_new}', 'uuid': uuid_str}, room=room)
            return jsonify({'message': 'File uploaded successfully', 'url': f'{URL}/get_file?filename={filename_new}'}), 200
        else:
            return jsonify({'error': 'File type not allowed'}), 415

    @app.route('/get_file', methods=['GET', 'HEAD'])
    def get_file():
        filename = request.args.get('filename', '').strip()
        if filename == '':
            return jsonify({'error': 'No filename provided'}), 400
        else:
            filename = secure_filename(filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path):
                if request.method == 'HEAD':
                    return ('', 204)
                else:
                    file = open(file_path, 'rb')
                    @after_this_request
                    def unlock_file(response):
                        file.close()
                        return response
                    return send_file(file_path, as_attachment=True), 200
            else:
                return jsonify({'error': 'File not found'}), 404

    @app.route('/create_room', methods=['POST'])
    def create_room():
        with conn:
            c = conn.cursor()
            room_id = request.json.get('room_id', '').strip().replace(' ', '')
            if not 6 <= len(room_id) <= 36 or room_id == '':
                while room_id == '' or c.execute(f"SELECT 1 FROM rooms WHERE room_id = ?", (room_id,)).fetchone() is not None:
                    room_id = str(uuid.uuid4())
                key = base64.b64encode(os.urandom(32)).decode('utf-8')
                c.execute("INSERT INTO rooms (room_id, key) VALUES (?, ?)", (room_id, key,))
                conn.commit()
                return jsonify({'room_id': room_id, 'key': key}), 201
            else:
                if not 6 <= len(room_id) <= 36:
                    return jsonify({'error': 'Room ID must be between 6 and 36 characters long'}), 400
                if c.execute("SELECT 1 FROM rooms WHERE room_id = ?", (room_id,)).fetchone() is not None:
                    return jsonify({'error': 'Room already exists'}), 409
                else:
                    key = base64.b64encode(os.urandom(32)).decode('utf-8')
                    c.execute("INSERT INTO rooms (room_id, key) VALUES (?, ?)", (room_id, key,))
                    conn.commit()
                    return jsonify({'room_id': room_id, 'key': key}), 201

    @app.route('/room_exists', methods=['GET'])
    def room_exists():
        with conn:
            c = conn.cursor()
            room_id = request.args.get('room_id', '').strip().replace(' ', '')
            if room_id == '':
                return jsonify({'error': 'No room_id provided'}), 400
            else:
                room_exists = c.execute("SELECT 1 FROM rooms WHERE room_id = ?", (room_id,)).fetchone() is not None
                if room_exists:
                    key = c.execute("SELECT key FROM rooms WHERE room_id = ?", (room_id,)).fetchone()[0]
                    return jsonify({'status': 'Room exists', 'key': key}), 200
                else:
                    return jsonify({'error': 'Room not found'}), 404

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'ok'}), 200

    @app.route('/config', methods=['GET'])
    def get_config():
        return jsonify({
            'max_upload_size': app.config['MAX_UPLOAD_SIZE'],
            'text_extensions': text_extensions,
            'img_extensions': img_extensions,
            'video_extensions': video_extensions,
            'audio_extensions': audio_extensions,
            'zip_extensions': zip_extensions,
            'diverse_extensions': diverse_extensions,
            'file_age_limit': app.config['MAX_FILE_AGE']
        }), 200



class sockets():
    @socketio.on('join')
    def on_join(data):
        with conn:
            c = conn.cursor()
            username = data['username'].strip().replace(' ', '')
            room_id = data['room'].strip().replace(' ', '')

            if not 3 <= len(username) <= 20:
                return jsonify({'error': 'Username must be between 3 and 20 characters long'}), 400
            if not 6 <= len(room_id) <= 36:
                return jsonify({'error': 'Room ID must be between 6 and 36 characters long'}), 400

            # Load key from db rooms table
            c.execute("INSERT INTO clients (client_id, username, room) VALUES (?, ?, ?)",
                      (request.sid, username, room_id))
            c.execute("INSERT INTO connection_status (client_id, status) VALUES (?, ?)",
                      (request.sid, 'connected'))
            conn.commit()
            join_room(room_id)
            socketio.emit('join', {'message': f"{username} has joined the room."}, room=room_id, include_self=False)

    @socketio.on('message')
    def handle_message(data):
        message = str(data['message']).strip()
        if not message or message.isspace():
            return
        socketio.emit('message', data, room=data['room'], include_self=False)

    @socketio.on('leave')
    def on_leave(data):
        with conn:
            c = conn.cursor()
            username = data['username']
            room_id = data['room']
            leave_room(room_id)
            c.execute("UPDATE connection_status SET status = ? WHERE client_id = ?", ('disconnected', request.sid))
            try:
                conn.commit()
            except sqlite3.Error:
                pass
            socketio.emit('leave', {'message': f"{username} has left the room."}, room=room_id, include_self=False)

    @socketio.on('disconnect')
    def handle_disconnect():
        with conn:
            c = conn.cursor()
            c.execute("SELECT username, room FROM clients WHERE client_id = ?", (request.sid,))
            user_info = c.fetchone()
            if user_info:
                username, room_id = user_info
                leave_room(room_id)
                c.execute("SELECT status FROM connection_status WHERE client_id = ?", (request.sid,))
                status_info = c.fetchone()
                if status_info and status_info[0] != 'disconnected':
                    socketio.emit('disconnect', {'message': f"{username} has lost connection."}, room=room_id, include_self=False)
            c.execute("DELETE FROM clients WHERE client_id = ?", (request.sid,))
            c.execute("DELETE FROM connection_status WHERE client_id = ?", (request.sid,))
            conn.commit()

    @socketio.on('file')
    def handle_file(data):
        filename = data['file_name']
        filedata = data['file_data']
        with open(filename, 'wb') as f:
            f.write(filedata)
        print(f'File received: {filename}')



def delete_old_files():
    while True:
        now = time.time()
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        for filename in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.getctime(file_path) < now - 60 * app.config['MAX_FILE_AGE']:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to delete file {file_path}: {e}")
        gevent.sleep(15)






if __name__ == '__main__':
    os.environ['GEVENT_SUPPORT'] = 'True'
    greenlet = gevent.spawn(delete_old_files)
    socketio.run(app, port = PORT, debug=True)



