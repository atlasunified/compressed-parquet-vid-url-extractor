import pyarrow.parquet as pq
import pandas as pd
import re

def find_ngrams(text, n, url_pattern):
    words = text.split()
    ngrams = []

    for i, word in enumerate(words):
        if re.match(url_pattern, word):
            ngram_start_prior = max(0, i - n)
            ngram_end_prior = i

            ngram_start_post = i + 1
            ngram_end_post = min(len(words), i + n + 1)

            ngrams.append((words[ngram_start_prior:ngram_end_prior], word, words[ngram_start_post:ngram_end_post]))

    return ngrams

def parse_column_selection(selection, headers):
    columns = []
    parts = selection.split(',')

    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            columns.extend(headers[start - 1:end])
        else:
            index = int(part) - 1
            columns.append(headers[index])

    return columns

def filter_video_urls(value):
    patterns = [
        r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+',
        r'(https?://)?(www\.)?(vimeo\.com)/.+',
        r'(https?://)?(www\.)?(dailymotion\.com)/.+',
        r'(https?://.+)\.(mp4|mkv|flv|avi|webm|mov|m4v|mpg|wmv)'
    ]

    if isinstance(value, bytes):
        value = value.decode('utf-8')

    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            url = match.group(0)
            url = re.sub(r'(\s*\"]\s*)$', '', url)  # Strip the ' "] ' off the end of the URL
            return url

    return None

def deduplicate_urls(video_urls):
    unique_urls = list(set(video_urls))
    return unique_urls

def main():
    parquet_file = 'compressed.parquet'
    table = pq.read_table(parquet_file)
    headers = table.schema.names

    print("Column headers:")
    for i, header in enumerate(headers, start=1):
        print(f"{i}. {header}")

    selected_columns_str = input("Enter the column numbers you want to extract (e.g., '1, 2, 3' or '1-3'): ")
    selected_columns = parse_column_selection(selected_columns_str, headers)

    if all(column in headers for column in selected_columns):
        selected_table = table.select(selected_columns)
        df = selected_table.to_pandas()

        for column in selected_columns:
            df[column] = df[column].apply(filter_video_urls)

        video_urls = []
        for index, row in df.iterrows():
            for column in selected_columns:
                if row[column]:
                    video_urls.append(row[column])
        unique_urls = deduplicate_urls(video_urls)

        output_txt = 'myvidlist.txt'
        with open(output_txt, 'w') as f:
            for url in unique_urls:
                f.write(f"{url}\n")
        # Find N-grams surrounding YouTube links
        n = 3
        ngram_column = selected_columns[0]  # Change this to the desired column for N-grams
        youtube_pattern = r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+'
        ngrams = []

        for index, row in df.iterrows():
            ngrams.extend(find_ngrams(str(row[ngram_column]), n, youtube_pattern))

        # Create a DataFrame for the Excel output
        ngram_data = []
        for ngram in ngrams:
            ngram_data.append((' '.join(ngram[0]), ngram[1], ' '.join(ngram[2])))

        ngram_df = pd.DataFrame(ngram_data, columns=['n-gram-prior', 'video link', 'n-gram-post'])


        # Save the DataFrame to an Excel file
        excel_output = 'n-gram-vid-list.xlsx'
        ngram_df.to_excel(excel_output, index=False)
        print(f"Video URLs and n-grams have been saved to '{excel_output}'.")


if __name__ == '__main__':
    main()
