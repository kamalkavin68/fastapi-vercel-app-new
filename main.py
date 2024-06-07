from fastapi import FastAPI

from api.nse.client import NseClient

app = FastAPI()



@app.get("/")
def root():
    return {"detail": f"API running..."}

@app.get("/stocks")
def some():
    nseClient = NseClient()
    allNseStocks = nseClient.getEquityList()
    allNseStocks = [each.dict() for each in allNseStocks]
    return allNseStocks