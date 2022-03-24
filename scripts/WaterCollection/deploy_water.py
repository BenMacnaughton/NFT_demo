from brownie import WaterCollection, accounts, network, config

def main():
    dev = accounts.add(config['wallets']['from_key'])
    water_collection = WaterCollection.deploy(
        config['networks'][network.show_active()]['vrf_coordinator'],
        config['networks'][network.show_active()]['link_token'],
        config['networks'][network.show_active()]['keyhash'],
        {'from': dev}
    )