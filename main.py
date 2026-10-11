import os
import shutil
import sys

import json

def organise_folder(folder_path=None):
    move_history = []

    if not folder_path:
        folder_path = input("Enter the path of the folder to organize or . for the current directory: ")

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    for file in files:
        # Track the paths
        file_extension = os.path.splitext(file)[1][1:]
        if not file_extension:  # Skip files with no extension first
            continue

        destination_folder = os.path.join(folder_path, file_extension.lower())

        # Track the paths
        move_record = {
            "source": os.path.join(folder_path, file),
            "destination": os.path.join(destination_folder, file)
        }
        move_history.append(move_record)

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        shutil.move(os.path.join(folder_path, file), os.path.join(destination_folder, file))

    print("Files have been organized.")



    # Write the history array to a file
    with open(os.path.join(folder_path, "organizer_history.json"), "w") as f:
        json.dump(move_history, f)


if __name__ == "__main__":
    # Call your setup and organizing functions here
    print("Starting file organizer...")
    mode = "organise"

    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            folder_path = sys.argv[1]

            if len(sys.argv) > 2:
                if sys.argv[2] == "--undo":
                    # Load the move history from the JSON file
                    with open(os.path.join(folder_path, "organizer_history.json"), "r") as f:
                        move_history = json.load(f)

                    # Undo the moves
                    for move in reversed(move_history):
                        shutil.move(move["destination"], move["source"])
                    sys.exit()
            else:
                print("Invalid argument. Use --undo to undo the last operation.")
                sys.exit()

            organise_folder(folder_path)
        else:
            organise_folder(None)
    else:
        sys.exit()