from fastapi import APIRouter
from bson.objectid import ObjectId
from config.config import DB, BACK_UP_DB
from utils import *
import main
import datetime
from .utils import update_patient

patients_router = APIRouter()
patients = DB.patients
patients_backup = BACK_UP_DB.patients

@patients_router.put("/edit")
async def edit_patient(data: dict):
  patient_id = ObjectId(data.get("id"))
  patient = await patients.find_one({"_id": patient_id})
  if patient:
    result = await update_patient(patients, patient_id, data)
    if result.modified_count > 0:
      patients_backup.update_one(
                                  {
                                    "_id": patient_id
                                  },
                                  {
                                    "$set": {
                                      "patient_details": data.get("core_data"),
                                      "updated_on": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    }
                                  },
                                  upsert=True
                                )
      patient = await patients.find_one({"_id": patient_id})
      last_update = patient.get("updated_on")

      # Save in backup database
      await update_patient(patients_backup, patient.get("_id"), data, upsert=True, last_update=last_update)
      patient["_id"] = str(patient["_id"])
      print("Successfully wrote in backup DB")


      # Update patient data hash on blockchain
      receipt = main.med_data_integrity_contract_bridge.write_patient_data(patient["_id"], hashData(patient))
      print(receipt)

      return {
        "status_code": 2000,
        "detail": "Patient information  is successfully modified"
      }
    else:
      return {
        "status_code": 1001,
        "detail": "An error occurred while modifying patient information"
      }
  else:
    return {
      "status_code": 1000,
      "detail": "Failed to retrieve this patient"
    }


@patients_router.get("/{patient_id}")
async def get_patient(patient_id: str):
  
  try:
    patient_id = ObjectId(patient_id)
    patient =  await patients.find_one({"_id": patient_id})
    if patient:
      patient["_id"] = str(patient["_id"])
      if not main.med_data_integrity_contract_bridge.integrity_is_compromised(patient.get("_id"), hashData(patient)):
        return {
          "status_code": 2000,
          "detail": patient
        }
      else:
        #Rollback
        patient = await patients_backup.find_one({"_id": patient_id})
        data = {}
        data["core_data"] = patient.get("patient_details")
        last_update = patient.get("updated_on")
        result = await update_patient(patients, patient_id, data, upsert=False, last_update=last_update)
        if result.modified_count > 0:
          patient["_id"] = str(patient["_id"])
          return {
            "status_code": 2001,
            "alert": "The patient data integrity has been compromised but successfully updated from backup database",
            "detail": patient
          }
        else:
          return {
            "status_code": 1002,
            "detail": "Patient data integrity compromised. The patient data with this ID cannot been reverted back from backup database"
          }

    else:
      patient = await patients_backup.find_one({"_id": patient_id})
      if patient:
        #Rollback

        data = {}
        data["core_data"] = patient.get("patient_details")
        last_update = patient.get("updated_on")
        result = await update_patient(patients, patient_id, data, upsert=True, last_update=last_update)
        if result.upserted_id:
          patient["_id"] = str(patient["_id"])
          return {
            "status_code": 2002,
            "alert": "The patient data integrity has been compromised. The record data has been deleted from the principal database, but successfully reverted back from backup database",
            "detail": patient
          }
        else:
          return {
            "status_code": 1003,
            "detail": "Patient data integrity compromised. The patient data with this ID cannot been reverted back from backup database"
          }
      else:
        return {
          "status_code": 1001,
          "detail": "No patient with this id"
        }

  except Exception as e:
    print(e)
    return {
        "status_code": 1000,
        "detail": "Invalid patient id"
    }


