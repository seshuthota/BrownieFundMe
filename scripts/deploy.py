from brownie import FundMe, config, MockV3Aggregator, network
from scripts.utils import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_fund_me():
    account = get_account()
    # if we are on a persisted network like rinkeby use the associated address
    # otherwise, deploy mocks
    price_feed_address = ""
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(price_feed_address, {"from": account},
                            publish_source=config["networks"][network.show_active()].get("verify"))
    print(f"Contract deployed to {fund_me}")
    return fund_me


def main():
    deploy_fund_me()
