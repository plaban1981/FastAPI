# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:40:41 2020

@author: win10
"""

# 1. Library imports
import uvicorn
from fastapi import FastAPI,File,UploadFile
from fastapi.responses import StreamingResponse
from BankNotes import BankNote
import numpy as np
import pickle
import pandas as pd
import json
import io
# 2. Create the app object
app = FastAPI()
pickle_in = open("classifier.pkl","rb")
classifier=pickle.load(pickle_in)

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, World'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To Krish Youtube Channel': f'{name}'}

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted Bank Note with the confidence
@app.post('/predict')
def predict_banknote(data:BankNote):
    data = data.dict()
    variance=data['variance']
    skewness=data['skewness']
    curtosis=data['curtosis']
    entropy=data['entropy']
   # print(classifier.predict([[variance,skewness,curtosis,entropy]]))
    prediction = classifier.predict([[variance,skewness,curtosis,entropy]])
    if(prediction[0]>0.5):
        prediction="Fake note"
    else:
        prediction="Its a Bank note"
    return {
        'prediction': prediction
    }
def convertBytesToString(bytes):
    
    data = bytes.decode('utf-8').splitlines()
    print(type(data))
    df = pd.DataFrame(data)
    list1 = df.values.tolist()[0]
    list2 = df.values.tolist()[1:]
    df1 = pd.DataFrame(list2,columns=list1)
    val1 = []
    val2 = []
    val3 = []
    val4 = []
    for item in list2:
      
        val1.append(float(item[0].split(",")[0]))
        val2.append(float(item[0].split(",")[1]))
        val3.append(float(item[0].split(",")[2]))
        val4.append(float(item[0].split(",")[3]))
    var1,var2,var3,var4 = list1[0].split(",")[0],list1[0].split(",")[1],list1[0].split(",")[2],list1[0].split(",")[3]
    df1 = pd.DataFrame({var1:val1,var2:val2,var3:val3,var4:val4})
    print(df1.info())
    print(df1)
    return df1
def parse_csv(bytes):
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    return parsed 

@app.post("/csv")
async def parsecsv(file:UploadFile = File("test.csv")):
    contents = await file.read()
    test_data  = convertBytesToString(contents)
    print(test_data.head())
    # print(classifier.predict([[variance,skewness,curtosis,entropy]]))
    predictions = classifier.predict(test_data)
    preds = []
    for i in predictions :
      if(i > 0.5):
         preds.append("Fake note")
      else:
         preds.append("Bank note")
    test_data['predicted_class']  = preds
    response = StreamingResponse(io.StringIO(test_data.to_csv("fatapi_predictions.csv",index=False)), media_type="text/csv")
    return response

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload