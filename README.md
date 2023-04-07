# compressed-parquet-vid-url-extractor

This Python script reads data from a Parquet file, processes it, and extracts video URLs based on user-selected columns. The user can select columns by entering column numbers as a comma-separated list (e.g., '1, 2, 3') or a range (e.g., '1-3'). After selecting the desired columns, the script filters out video URLs in the '.mp4', '.avi', '.mkv', '.flv', '.mov', '.wmv', and '.webm' formats. It then deduplicates the extracted video URLs and saves them in a text file called 'myvidlist.txt', with each URL on a separate line. The primary purpose of this script is to help users easily extract and organize video URLs from a given Parquet file.

The myvidlist.txt is the output example from the compressed.parquet file.

##Please check your myvidlist.txt file for the following types of errors, as I cannot code out the erronous URLs:

###Two dots in the vid-file:
https://bloximages.chicago2.vip.townnews.com/weatherforddemocrat.com/content/tncms/assets/v3/editorial/4/80/4806df6a-59e3-11ec-abbc-d77264de681a/61b3965be45ff.video.mp4

###Commas in the vid-file:
https://voanews-vh.akamaihd.net/i/Pangeavideo/2022/01/0/09/09a80000-0a00-0242-1936-08d9e2b39d11,_240p,,_480p,_720p,_1080p,.mp4

###No video file but ends in MP4/vid extension:
https://d1.vnecdn.net/giaitri/video/video/web/mp4
