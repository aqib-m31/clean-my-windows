# Clean My Windows

Clean My Windows is a python script developed for CS50P's final project. The project aims to clean unnecessary junk and cache files from a Windows system, freeing up valuable disk space and improving system performance.

### How it Works
1. The script scans for various cache directories, including user temp, system temp, prefetch, and local cache directories.
2. It calculates the size of the junk files and displays the results.
3. Users are prompted to decide whether they want to clean the cache or not.
4. If they choose to clean, the script proceeds to clean the cache and displays statistics after the cleaning process.
5. In case of access denied errors, the script logs the paths that couldn't be cleaned.

### Dependencies
- Python 3.x
- `colorama`

### How to Run
1. Clone the repository `git clone https://github.com/aqib-m31/clean-my-windows`
2. Install the required library using `pip install -r requirements.txt`.
3. Run the script using `python clean_my_windows.py`.

> Note: Run on windows machine.

### This tool cleans following directories:
- `C:\Users\username\AppData\Local\Temp`
- `C:\Windows\Temp`
- `C:\Windows\Prefetch`
- All directories with names `cache` or `cache2` in `C:\Users\username\AppData\Local`
