import json;
import hashlib;
import os;

#Functions created with the help of Deepseek and Copilot generative AI tools.
def hash_file(filepath):
    try: 
        hash_func = hashlib.sha256()

        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hash_func.update(chunk)

        return hash_func.hexdigest()

    except Exception as e:
        print("Error: hashing file")
        return None;
    

def traverse_directory(directory):
    file_hashes = {}

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path)
            if file_hash:
                rel_path = os.path.relpath(file_path, directory)
                file_hashes[rel_path] = file_hash
    
    return file_hashes

def generate_table(directory):
    file_hashes = traverse_directory(directory)
    
    hash_table = {
        "directory": directory,
        "files": file_hashes
    }

    with open('hash_table.json', 'w') as f:
        json.dump(hash_table, f, indent=4)

    print("Hash table generated")
    return True

def validate_hash():
    with open('hash_table.json', 'r') as f:
        hash_table = json.load(f)

    original_directory = hash_table["directory"]
    stored_files = hash_table["files"] 

    current_files = {}
    for root, dirs, filenames in os.walk(original_directory): 
        for filename in filenames: 
            file_path = os.path.join(root, filename)
            file_hash = hash_file(file_path)
            if file_hash:
                rel_path = os.path.relpath(file_path, original_directory)
                current_files[rel_path] = file_hash

    problem_count = 0

    for filepath, stored_hash in stored_files.items():  
        if filepath in current_files:
            if current_files[filepath] != stored_hash:
                print(f"Modified: {filepath}")
                problem_count += 1
            else:
                print(f"Valid: {filepath}")
        else:
            print(f"file is deleted: {filepath}")
            problem_count += 1

    for filepath in current_files:
        if filepath not in stored_files:
            print(f"file added: {filepath}")
            problem_count += 1
    
    
    return problem_count == 0

def main():
    while True:
        print("1. Generate a new hash table")
        print("2. Verifying hashes")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            directory = input("Enter the directory to hash: ")
            if generate_table(directory):
                print("Hash table generated successfully.")
            else:
                print("Failed to generate hash table.")

        elif choice == '2':
            if validate_hash():
                print("All files are valid.")
            else:
                print("Some files have issues.")

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()