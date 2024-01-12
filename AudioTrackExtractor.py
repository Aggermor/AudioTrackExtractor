import os
import subprocess
import tkinter as tk
from tkinter import filedialog

def extract_audio_tracks(video_file, output_dir):
    command = ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', video_file]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    num_tracks = len(result.stdout.decode().split('\n')) - 1

    for i in range(num_tracks):
        output_file = os.path.join(output_dir, f"audio_track_{i}.mp3")
        command = ['ffmpeg', '-i', video_file, '-map', f'0:a:{i}', output_file]
        subprocess.run(command)

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("MKV files", "*.mkv")])
    return filename

def browse_folder():
    foldername = filedialog.askdirectory()
    return foldername

def main():
    root = tk.Tk()
    root.title("Audio Extractor")

    def start_extraction():
        video_file = browse_file()  # Ask the user to select a file
        output_dir = browse_folder()  # Ask the user to select a folder
        extract_audio_tracks(video_file, output_dir)

    browse_button = tk.Button(root, text="Browse", command=start_extraction)
    browse_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
