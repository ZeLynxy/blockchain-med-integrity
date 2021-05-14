import datetime
from fastapi_mail import FastMail, MessageSchema
from config.config import EMAIL_CONF

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


class EmailSender(FastMail):
    def __init__(self):
        super().__init__(EMAIL_CONF)

    async def send_message(self, subject, recipients, body):
        print(f"{subject=}, {recipients=}, {body=}")
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
        )
        await super().send_message(message)

async def alert_admin(email, patient_id):
    await EmailSender().send_message(
        "ALERT - Patient data compromised", 
        email,
        f"The data of the patient of ID {patient_id} has been compromised. Take necessary actions to resolve the issue."
    )