import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

def extract_audio_tracks(video_file, output_dir):
    command = ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', video_file]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    num_tracks = len(result.stdout.decode().split('\n')) - 1

    overwrite_all = None
    existing_files = []

    for i in range(num_tracks):
        output_file = os.path.join(output_dir, f"audio_track_{i}.mp3")
        if os.path.exists(output_file):
            existing_files.append(output_file)

    if existing_files and overwrite_all is not True:
        if overwrite_all is None:
            result = messagebox.askyesnocancel("Files exist", "Some files already exist. Do you want to overwrite them?", icon='warning')
            if result is None:  # Cancel
                return
            elif result:  # Yes
                overwrite_all = True
                if simpledialog.askyesno("Apply to all", "Apply this action to all existing files?", icon='info'):
                    overwrite_all = 'all'
        if not overwrite_all:  # No
            return

    for i in range(num_tracks):
        output_file = os.path.join(output_dir, f"audio_track_{i}.mp3")
        if os.path.exists(output_file) and overwrite_all != 'all':
            continue
        command = ['ffmpeg', '-y', '-i', video_file, '-map', f'0:a:{i}', output_file]
        subprocess.run(command)

def main():
    root = tk.Tk()
    root.title("Audio Extractor")

    video_file = tk.StringVar()
    output_dir = tk.StringVar()

    def browse_file():
        filename = filedialog.askopenfilename(filetypes=[("MKV files", "*.mkv")])
        video_file.set(filename)

    def browse_folder():
        foldername = filedialog.askdirectory()
        output_dir.set(foldername)

    def start_extraction():
        if video_file.get() and output_dir.get():
            extract_audio_tracks(video_file.get(), output_dir.get())

    browse_file_button = tk.Button(root, text="Browse Video File", command=browse_file, anchor='w')
    browse_file_button.pack(fill='x')

    video_file_label = tk.Label(root, textvariable=video_file, anchor='w')
    video_file_label.pack(fill='x')

    browse_folder_button = tk.Button(root, text="Browse Destination Folder", command=browse_folder, anchor='w')
    browse_folder_button.pack(fill='x')

    output_dir_label = tk.Label(root, textvariable=output_dir, anchor='w')
    output_dir_label.pack(fill='x')

    convert_button = tk.Button(root, text="Convert", command=start_extraction, state=tk.DISABLED, anchor='w')
    convert_button.pack(fill='x')

    def check_convert_button_state(*args):
        if video_file.get() and output_dir.get():
            convert_button.config(state=tk.NORMAL)
        else:
            convert_button.config(state=tk.DISABLED)

    video_file.trace("w", check_convert_button_state)
    output_dir.trace("w", check_convert_button_state)

    exit_button = tk.Button(root, text="Exit", command=root.destroy, anchor='w')
    exit_button.pack(fill='x')

    root.mainloop()

if __name__ == "__main__":
    main()
