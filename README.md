# Used Car Price Prediction API

A FastAPI-based REST API that predicts the price range of a used car using a trained machine learning model.

**Live API**
https://used-car-prices-project.onrender.com/

**Swagger UI (Web UI)**
https://used-car-prices-project.onrender.com/docs

---

## Features

- Add car details via API
- Retrieve stored car data
- Predict used car price range

---

## API Endpoints

### 1. Root Endpoint

Check if the API is running.

```bash
curl https://used-car-prices-project.onrender.com/
```

### 2. Add Car Data

Add a single car’s details for prediction

```bash
curl -X POST https://used-car-prices-project.onrender.com/add_car/ \
-H "Content-Type: application/json" \
-d '{
  "brand": "Maruti",
  "model": "Swift",
  "km_driven": 45000,
  "seller_type": "Individual",
  "fuel_type": "Petrol",
  "transmission_type": "Manual",
  "mileage": 22.5,
  "engine": 1197,
  "max_power": 82.0,
  "seats": 5,
  "vehicle_age": 5
}'
```

### 3. Get Car Data by ID

Retrieve stored car data using its index

```bash
curl https://used-car-prices-project.onrender.com/cars/0/
```

### 4. Predict Car Price

Predict the price range for the added car

```bash
curl -X POST https://used-car-prices-project.onrender.com/predict_price/
```

### Important Notes

- Only one car should be added before prediction
- API stores data in memory (resets on server restart)
- Transmission type must be 
		Manual
		Automatic
- Seller type must be:
		Dealer
		Trustmark Dealer
		Individual
- All the numeric features must be positive.

---

## Swagger UI

For a UI-based interactive experience, open https://used-car-prices-project.onrender.com/docs