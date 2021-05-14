from fastapi import APIRouter
from bson.objectid import ObjectId
import bcrypt
from config.config import DB
from utils import *
import main

patients_router = APIRouter()
patients = DB.patients

@patients_router.put("/edit")
async def edit_patient(data: dict):
  patient_id = ObjectId(data.get("id"))
  patient = await patients.find_one({"_id": patient_id})
  if patient:
    result = await patients.update_one(
                                        {
                                          "_id": patient_id
                                        },
                                        {
                                          "$set": {
                                            "patient_details": data.get("core_data")
                                          }
                                        }
                                      )
    if result.modified_count > 0:
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
      return {
        "status_code": 2000,
        "detail": patient
      }
    else:
      return {
        "status_code": 1001,
        "detail": "No patient with this id"
      }

  except Exception as e:
    return {
        "status_code": 1000,
        "detail": "Invalid patient id"
    }


