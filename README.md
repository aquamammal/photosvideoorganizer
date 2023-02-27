# photosvideoorganizer
The script prompts the user to enter a directory path. Once the user enters the directory path, the script searches for all the image and video files within that directory. It then extracts the creation date from the exif data of each file and creates a folder in the directory with the name of the creation date (in yyyy-mm-dd format). Finally, the script moves the file into the folder with the corresponding creation date.

The code makes use of the os, PIL and shutil modules to perform file and folder operations, extract exif data and copy files between directories.

The modified code also includes a feature to ignore any subdirectories within the selected directory so that it only processes files within the main directory.



