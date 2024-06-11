from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["kanomDB"]
product = db["product"]
history = db["history"]

class Product(BaseModel):
    barcode: str
    name: str
    price: int

class History(BaseModel):
    product_list: dict
    total: int

# ***********************Create*************************

@app.post("/kanom")
async def add_kanom(kanom: Product):
    result = product.insert_one(kanom.dict())
    return {
        "barcode": kanom.barcode,
        "name": kanom.name,
        "price": kanom.price
    }

@app.post("/history")
async def add_history(history_dt: History):
    result = history.insert_one(history_dt.dict())
    return {
        "product_list": history_dt.product_list,
        "total": history_dt.total
    }

# ***********************Read*************************

@app.get("/kanom/{barcode}")
async def read_kanom(barcode: str):
    result = product.find_one({"barcode": barcode})
    if result:
        return {
            "barcode": result["barcode"],
            "name": result["name"],
            "price": result["price"]
        }
    else:
        raise HTTPException(status_code=404, detail="Kanom not found")
    
# ***********************Update*************************

#update both
@app.put("/kanom/{barcode}")
async def update_kanom(barcode: str, new_name: str, new_price: int):
    result = product.update_one(
        {"barcode": barcode}, {"$set": {"name": new_name, "price": new_price}}
    )
    if result.modified_count >= 1:
        return {
            "barcode": barcode,
            "name": new_name,
            "price": new_price
        }
    else:
        raise HTTPException(status_code=404, detail="Kanom not found")

#update name
@app.put("/kanom/name/{barcode}")
async def update_name_kanom(barcode: str, new_name: str):
    result = product.update_one(
        {"barcode": barcode}, {"$set": {"name": new_name}}
    )
    if result.modified_count >= 1:
        return {
            "barcode": barcode,
            "name": new_name,
        }
    else:
        raise HTTPException(status_code=404, detail="Kanom not found")

#update price
@app.put("/kanom/price/{barcode}")
async def update_price_kanom(barcode: str, new_price: int):
    result = product.update_one(
        {"barcode": barcode}, {"$set": {"price": new_price}}
    )
    if result.modified_count >= 1:
        return {
            "barcode": barcode,
            "price": new_price
        }
    else:
        raise HTTPException(status_code=404, detail="Kanom not found")

# ***********************Delete*************************

@app.delete("/kanom/{barcode}")
async def delete_kanom(barcode: str):
    result = product.delete_one({"barcode": barcode})
    if result.deleted_count == 1:
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=404, detail="Kanom not found")
    
