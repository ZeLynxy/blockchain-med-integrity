import json

class MedDataIntegrityContractBridge:
    def __init__(self, w3_instance):
        self.w3 = w3_instance
        with open("../med-data-integrity_contract.json", "r") as f:
            contract_data = json.load(f)
            abi = contract_data["abi"]
            self.contract_address = contract_data["contract_address"]
            self.med_data_integrity_contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(self.contract_address), abi=abi)

    def write_patient_data(self, patientID, hashData):
        tx_hash = self.med_data_integrity_contract.functions.writePatientData(patientID, hashData).transact()
        receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return receipt
    
    def integrity_is_compromised(self, patientID, hashData):
      return not self.med_data_integrity_contract.functions.checkIntegrity(patientID, hashData).call()