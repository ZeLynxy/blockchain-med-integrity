import json
from web3 import Web3
from solcx import compile_files
w3 = Web3(Web3.HTTPProvider("http://172.17.0.1:7545"))
w3.eth.default_account = w3.eth.accounts[0]

def deploy_contract(contract_interface):
    contract = w3.eth.contract (
        abi=contract_interface["abi"],
        bytecode=contract_interface["bin"]
    )
    tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt.contractAddress


contracts = compile_files(["med-data-integrity.sol"])
chainvote_contract = contracts.pop("med-data-integrity.sol:MedDataIntegrity")


with open("../med-data-integrity_contract.json", "w") as f:
    data = {
        "abi": chainvote_contract["abi"],
        "contract_address": deploy_contract(chainvote_contract)
    }

    json.dump(data, f, indent=4, sort_keys=True)
    print("Saved contract address")