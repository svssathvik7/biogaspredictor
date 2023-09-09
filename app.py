from flask import Flask, request, jsonify
import pickle
app = Flask(__name__)

with open('biogas_model','rb') as f:
    __model = pickle.load(f)
 
@app.route('/getprediction',methods=['POST'])
def get_biogas_prediction():
    x = request.json.get('food_waste')
    if float(x) == 0:
        response = jsonify({
            'estimation' : 0
        })
    else:
        response = jsonify({
            'estimation' : round(__model.predict([[float(x)]])[0],2)
        })
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

@app.route("/",methods=['GET'])
def hello():
    return "hi"


if __name__ == "__main__":
    print("Running Python server for Biogas prediction")
    app.run(host='0.0.0.0', port=5000)

