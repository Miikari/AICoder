from functions.get_files_info import get_files_info

def main():

    result = get_files_info("calculator", ".")
    print(f"Result for current directory:\n{result}")

    result = get_files_info("calculator", "pkg")
    print(result)

    result = get_files_info("calculator", "pkg")
    print(result)

    result = get_files_info("calculator", "/bin")
    print(result)

    result = get_files_info("calculator", "../")
    print(result)

main()