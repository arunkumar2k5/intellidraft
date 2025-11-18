import os
import shutil
import csv
import logging
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth
import json
from pathlib import Path


def digikey_search(uniq, on_progress=None):
    try:
            #Li = [p.strip() for p in lis1.split(',') if p.strip()]
            Li= uniq
            
            fin_11 = []
            total = len(Li) if hasattr(Li, "__len__") else 0
            done = 0
            #Step 1: Get access token
            client_id = "0dhv3AZgnR9XJnjvVs8RMwI5c2aWbUNA"
            client_secret = "bKXnVOBACsXedDa5"
            auth_url = "https://api.digikey.com/v1/oauth2/token"
            data = {
                "grant_type": "client_credentials"
            }

            token_response = requests.post(auth_url, data=data, auth=HTTPBasicAuth(client_id, client_secret))

            if token_response.status_code == 200:
                access_token = token_response.json()["access_token"]
                print("Access token received.")
            else:
                print("Token error:", token_response.text)
                access_token = None
            part_list = Li

            if access_token:
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "X-DIGIKEY-Client-Id": client_id,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
                product_url = "https://api.digikey.com/products/v4/search/keyword"
                #part_number = "GCM1885C1H180JA16D"
                miss = []

                for part in range(len(part_list)):
                    body = {
                        "keywords": part_list[part],
                        "recordCount": 1
                    }

                    response = requests.post(product_url, headers=headers, json=body)
                    specs = {"Part Number": part_list[part].upper()}

                    if response.status_code == 200:
                        result = response.json()
                        print("Search result:", result)
                        if result['Products'] == []:
                            miss.append(part)
                            done += 1
                            if on_progress is not None and total:
                                on_progress(done, total)
                        else:
                            pr = result['Products'][0]["Parameters"]
                            specs["Mfr"] = result['Products'][0]['Manufacturer']['Name']
                            specs["Part Status"] = result['Products'][0]['ProductStatus']['Status']
                            for e in pr:
                                specs[e['ParameterText']] = e["ValueText"]
                            fin_11.append(specs)
                            done += 1
                            if on_progress is not None and total:
                                on_progress(done, total)
                    else:
                        print("Search error:", response.text)
                        done += 1
                        if on_progress is not None and total:
                            on_progress(done, total)
            p_1 = [pd.DataFrame(d.items(), columns=["Attribute", "Value"]) for d in fin_11]
            
            
            # with open('parts1.json', 'w', encoding='utf-8') as json_file:
            #     json.dump(fin_11, json_file, indent=2, ensure_ascii=False)
            # print(fin_11)
            # print("parts.json has been created successfully!")
            out_path = Path(__file__).parent / "parts.json"
            with out_path.open('w', encoding='utf-8') as json_file:
                json.dump(fin_11, json_file, indent=2, ensure_ascii=False)

            print(f"parts.json has been created successfully at: {out_path.resolve()}")
    except Exception as e: #genai
        print("Error:", e)
    return uniq