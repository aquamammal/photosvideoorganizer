import os
import shutil
from datetime import datetime
from PIL import Image, ExifTags
import tkinter as tk
from tkinter import filedialog, messagebox


def choose_directory():
    global media_path
    media_path = filedialog.askdirectory()
    if media_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, media_path)


def organize_media():
    try:
        # loop through each file in the directory
        for filename in os.listdir(media_path):
            file_path = os.path.join(media_path, filename)

            # check if the file is an image or video
            ext = os.path.splitext(filename)[1].lower()
            if ext not in ('.jpg', '.jpeg', '.png', '.mp4', '.avi', '.mov'):
                continue

            # extract the date and time information from the file's metadata
            if ext in ('.jpg', '.jpeg', '.png'):
                try:
                    with Image.open(file_path) as img:
                        exif_data = img._getexif()
                except:
                    exif_data = None

                if exif_data is not None:
                    for tag, value in exif_data.items():
                        if tag in ExifTags.TAGS and ExifTags.TAGS[tag] == 'DateTimeOriginal':
                            datetime_original = value
                            break
                    else:
                        datetime_original = None

                    if datetime_original is not None:
                        date_str = datetime.strptime(datetime_original, '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d')
                    else:
                        date_str = 'unknown_date'
                else:
                    date_str = 'unknown_date'
            else:
                try:
                    # use the creation time of the video file
                    creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    date_str = creation_time.strftime('%Y-%m-%d')
                except:
                    date_str = 'unknown_date'

            # create a folder with the date from the file's metadata
            folder_path = os.path.join(media_path, date_str)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # move the file to the corresponding folder
            new_file_path = os.path.join(folder_path, filename)
            shutil.move(file_path, new_file_path)

        messagebox.showinfo("Success", "Media files organized successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error organizing media files: {str(e)}")


# create the main window
root = tk.Tk()
root.title("Media Organizer")

# create a label and entry for the folder path
folder_label = tk.Label(root, text="Media folder:")
folder_label.grid(row=0, column=0, padx=5, pady=5)

folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=5, pady=5)

folder_button = tk.Button(root, text="Choose folder", command=choose_directory)
folder_button.grid(row=0, column=2, padx=5, pady=5)

# create a button to organize the media
organize_button = tk.Button(root, text="Organize media", command=organize_media)
organize_button.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()
