import pickle
from flask import Flask,jsonify,request
import numpy as np

model_D_T = pickle.load(open('fraud_detector_D_T.pkl','rb'))
app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    print('Hi Welcome!')
    print('Request_Result: Connected')
    print('Next_Actions: Get Data from Users')
    return jsonify({
        'Request_Result': str("Connected"),
        'Next_Actions': str("Get Data from Users")
    })

@app.route('/', methods=['POST'])
def predict():
    print('Hello Coders!')

    in_vr = request.form.get('international')
    fl_vr = request.form.get('fail')
    ty_vr = request.form.get('type')
    de_vr = request.form.get('device')
    amount_vr = request.form.get('amount')
    hour_vr = request.form.get('time')

    if in_vr.lower() == 'yes':
        in_vr = 1
    else:
        in_vr = 0

    if fl_vr.lower() == 'yes':
        fl_vr = 1
    else:
        fl_vr = 0

    if ty_vr.lower() == 'online':
        ty_vr = 0
    elif ty_vr.lower() == 'pos':
        ty_vr = 1
    elif ty_vr.lower() == 'atm':
        ty_vr = 2
    elif ty_vr.lower() == 'transfer':
        ty_vr = 3

    if de_vr.lower() == 'tablet':
        de_vr = 0
    elif de_vr.lower() == 'computer':
        de_vr = 1
    elif de_vr.lower() == 'mobile':
        de_vr = 2

    if amount_vr == '' or amount_vr is None:
        return jsonify({
            'Value Error': str(1)
        })
    elif int(amount_vr) < 0:
        return jsonify({
            'Value Error': str(1)
        })
    else:
        am_vr = int(amount_vr)

    if hour_vr == '' or hour_vr is None:
        return jsonify({
            'Value Error': str(2)
        })
    elif int(hour_vr) < 0:
        return jsonify({
            'Value Error': str(3)
        })
    else:
        hr_vr = int(hour_vr)

    input = np.array([[am_vr,in_vr,ty_vr,fl_vr,de_vr,hr_vr]])
    pred_D_T = model_D_T.predict(input)
    pred_score_D_T = model_D_T.predict_proba(input)

    fin_res_D_T = pred_D_T[0]
    risk_score_D_T = pred_score_D_T[0][1]
    print("Fraud_Result: ",fin_res_D_T==1)
    print("Risk_Score: ",int(risk_score_D_T*100))

    return jsonify({
        'Fraud_Result': str(fin_res_D_T==1),
        'Risk_Score': str(int(risk_score_D_T*100))
    })
if __name__ == "__main__":
    app.run()