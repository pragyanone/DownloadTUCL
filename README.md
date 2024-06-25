# tl;dr
If you want thesis files for Department of Civil Enginering, download [this folder](https://drive.google.com/drive/folders/1B_prOMKvjyQcjkBLBhmMjrqoN1HDtgJp?usp=drive_link) to some root directory (C:\\, D:\\, E:\\, etc) and **page_1.html**.

# DownloadTUCL

- The [Tribhuvan University Central Library (eLibrary)](https://elibrary.tucl.edu.np/) website is frequently inaccessible during the day.
- This Python script downloads all thesis papers within a specified collection *(Department)* (e.g., Department of Civil Engineering).
- Files downloaded for the [Department of Civil Engineering](https://elibrary.tucl.edu.np/collections/1f1fdc5f-96bf-41b1-b0d9-21ae72697297) as of 2024-06-04 can be found [here](https://drive.google.com/drive/folders/1B_prOMKvjyQcjkBLBhmMjrqoN1HDtgJp?usp=drive_link).
    - Download the folder and move it to the root of a drive (e.g., C:\, D:\, E:\). <br>Nested locations may not work.
    - Then open **page_1.html** and browse.

## Usage
1. Download the script **DownloadTUCL.py** and save it in a root directory.
2. Update the `base_url` to reflect your chosen collection.
3. Adjust the page range as needed (`range(1, 8)`).
4. Run the script.
5. Open **tucl/page1.html** and browse.

## Limitation
1. The website currently only allows filtering upto the collection level *(as far as I know)*. It would be more helpful if filtering by specific programs (e.g., MSc. in Transportation Engineering) was possible.

Feedback is welcome.

