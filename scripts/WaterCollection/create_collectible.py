from brownie import (
    network,
    accounts,
    config,
    interface,
    WaterCollection,
)

def main():
    dev = accounts.add(config['wallets']['from_key'])
    water_collection = WaterCollection[-1]
    transaction = water_collection.createCollectible(
        "None", {'from': dev,  "gas_limit": 20740440, "allow_revert": True})
    transaction.wait(45)
    request_id = transaction.events["RequestCollectible"]['requestId']
    token_id = transaction.requestIdToTokenId(request_id)
    print(token_id)


def fund_water_collection(water_collection):
    account = accounts.add(config['wallets']['from_key'])
    link_token = config['networks'][network.show_active()]['link_token']
    interface.LinkTokenInterface(link_token).transfer(
        water_collection.address, 0.25 * 10 ** 18, {"from": account}
    )
    print("Funded WaterCollection contract with 0.25 ETH")