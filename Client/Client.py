import base64
import json
import os
import re
import requests
import socketio
import sys
import threading
import tkinter as tk
import uuid
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from datetime import datetime
from CustomModules.RandomUsernames import generate_username
from tkinter import PhotoImage, scrolledtext, messagebox, filedialog
from webbrowser import open as open_url










class Login():
    def __init__(self, root):
        self.root = root
        root.title("Login")
        root.geometry("400x200")
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.withdraw()
        root.iconbitmap(icon)
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.background_image = PhotoImage(file=login_img)
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        root.deiconify()
        self.sio = client


        # Eingabefelder
        self.room_label = tk.Label(root, text="Room:")
        self.room_label.pack(pady=10)  
        self.room_entry = tk.Entry(root)
        self.room_entry.pack()

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack(pady=10)  
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        # Buttons
        self.create_button = tk.Button(root, text="Create room", command=self.create_room)
        self.create_button.pack(pady=10)

        self.join_button = tk.Button(root, text="Enter room", command=self.join_room)
        self.join_button.pack()


    def create_room(self):
        global username, room
        username = self.username_entry.get().strip().replace(' ', '')
        room = self.room_entry.get().strip().replace(' ', '')
        if not 3 <= len(username) <= 20 or username == '':
            username = generate_username(1)[0]
        if not 6 <= len(room) <= 36 and room != '':
            room = str(uuid.uuid4())
        threading.Thread(target=self._create_room_thread, args=(username, room), daemon=True).start()
    
    def _create_room_thread(self, username, room_id):
        global room, key
        self.switch_status('disabled')
        try:
            response = requests.post(f'{base_url}/create_room', json={'room_id': room})
        except requests.exceptions.ConnectionError:
            messagebox.showerror('Error', 'Failed to connect to server.')
            self.switch_status('normal')
            return
        if response.status_code == 201:
            print('Room created successfully.')
            print('Room ID:', response.json()['room_id'])
            room_id = response.json()['room_id']
            key = base64.b64decode(response.json()['key'])
            print(key)
        elif response.status_code == 409:
            messagebox.showerror('Error', 'Room already exists.')
            self.switch_status('normal')
            return
        else:
            messagebox.showerror('Error', 'Failed to create room.')
            self.switch_status('normal')
            return
        room = room_id 
        try:
            self.sio.connect(base_url)
        except:
            messagebox.showerror('Error', 'Failed to connect to server.')
            self.switch_status('normal')
            return
        self.sio.emit('join', {'username': username, 'room': room})
        top = tk.Toplevel(self.root)
        top.withdraw()
        Chat(top, self.root)


    def join_room(self):
        global username, room
        username = self.username_entry.get().strip().replace(' ', '')
        room = self.room_entry.get().strip().replace(' ', '')
        if not 6 <= len(room) <= 36 or room == '':
            messagebox.showerror('Error', 'Room ID needs to be between 6 and 36.')
            return
        if not 3 <= len(username) <= 20:
            username = generate_username(1)[0]
        threading.Thread(target=self._join_room_thread, args=(username, room), daemon=True).start()
    
    def _join_room_thread(self, username, room):
        global key
        self.switch_status('disabled')
        try:
            response = requests.get(f'{base_url}/room_exists?room_id={room}')
            key = base64.b64decode(response.json()['key'])
            print(key)
        except requests.exceptions.ConnectionError:
            messagebox.showerror('Error', 'Failed to connect to server.')
            self.switch_status('normal')
            return
        if response.status_code == 200:
            try:
                self.sio.connect(base_url)
            except requests.exceptions.ConnectionError:
                messagebox.showerror('Error', 'Failed to connect to server.')
                self.switch_status('normal')
                return
            response = self.sio.emit('join', {'username': username, 'room': room})
            print(response)
            top = tk.Toplevel(self.root)
            top.withdraw()
            Chat(top, self.root)            
        elif response.status_code == 404:
            messagebox.showerror('Error', 'Room does not exist.')
            self.switch_status('normal')
            return
        elif response.status_code == 400:
            messagebox.showerror('Error', 'Room ID is missing.')
            self.switch_status('normal')
            return
        elif response.status_code == 500:
            messagebox.showerror('Error', 'Failed to join room.')
            self.switch_status('normal')
            return
        else:
            messagebox.showerror('Error', response)
            self.switch_status('normal')
            return


    def switch_status(self, state: str):
        self.create_button.config(state=state)
        self.join_button.config(state=state)
        self.room_entry.config(state=state)
        self.username_entry.config(state=state)
        if state == 'disabled':
            self.root.title("Loading...")
        else:
            self.root.title("Login")
    



    def close(self):
        self.root.destroy()
        sys.exit(0)








