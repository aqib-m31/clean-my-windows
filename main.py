from os import walk, path, remove, listdir
from shutil import rmtree
from time import time
from re import search, IGNORECASE

from paths import (
    USER_TEMP_DIR,
    SYSTEM_TEMP_DIR,
    PREFETCH_DIR,
    LOCAL_DIR,
)


def main() -> None:
    print("=== CLEAN MY WINDOWS ===")
    print("Scanning for junk...\t")

    # Scan for junk
    local_cache_dirs = get_cache_dirs(LOCAL_DIR)
    cache_dirs = [USER_TEMP_DIR, SYSTEM_TEMP_DIR, PREFETCH_DIR] + local_cache_dirs

    # Get size of junk and display it
    sizes = get_sizes(
        {
            "User Temp": USER_TEMP_DIR,
            "System Temp": SYSTEM_TEMP_DIR,
            "Prefetch": PREFETCH_DIR,
            "Local Cache Dirs": LOCAL_DIR,
        },
        multiple={"Local Cache Dirs": local_cache_dirs},
    )
    display_size(sizes)

    # Ask user whether to clean cache or not
    if prompt_clean_cache():
        # Clean cache and print stats
        size, time_elapsed = clean_all(cache_dirs)
        print(
            f"Total space freed: {get_formatted_size(size)}\nTime Elapsed: {(time_elapsed * 1000):.2f}ms"
        )
    else:
        print("Okay :)")

    input("Press any key to EXIT")


def get_dir_size(dir_path: str) -> int:
    """
    Return size of the directory in bytes.

    :param dir_path: Path of directory
    :type dir_path: str
    :return: Size of the directory in bytes
    :rtype: int
    """
    size = 0

    for root, _, files in walk(dir_path):
        size += sum(path.getsize(path.join(root, name)) for name in files)

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

    stats = {"Access Denied": [], "Cleaned Size": 0}

    try:
        dirs = listdir(dir_path)

        if not dirs:
            print("No directory to clean.")
            return
        for file in dirs:
            path = path.join(dir_path, file)

            try:
                if not path.isdir(path):
                    file_size = path.getsize(path)
                    print(f"Removing {path}", end="\t")
                    remove(path)
                else:
                    file_size = get_dir_size(path)
                    print(f"Removing {path}", end="\t")
                    rmtree(path)
            except PermissionError:
                stats["Access Denied"].append(path)
                print("[ACCESS DENIED]")
            else:
                print("[DONE]")
                stats["Cleaned Size"] += file_size
    except PermissionError:
        print(f"Abort! Couldn't clean {dir_path}!\t[ACCESS DENIED]")
        return stats

    return stats


def get_cache_dirs(dir_path: str) -> list:
    """
    Return list of all the paths in which regex pattern is found.

    :param dir_path: Path of a directory
    :type dir_path: str
    :return: A list of cache directories
    :rtype: list
    """
    cache_dirs = set()

    for root, _, _ in walk(dir_path):
        if matches := search(r"((?:.+)\\(?:cache2?))\\", root, IGNORECASE):
            cache_dirs.add(matches.group(1))

    return list(cache_dirs)


def get_dirs_size(dir_paths: list) -> int:
    """
    Return size of a list of directories.

    :param dir_paths: List of directory paths
    :type dir_paths: list
    :return: Size of directories in dir_paths
    :rtype: int
    """
    size = 0

    for dir in dir_paths:
        size += get_dir_size(dir)

    return size


def display_size(sizes: dict) -> None:
    """
    Display sizes.

    :param sizes: Dictionary having label as key and size as value
    :type sizes: dict
    """
    for label, size in sizes.items():
        print(f"{label} Size: {size}")


def get_sizes(paths: dict, multiple={}) -> dict:
    """
    Return a dictionary of sizes.

    :param paths: A dictionary having a path associated with a label (key)
    :type paths: dict
    :param multiple: A dictionary of 'paths dict keys' whose values contains list of cache directories
    :type multiple: dict
    :return: Sizes of the directories
    :rtype: dict
    """
    sizes = {}

    total_size = 0

    for label, path in paths.items():
        if label in multiple:
            size = get_dirs_size(multiple[label])
        else:
            size = get_dir_size(path)

        sizes[label] = get_formatted_size(size)
        total_size += size

    sizes["Total"] = get_formatted_size(total_size)

    return sizes


def clean_all(dirs: list) -> tuple:
    """
    Clean all directories and return space freed and time elapsed.

    :param dirs: List of directories to be cleaned
    :type dirs: list
    :return: A tuple of freed space and time elapsed
    :rtype: tuple
    """
    cleaned_size = 0
    start_time = time()

    with open("log.txt", "w") as log:
        for dir in dirs:
            stats = clean_cache(dir)
            cleaned_size += stats["Cleaned Size"]

            for path in stats["Access Denied"]:
                log.write(f"[ACCESS DENIED] - {path}\n")

    end_time = time()

    return (cleaned_size, end_time - start_time)


if __name__ == "__main__":
    main()
