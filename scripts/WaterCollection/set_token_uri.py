from brownie import WaterCollection, accounts, config
from scripts.WaterCollection.create_metadata import write_metadata

OPEN_SEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def main():
    water_collection = WaterCollection[-1]
    num_tokens = water_collection.tokenCounter()
    meta_data_hashes = write_metadata(water_collection, num_tokens)
    for token_id in range(num_tokens):
        if water_collection.tokenURI(token_id) == "None":
            token_uri = meta_data_hashes[token_id]
            set_token_uri(water_collection, token_id, token_uri)


def set_token_uri(contract, token_id, token_uri):
    owner = accounts.add(config['wallets']['from_key'])
    transaction = contract.setTokenURI(token_id, token_uri, {'from': owner})
    transaction.wait(3)
    request_id = transaction.events["RequestSetTokenURI"]['requestId']
    token_id = transaction.requestIdToTokenId(request_id)
    print(f"Token {token_id} URI set to {token_uri}")
    print(f"OpenSea URI: {OPEN_SEA_FORMAT.format(contract.address, token_id)}")