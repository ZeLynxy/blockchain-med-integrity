import datetime

async def update_patient(patients_collection, patient_id, data, upsert=False, last_update=None):
  if not last_update:
    last_update = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  result = await patients_collection.update_one(
                                  {
                                    "_id": patient_id
                                  },
                                  {
                                    "$set": {
                                      "patient_details": data.get("core_data"),
                                      "updated_on": last_update,
                                    }
                                  },
                                  upsert = upsert
                                )
  return result