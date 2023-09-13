from flask import Flask, request, jsonify
import pickle
app = Flask(__name__)

with open('biogas_model','rb') as f:
    __model = pickle.load(f)

with open('expiry-predictor','rb') as f2:
    __model2 = pickle.load(f2)
 
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

@app.route("/getexpiryprob",methods=['POST'])
def get_expiry_prediction():
    foodqty = request.json.get('food_qty')
    food_expiry = request.json.get('food_expiry')
    inp_list = []
    inp_list.append(int(foodqty))
    inp_list.append(int(food_expiry))
    probability = int(__model2.predict([inp_list]))[0]
    print(probability)
    response = jsonify({
        'probability' : probability[0]
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

@app.route("/",methods=['GET'])
def hello():
    return "hi"


if __name__ == "__main__":
    print("Running Python server for Biogas prediction")
    app.run(host='https://sathvik-biogas-predictor.onrender.com', port=5000)

