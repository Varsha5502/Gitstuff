import dotenv
import csv
import requests
import time
from multiprocessing import Pool

GENIUS_API_TOKEN = "YOUR_GENIUS_API_TOKEN"

def fetch_data(search_term):
    try:
        url = f"https://api.genius.com/search?q={search_term}"
        headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for '{search_term}': {e}")
        return None

def process_search_term(search_term):
    data = fetch_data(search_term)
    if data:
        # Process data here if needed
        return data
    else:
        return None

def main():
    search_terms = ["Python", "Machine Learning", "Data Science", "Artificial Intelligence"]
    results = []

    # Using multiprocessing for parallel execution
    with Pool(processes=len(search_terms)) as pool:
        results = pool.map(process_search_term, search_terms)

    # Writing results to a CSV file
    with open("genius_search_results.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Search Term", "Result Count", "Results"])
        for search_term, result in zip(search_terms, results):
            if result:
                writer.writerow([search_term, result["meta"]["total"], result["response"]["hits"]])
            else:
                writer.writerow([search_term, "Error", ""])

if __name__ == "__main__":
    main()