class Chat():
    def __init__(self, root, parent):
        def __format_size(self, size):
            if size < 1024:
                return f"{size} B"
            size /= 1024
            if size < 1024:
                return f"{size:.2f} KB"
            size /= 1024
            if size < 1024:
                return f"{size:.2f} MB"
            size /= 1024
            if size < 1024:
                return f"{size:.2f} GB"
            size /= 1024
            return f"{size:.2f} TB"

        def __minutes_to_readable_time(self, minutes):
            minutes_in_a_day = 1440
            minutes_in_a_week = 10080

            weeks, minutes = divmod(minutes, minutes_in_a_week)
            days, minutes = divmod(minutes, minutes_in_a_day)
            hours, minutes = divmod(minutes, 60)

            time_string = ""
            if weeks > 0:
                time_string += f"{weeks} Woche(n) "
            elif days > 0:
                time_string += f"{days} Tag(e) "
            elif hours > 0:
                time_string += f"{hours} Stunde(n) "
            elif minutes > 0:
                time_string += f"{minutes} Minute(n)"

            return time_string.strip()

        def __validate_config(self, config):
            expected_structure = {
                "audio_extensions": list,
                "file_age_limit": int,
                "img_extensions": list,
                "max_upload_size": int,
                "text_extensions": list,
                "video_extensions": list,
                "zip_extensions": list,
            }

            for key, expected_type in expected_structure.items():
                if key not in config:
                    print(f"Missing key: {key}")
                    return False
                if not isinstance(config[key], expected_type):
                    print(f"Unexpected type for key {key}. Expected {expected_type}, got {type(config[key])}.")
                    return False

            return True


        self.root = root
        self.root.withdraw()
        self.parent = parent

        request = requests.get(f'{base_url}/config')
        if request.status_code == 200:
            if not __validate_config(self, request.json()):
                messagebox.showerror('Error', 'Config from Server is invalid.')
                sys.exit(1)
            self.config = request.json()
            print('Config loaded successfully.')
        else:
            messagebox.showerror('Error', 'Failed to load config.')
            sys.exit(1)

        self.config.update({'max_upload_size_formated': __format_size(self, self.config.get('max_upload_size'))})
        self.config.update({'file_age_limit': __minutes_to_readable_time(self, self.config.get('file_age_limit'))})

        self.sio = socketio.Client()
        self.root.title("Chat")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.iconbitmap(icon)
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        self.sio = client
        self.sio.on('message')(self.message)
        self.sio.on('disconnect')(self.disconnect)
        self.sio.on('join')(self.join)
        self.sio.on('leave')(self.leave)
        self.sio.on('file')(self.file_uploaded)
        self.disconnected = False
        self.uuid = ''



        room_frame = tk.Frame(root)
        room_frame.pack()

        left_spacer = tk.Label(room_frame, width=10)
        left_spacer.pack(side='left')

        self.room_label = tk.Label(room_frame, text=f"Room: {room}", width=40)
        self.room_label.pack(side='left')

        self.room_copy_button = tk.Button(room_frame, text="Copy room name", command=self.copy_room_name_to_clipboard)
        self.room_copy_button.pack(side='left')

        right_spacer = tk.Label(room_frame, width=10)
        right_spacer.pack(side='left')

        username_frame = tk.Frame(root)
        username_frame.pack()

        left_spacer = tk.Label(username_frame, width=10)
        left_spacer.pack(side='left')

        self.username_label = tk.Label(username_frame, text=f"Username: {username}", width=40)
        self.username_label.pack(side='left')

        self.username_copy_button = tk.Button(username_frame, text="Copy username", command=self.copy_username_to_clipboard)
        self.username_copy_button.pack(side='left')

        right_spacer = tk.Label(username_frame, width=10)
        right_spacer.pack(side='left')

        self.chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
        self.chat_window.bind("<Enter>", lambda e: self.chat_window.config(cursor=""))
        self.chat_window.pack(fill='both', expand=True)
        self.chat_window.tag_config('username_partner', foreground='black')
        self.chat_window.tag_config('username_self', foreground='blue')
        self.chat_window.tag_config('message', foreground='black')
        self.chat_window.tag_config('info', foreground='blue')
        self.chat_window.tag_config('error', foreground='red')
        self.chat_window.tag_config('file', foreground='green')
        self.chat_window.tag_config('link', foreground='green', underline=1)
        self.chat_window.tag_bind("link", "<Button-1>", self.open_link)
        self.chat_window.tag_bind("link", "<Enter>", lambda e: self.chat_window.config(cursor="hand2"))
        self.chat_window.tag_bind("link", "<Leave>", lambda e: self.chat_window.config(cursor=""))

        self.text_entry = scrolledtext.ScrolledText(root, height=3)
        self.text_entry.pack(side='left', fill='both', expand=True)


        send_button_frame = tk.Frame(root)
        send_button_frame.pack(side='right', fill='both', expand=True)

        if self.config.get('max_upload_size') != 0:
            self.send_file_button = tk.Button(send_button_frame, text="Send File", command=self.send_file)
            self.send_file_button.pack(side='bottom', fill='both', expand=True)
        else:
            self.send_file_button = tk.Button(send_button_frame, text="Upload disabled", state='disabled')
            self.send_file_button.pack(side='bottom', fill='both', expand=True)

        self.send_button = tk.Button(send_button_frame, text="Send", command=self.send_message)
        self.text_entry.bind('<Return>', self.return_key)
        self.send_button.pack(side='top', fill='both', expand=True)

        self.parent.withdraw()
        self.root.deiconify()


    def copy_room_name_to_clipboard(self):
        label_text = self.room_label.cget('text')
        room = label_text.split(": ")[1]
        self.root.clipboard_clear()
        self.root.clipboard_append(room)


    def copy_username_to_clipboard(self):
        label_text = self.username_label.cget('text')
        username = label_text.split(": ")[1]
        self.root.clipboard_clear()
        self.root.clipboard_append(username)



    def send_message(self):
        def __encrypt_message(message):
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
            return iv, ciphertext

        message = self.text_entry.get('1.0', 'end-1c').strip()
        self.text_entry.delete('1.0', 'end')
        if not message or message.isspace():
            return
        iv, ciphertext = __encrypt_message(message)
        self.sio.emit('message', {'message': ciphertext, 'iv': iv, 'room': room, 'user': username})
        self.insert_into_chat(message, username = "X", kind = 'message')


    def send_file(self):
        text_extensions = self.config.get('text_extensions')
        img_extensions = self.config.get('img_extensions')
        zip_extensions = self.config.get('zip_extensions')
        audio_extensions = self.config.get('audio_extensions')
        video_extensions = self.config.get('video_extensions')
        extensions = text_extensions + img_extensions + zip_extensions + audio_extensions + video_extensions

        all_extensions = [(f'All files ({", ".join("*." + ext for ext in extensions)})', ' '.join(f'*.{ext}' for ext in extensions))]
        text_files = [(f'Text files ({", ".join("*." + ext for ext in text_extensions)})', ' '.join(f'*.{ext}' for ext in text_extensions))]
        image_files = [(f'Image files ({", ".join("*." + ext for ext in img_extensions)})', ' '.join(f'*.{ext}' for ext in img_extensions))]
        archive_files = [(f'Archive files ({", ".join("*." + ext for ext in zip_extensions)})', ' '.join(f'*.{ext}' for ext in zip_extensions))]
        audio_files = [(f'Audio files ({", ".join("*." + ext for ext in audio_extensions)})', ' '.join(f'*.{ext}' for ext in audio_extensions))]
        video_files = [(f'Video files ({", ".join("*." + ext for ext in video_extensions)})', ' '.join(f'*.{ext}' for ext in video_extensions))]

        filetypes = all_extensions + text_files + image_files + archive_files + audio_files + video_files
        filename = filedialog.askopenfilename(filetypes=filetypes)

        if filename:
            filesize = os.path.getsize(filename)
            if filesize > self.config.get('max_upload_size'):
                messagebox.showerror("Error", f"File too large.\nMaximum {self.config.get('max_upload_size_formated')}.")
                return
            only_filename = os.path.basename(filename)
            with open(filename, 'rb') as file:
                file_data = file.read()
            self.uuid = str(uuid.uuid4())
            data = {'room': room, 'user': username, 'only_filename': only_filename, 'filesize': filesize, 'uuid': self.uuid}
            files = {'file': file_data}
            def send_file_thread():  
                try:
                    response = requests.post(f'{base_url}/upload_file', files=files, data=data)
                    if response.status_code == 200:
                        response_data = response.json()
                        self.insert_into_chat(f"Sent file: \"{filename}\"", username = "X", kind = 'file', url = response_data['url'])
                    elif response.status_code == 400:
                        messagebox.showerror("Error", response.text)
                    elif response.status_code == 413:
                        messagebox.showerror("Error", f"Either file too large (Maximum {self.config.get('max_upload_size_formated')}),\nor upload folder is full.\nTry again at a later time.")
                    elif response.status_code == 415:
                        messagebox.showerror("Error", "Unsupported file type")
                    else:
                        messagebox.showerror("Error", "Something went wrong.")
                    self.send_file_button.configure(state='normal', text='Send File')
                except requests.exceptions.ConnectionError:
                    messagebox.showerror("Error", "Connection error")
                    if self.sio.connected:
                        self.send_file_button.configure(state='normal', text='Send File')
                    else:
                        self.send_file_button.configure(state='disabled', text='Send File')

            self.send_file_button.configure(state='disabled', text='Sending...')
            threading.Thread(target=send_file_thread).start()


    def insert_into_chat(self, message, username: str = None, kind: str = None, url: str = ''):
        self.chat_window.configure(state='normal')

        # Check if scrollbar is at the end
        at_end = self.chat_window.yview()[1] == 1.0
        url_pattern = re.compile(r'([a-zA-Z]*://|www\.)+(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

        if kind == 'join':
            self.chat_window.insert(tk.END, f'{datetime.now().strftime("%H:%M:%S")} -> ', 'info')
            self.chat_window.insert(tk.END, message + '\n\n', 'message')
        elif kind == 'leave':
            self.chat_window.insert(tk.END, f'{datetime.now().strftime("%H:%M:%S")} <- ', 'info')
            self.chat_window.insert(tk.END, message + '\n\n', 'message')
        elif kind == 'disconnect':
            self.chat_window.insert(tk.END, f'{datetime.now().strftime("%H:%M:%S")} X ', 'error')
            self.chat_window.insert(tk.END, message + '\n\n', 'message')
        elif kind == 'message':
            if username == "X":
                self.chat_window.insert(tk.END, f'{datetime.now().strftime("%H:%M:%S")} (You):\n', 'username_self')
            else:
                self.chat_window.insert(tk.END, f'{datetime.now().strftime("%H:%M:%S")} ({username}):\n', 'usename_partner')
        
            start = 0
            for match in url_pattern.finditer(message):
                self.chat_window.insert(tk.END, message[start:match.start()], 'message')
                self.chat_window.insert(tk.END, message[match.start():match.end()], 'link')
                start = match.end()
            self.chat_window.insert(tk.END, message[start:] + '\n\n', 'message')
        elif kind == 'file':
            if username == "X":
                self.chat_window.insert(tk.END, f'{datetime.now().strftime("%H:%M:%S")} (You):\n', 'username_self')
            else:
                self.chat_window.insert(tk.END, f'{datetime.now().strftime("%H:%M:%S")} ({username}):\n', 'usename_partner')
            self.chat_window.insert(tk.END, message + '\n', 'file')
            self.chat_window.insert(tk.END, url + '\n\n', 'link')

        # If scrollbar was at the end before insert, scroll to the end
        if at_end:
            self.chat_window.see(tk.END)

        self.chat_window.configure(state='disabled')


    def return_key(self, event):
        if event.state & 0x1:
            self.text_entry.insert(tk.END, '\n')
        else:
            self.send_message()
        return "break"


    def open_link(self, event):
        # Get the index of the mouse click
        click_index = self.chat_window.index("@%s,%s" % (event.x, event.y))
        
        # Get all the tags at the click index
        tags = self.chat_window.tag_names(click_index)
        
        # Check if the clicked text has the "link" tag
        if "link" in tags:
            # Get the range of the link tag
            ranges = self.chat_window.tag_ranges("link")
            for i in range(0, len(ranges), 2):
                start = ranges[i]
                end = ranges[i+1]
                # Check if the click index is within this range
                if self.chat_window.compare(start, "<=", click_index) and self.chat_window.compare(end, ">=", click_index):
                    url = self.chat_window.get(start, end).strip()
                    break
        
        if not self.is_url_active(url):
            messagebox.showwarning("Warning", f"Link is no longer valid.\nLinks are only available for {self.config.get('file_age_limit')}.")
            return
        answer = messagebox.askyesnocancel("Open Link", f"Open link?\nClick on 'no', to copy to clipboard.", default='yes')
        if answer == True:
            open_url(url)
        elif answer == False:
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            messagebox.showinfo("Copied", f"Link copied to clipboard:\n{url}")
        elif answer is None:
            pass



    def is_url_active(self, url):
        # If url starts with base_url, then return
        if not url.startswith(base_url):
            return True
        else:
            try:
                response = requests.head(url)
                return response.status_code == 204 # 204 = No Content
            except requests.exceptions.ConnectionError:
                return False


    def join(self, data):
        message = data['message']
        self.insert_into_chat(message, kind='join')


    def message(self, data):
        def __decrypt_message(message, key, iv):
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(message), AES.block_size)
            return plaintext.decode()

        message = data['message']
        iv = data['iv']
        user = data['user']
        message = __decrypt_message(message, key, iv)
        print(message)
        self.insert_into_chat(message, user, kind = 'message')


    def file_uploaded(self, data):
        url = data['url']
        user = data['user']
        filename = data['filename']
        if self.uuid == data['uuid']:
            return
        self.insert_into_chat(f"Received file: \"{filename}\"", user, kind = 'file', url = url)


    def leave(self, data):
        message = data['message']
        self.insert_into_chat(message, kind='leave')


    def disconnect(self, data = None):
        if self.disconnected:
            return
        if data:
            message = data['message']
        else:
            message = 'You have been disconnected from the server.'
            self.text_entry.configure(state='disabled')
            self.send_button.configure(state='disabled')
            self.send_file_button.configure(state='disabled')
            self.disconnected = True
            self.sio.disconnect()
        self.insert_into_chat(message, kind='disconnect')


    def close(self):
        self.root.withdraw()
        if self.sio.connected:
            self.sio.emit('leave', {'username': username, 'room': room})
            self.sio.disconnect()
        self.root.destroy()
        os._exit(0)











      








