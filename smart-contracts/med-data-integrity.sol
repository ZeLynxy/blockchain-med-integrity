pragma solidity >=0.7.4;
pragma experimental ABIEncoderV2;

contract MedDataIntegrity {
    struct Patient {
        bytes32 id;
        bytes32 hashData;
    }
 
    mapping (bytes32 => Patient) patients;
    
    function writePatientData(string memory patientID, string memory hashData) public {
        bytes32 id = keccak256(abi.encodePacked(patientID));    
        bytes32 actualHashData = keccak256(abi.encodePacked(hashData));   
        patients[id] = Patient(id, actualHashData);
    }

    function checkIntegrity(string memory patientID, string memory patientHashData) external view returns (bool) {
      bytes32 id = keccak256(abi.encodePacked(patientID));
      return patients[id].hashData == keccak256(abi.encodePacked(patientHashData)) ? true: false;
    }
}