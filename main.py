import os
import shutil
import time


def main() -> None:
    print("Scanning for junk...\t")

    # TODO: Scan for junk
    TEMP_DIR = os.path.expanduser(r"~\AppData\Local\Temp")

    # Calculate size and print cache size
    temp_cache_size = get_dir_size(TEMP_DIR)
    print(f"Cache size: {get_formatted_size(temp_cache_size)}")

    # TODO: Ask user whether to clean cache or not
    if prompt_clean_cache():
        # TODO: Clean cache
        clean_cache(TEMP_DIR)
    else:
        print("Okay :)")


def get_dir_size(dir_path: str) -> int:
    """
    Return size of the directory in bytes.

    :param dir_path: Path of directory
    :type dir_path: str
    :return: Size of the directory in bytes
    :rtype: int
    """
    size = 0

    for root, _, files in os.walk(dir_path):
        size += sum(os.path.getsize(os.path.join(root, name)) for name in files)

    return size


def get_formatted_size(size: int) -> str:
    """
    Return size in KB's, MB's or GB's.

    :param size: Size in bytes
    :type size: int
    :return: Size in KB's, MB's or GB's.
    :rtype: str
    """
    size /= 1024
    suffixes = ["KB", "MB", "GB"]

    for suffix in suffixes:
        if size < 1024:
            break
        size /= 1024

    return f"{size:.2f}{suffix}"


def prompt_clean_cache() -> bool:
    """Return if the cache should be cleaned or not"""
    choice = ""

    while choice not in ("Y", "N"):
        choice = input("Clean your cache? [Y | N]: ").strip().upper()

    return choice == "Y"


def clean_cache(dir_path: str) -> None:
    """
    Clean cache files in dir_path.

    :param dir_path: Path of folder to be cleaned
    :type dir_path: str
    """
    cleaned_size = 0
    start_time = time.time()

    try:
        dirs = os.listdir(dir_path)

        if not dirs:
            print("No directory to clean.")
            return
        for file in dirs:
            path = os.path.join(dir_path, file)

            try:
                if not os.path.isdir(path):
                    file_size = os.path.getsize(path)
                    print(f"Removing {path}", end="\t")
                    os.remove(path)
                else:
                    file_size = get_dir_size(path)
                    print(f"Removing {path}", end="\t")
                    shutil.rmtree(path)
            except PermissionError:
                print("ACCESS DENIED")
            else:
                print("[DONE]")
                cleaned_size += file_size
    except PermissionError:
        print(f"Abort! Couldn't clean {dir_path}! ACCESS DENIED")

    end_time = time.time()

    print(f"Success!\nCleaned {get_formatted_size(cleaned_size)}.")
    print(f"Time Elapsed: {(end_time - start_time) * 1000:.2f}ms")


if __name__ == "__main__":
    main()
