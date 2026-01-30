import os

def get_files_info(working_directory, directory="."):
    
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    print("DEBUG working_dir_abs:", working_dir_abs)
    print("DEBUG target_dir:", target_dir)
    print("DEBUG isdir(target_dir):", os.path.isdir(target_dir))


    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    result = []
    for name in os.listdir(target_dir):
        name_path = target_dir + "/" + name
        size = os.path.getsize(name_path)
        is_dir = os.path.isdir(name_path)
        result.append(f"- {name}: file_size:={size} bytes, is_dir={is_dir}")
    
    return "\n".join(result)
    
def main():
    result1 = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result1)

    # and similarly for the other 3 calls...

if __name__ == "__main__":
    main()