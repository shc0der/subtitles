import pandas as pd
import re

def parse_webvtt(file_path):
    text_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n(.+?)\n\n', re.DOTALL)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    subtitles = text_pattern.findall(content)

    df = pd.DataFrame(subtitles, columns=['Start', 'End', 'Text'])

    return df
