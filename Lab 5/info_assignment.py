from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm
import multiprocessing
import os
import requests

def env_load():
    load_dotenv()
    return os.environ['ACCESS_TOKEN']

def genius(search_term, access_token, per_page=15):
    try:
        genius_search_url = f"http://api.genius.com/search?q={search_term}&" + \
                            f"access_token={access_token}&per_page={per_page}"

        response = requests.get(genius_search_url)
        json_data = response.json()

    except Exception as e:
        print(e)
    return json_data['response']['hits']

def genius_to_df(search_term, access_token, n_results_per_term=10):
    try:
        print(f"Processing iteration for item: {search_term} in process {os.getpid()}")
        json_data = genius(search_term, access_token, per_page=n_results_per_term)
        hits = [hit['result'] for hit in json_data]
        df = pd.DataFrame(hits)

        # expand dictionary elements
        df_stats = df['stats'].apply(pd.Series)
        df_stats.rename(columns={c:'stat_' + c for c in df_stats.columns},
                        inplace=True)
        
        df_primary = df['primary_artist'].apply(pd.Series)
        df_primary.rename(columns={c:'primary_artist_' + c for c in df_primary.columns},
                        inplace=True)
        
        df = pd.concat((df, df_stats, df_primary), axis=1)
        return df
    except Exception as e:
        print(e)

def save_to_csv(df_list):
    res_df = pd.concat(df_list)
    res_df.to_csv('genius_output.csv', index=False, header=True)
    return

if __name__ == "__main__":

    dfs = []
    processes = []
    result_queue = multiprocessing.Queue()

    try:
        access_token = env_load()
        search_terms = ['Taylor Swift', 'One Direction', 'Selena Gomez', 'Harry Styles', 'The Weekend', 'Lana Del Rey', 'Joji', 'Halsey', 'Dua Lipa', 'Ariana Grande']

        for item  in search_terms:
            dfs.append(genius_to_df(item, access_token))

        
        save_to_csv(dfs)
         
    except Exception as e:
        print(e)
