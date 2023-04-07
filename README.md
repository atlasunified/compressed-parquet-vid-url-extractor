# compressed-parquet-vid-url-extractor

This Python script reads data from a Parquet file, processes it, and extracts video URLs based on user-selected columns. The user can select columns by entering column numbers as a comma-separated list (e.g., '1, 2, 3') or a range (e.g., '1-3'). After selecting the desired columns, the script filters out video URLs in the '.mp4', '.avi', '.mkv', '.flv', '.mov', '.wmv', and '.webm' formats. It then deduplicates the extracted video URLs and saves them in a text file called 'myvidlist.txt', with each URL on a separate line. The primary purpose of this script is to help users easily extract and organize video URLs from a given Parquet file.

The myvidlist.txt is the output example from the compressed.parquet file.
