import requests
import os
from brownie import WaterCollection, network
from metadata import metadata_template
from pathlib import Path
import json

def main():
    water_collection = WaterCollection[-1]
    num_tokens = water_collection.tokenCounter()
    write_metadata(water_collection, num_tokens)


def write_metadata(contract, num_tokens):
    meta_data_hahes = []
    for token_id in range(num_tokens):
        net = network.show_active()
        collectible_metadata = metadata_template.template
        meta_data_filename = f"metadata/{net}/{token_id}.json"
        if Path(meta_data_filename).exists():
            print(f"Metadata file {meta_data_filename} already exists.")
        else:
            collectible_metadata["name"] = contract.tokenName(token_id)
            collectible_metadata["description"] = "Wata"
            img_path = f"images/{token_id}.png"
            image = upload_to_ipfs(img_path)
            collectible_metadata["image"] = image
            with open(meta_data_filename, "w") as f:
                json.dump(collectible_metadata, f)
            meta_data_hahes.append(upload_to_ipfs(meta_data_filename))
    return meta_data_hahes


def upload_to_ipfs(img_path):
    with Path(img_path).open("rb") as f:
        img_binary = f.read()
        pinata_api_key = os.environ["PINATA_API_KEY"]
        pinata_api_secret = os.environ["PINATA_API_SECRET"]
        endpoint = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        headers = {
            'pinata_api_key': pinata_api_key,
            'pinata_api_secret': pinata_api_secret
        }
        body = {
            'file': img_binary
        }
        response = requests.post(endpoint, headers=headers, files=body)
        return response.json()["IpfsHash"]
        
