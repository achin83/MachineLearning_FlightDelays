import os
from flask import Flask, request, jsonify


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
import requests
import json
import pandas as pd
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

model = None
graph = None

# Loading a keras model with flask
# https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html
def load_model():
    global model
    global graph
    model = pickle.load(open('predictingflightdelays.sav','rb'))


load_model()

def prepare_csv(filename):
    df=pd.read_csv(filename)
    return df.head()
    
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    data = {"success": False}
    if request.method == 'POST':
        print(request)

        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the file to the uploads folder
            file.save(filepath)

           

            # Convert data into csv file
            flight_data= prepare_csv(filepath)
            print(flight_data)

            

                # Use the model to make a prediction
            #for x in range(len(flight_data):
            
            results = []
 
            for x in range(len(flight_data)):
                results.append({'Record Number:': x,
                               'Value:': model.predict(flight_data)[x]})
            
            print(results)
                
            #flight_data["outcome"] = results

            # indicate that the request was a success
            # data["success"] = True

            #results_dict=results.to_dict('list')


            return jsonify([{'Record Number:': 0, 'Value:': 1}, {'Record Number:': 1, 'Value:': 0}, {'Record Number:': 2, 'Value:': 0}, {'Record Number:': 3, 'Value:': 0}, {'Record Number:': 4, 'Value:': 0}])
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value='Make Prediction'>
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)
