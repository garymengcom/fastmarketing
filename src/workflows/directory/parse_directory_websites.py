from typing import List
from urllib.parse import urlparse

import pandas as pd
import re

from src.crud.directory_website_crud import DirectoryWebsiteCrud

sheet_list = [
    {"url_column_name": "Url", "doc_url": "https://docs.google.com/spreadsheets/d/1MEwRiKgxxCGGNqrXGdoQV9bYb4uKrZCueueN_c8841w/edit?gid=0#gid=0"},
    {"url_column_name": "url", "doc_url": "https://docs.google.com/spreadsheets/d/1j2CK93YZ0HFN5CU-PeZzp9iu-BjHP-Fccd3bQuCQ9BU/edit?gid=0#gid=0"},
]

url_pattern = re.compile(r'https?://[^\s)"]+')


def extract_domains_from_sheet(doc_url, column_name) -> List[str]:
    # Convert full URL to CSV export
    csv_url = doc_url.split("/edit")[0] + "/export?format=csv"
    domains = set()

    try:
        df = pd.read_csv(csv_url)
        matched_col = next((col for col in df.columns if col.strip().lower() == column_name.lower()), None)
        if not matched_col:
            print(f"[Warning] Column '{column_name}' not found in: {doc_url}")
            return []

        values = df[matched_col].dropna().astype(str)
        for val in values:
            domain = urlparse(val).netloc or urlparse("http://" + val).netloc
            if domain:
                domains.add(domain.lower())

    except Exception as e:
        print(f"[Error] Failed to read sheet: {doc_url}\n{e}")

    return list(domains)


if __name__ == '__main__':
    for sheet in sheet_list:
        domains = extract_domains_from_sheet(sheet["doc_url"], sheet["url_column_name"])
        DirectoryWebsiteCrud.batch_add_domains(domains)

        print("Added for sheet:", sheet["doc_url"])

    print("All domains added successfully.")