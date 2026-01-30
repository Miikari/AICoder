from functions.get_file_content import get_file_content

def main():

    result = get_file_content("calculator", "lorem.txt")
    if len(result) > 10000 and "truncated at" in result:
        print("len ok, truncate ok")
    print(len(result))
    print(result[-100:])

    result = get_file_content("calculator", "main.py")
    print(f"Result for pkg file:\n{result}")

    result = get_file_content("calculator", "pkg/calculator.py") 
    print(f"Result for pkg file:\n{result}")

    result = get_file_content("calculator", "/bin/cat")
    print(f"Result for /bin file:\n{result}")

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print(f"Result for pkg/does_not_exist.py file:\n{result}")

main()