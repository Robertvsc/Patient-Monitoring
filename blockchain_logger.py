from web3 import Web3
import json

# Conectare la Ganache local (sau Remix VM în browserul tău)
ganache_url = "http://127.0.0.1:7545"  # <- modifică doar dacă folosești alt port
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Verificăm conexiunea
if not web3.is_connected():
    raise Exception("❌ Nu se poate conecta la blockchain-ul local (Ganache).")

# Adresa contractului tău din Remix
contract_address = Web3.to_checksum_address("0x7EF2e0048f5bAeDe046f6BF797943daF4ED8CB47")

# ABI copiat din Remix
contract_abi = [
	{
		"anonymous": False,
		"inputs": [
			{"indexed": False, "internalType": "string", "name": "message", "type": "string"},
			{"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
		],
		"name": "AlertLogged",
		"type": "event"
	},
	{
		"inputs": [
			{"internalType": "string", "name": "_message", "type": "string"}
		],
		"name": "logAlert",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

# Creăm instanța contractului
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Folosim primul cont din Ganache (sau Remix VM)
web3.eth.default_account = web3.eth.accounts[0]

# Funcție de logare alertă în blockchain
def log_alert_in_blockchain(message: str):
    try:
        tx_hash = contract.functions.logAlert(message).transact()
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✅ Alertă logată în blockchain! Tx hash: {tx_hash.hex()}")
    except Exception as e:
        print(f"❌ Eroare la logarea în blockchain: {str(e)}")
