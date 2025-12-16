from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# Creating the API app
app = FastAPI()

# Storing car data in list
car_data = []

#Loading the saved model
model = joblib.load("./models/used_car_price_model.pkl")

# Creating Pydantic model for car data
class Car(BaseModel):
    brand : str
    model : str
    km_driven : int
    seller_type : str
    fuel_type : str
    transmission_type : str
    mileage : float
    engine : int
    max_power : float
    seats : int
    vehicle_age : int

# API Endpoints

# Root endpoint
@app.get("/")
def read_root():
    return {"message" : "Welcome to the Used Car Prices Prediction API!"}

# Add car data endpoint
# Used to add car data for prediction
@app.post("/add_car/")
def add_car(car : Car):
    car_data.append(car)
    return {"message" : "Car data added successfully", "car" : car}

# Get car data endpoint
# Used to get car data by index
@app.get("/cars/{car_id}/", response_model = Car)
def get_car(car_id : int):
    if car_id < 0 or car_id >= len(car_data):
        raise HTTPException(status_code = 404, detail = "Car not found")
    return car_data[car_id]

# Predict price endpoint
# Used to predict price of the car based on the provided data
@app.post("/predict_price/")
def get_prediction():
    if not car_data:
        raise HTTPException(status_code = 400, detail = "No car data available for prediction")
    
    if len(car_data) > 1:
        raise HTTPException(status_code = 400, detail = "Please provide only one car data for prediction")
    
    car = car_data[0]
    
    if car.km_driven < 0 or car.mileage < 0 or car.engine < 0 or car.max_power < 0 or car.seats <= 0 or car.vehicle_age < 0:
        raise HTTPException(status_code = 400, detail = "Invalid car data values")
    
    car.brand = car.brand.capitalize()
    car.model = car.model.capitalize()
    car.seller_type = car.seller_type.capitalize()
    car.fuel_type = car.fuel_type.capitalize()
    
    if car.transmission_type.lower() not in ['manual', 'automatic']:
        raise HTTPException(status_code = 400, detail = "Invalid transmission type. Must be 'Manual' or 'Automatic'")
    
    if car.seller_type not in ['Individual', 'Dealer', 'Trustmark Dealer']:
        raise HTTPException(status_code = 400, detail = "Invalid seller type. Must be 'Individual', 'Dealer'")
    
    input_data = pd.DataFrame([car.dict()])
    
    try:
        predicted_price = model.predict(input_data)
        price_range = [np.round(predicted_price[0] - 90000, 2), np.round(predicted_price[0] + 90000, 2)]
        return {"Predcited Price Range" : price_range}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = f"Prediction error: {str(e)}")

