from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import config 
from patients.routes import patients_router
from web3 import Web3
from utils.contract_helper import MedDataIntegrityContractBridge


w3 = Web3(Web3.HTTPProvider("http://172.17.0.1:7545"))
w3.eth.defaultAccount = w3.eth.accounts[0]

med_data_integrity_contract_bridge = MedDataIntegrityContractBridge(w3)

app = FastAPI()

origins = [
    "http://0.0.0.0"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    patients_router,
    prefix="/med-data-integrity-api/patients",
    tags=["patients"],
    responses={404: {"description": "Not found"}},
)


@app.on_event("startup")
async def app_startup():
    """
    App initialization.
    """    
    print("App has started ...")


@app.on_event("shutdown")
async def app_shutdown():
    """
    App termination.
    """
    config.close_db_client()
    config.close_backup_db_client()
    print( "App termination ...")
    