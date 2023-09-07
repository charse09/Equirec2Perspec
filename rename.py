import os

folder_path = os.getcwd()  # Use the current working directory as the folder path
file_extension = ".JPG"
new_extension = ".png"

# Get a list of all .jpg files in the folder
jpg_files = [filename for filename in os.listdir(folder_path) if filename.endswith(file_extension)]

# Rename the .jpg files to frame0.png, frame1.png, frame2.png, ...
for i, jpg_file in enumerate(jpg_files):
    new_name = f"frame{i}{new_extension}"
    old_path = os.path.join(folder_path, jpg_file)
    new_path = os.path.join(folder_path, new_name)
    
    try:
        os.rename(old_path, new_path)
        print(f"Renamed: {old_path} -> {new_path}")
    except Exception as e:
        print(f"Error renaming {old_path}: {e}")

print("Renaming complete.")