if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    dir_of_app = os.path.dirname(os.path.abspath(sys.argv[0]))

    config_file = os.path.join(dir_of_app, 'config.json')
    if not os.path.isfile(config_file):
        # Write new config file
        config = {
            'url': 'https://chat.bloodygang.com',
            'port': 5000
            }
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        url = config['url']
        port = config['port']
    else:
        with open(config_file, 'r') as f:
            try:
                config = json.load(f)
            except json.decoder.JSONDecodeError:
                messagebox.showerror("Error", "Config file is not valid JSON.")
                sys.exit(1)
        url = config['url']
        port = config['port']
        
    static = os.path.join(os.path.dirname(__file__), 'static')
    icon = os.path.join(static, 'icon.ico')
    loading_img = os.path.join(static, 'loading.png')
    login_img = os.path.join(static, 'login.png')
    
    client = socketio.Client()
    try:
        base_url = url
        print(base_url)
        request = requests.get(f'{base_url}/health')
        if request.status_code != 200:
            raise requests.exceptions.ConnectionError
    except requests.exceptions.ConnectionError:
        try:
            base_url = f'{url}:{port}'  
            print(base_url)
            request = requests.get(f'{base_url}/health')
            if request.status_code != 200:
                raise requests.exceptions.ConnectionError
        except requests.exceptions.ConnectionError:
            root.withdraw()
            messagebox.showerror("Error", "Server is not reachable.\nPlease check the config.json file.")
            sys.exit(1)
    login = Login(root)
    root.mainloop()
else:
    raise Exception('This file was not created to be imported')
