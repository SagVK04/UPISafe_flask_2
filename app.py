import pickle
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from flask import Flask, jsonify, request
import pandas as pd

model_rfc = pickle.load(open('fraud_detector.pkl', 'rb'))
tr_label = pickle.load(open('transaction_label.pkl', 'rb'))

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


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    return "".join(y)


@app.route('/', methods=['POST'])
def predict():
    upi_id = request.form.get('upi_id')
    date_input = request.form.get('date')  # DD/MM/YYYY
    time_input = request.form.get('time')  # HH:MM
    amount_input = request.form.get('amount')
    type_input = request.form.get('type')  # Requested/Debited

    upi_id_mod = transform_text(upi_id)
    num_char = len(upi_id_mod)
    amount = float(amount_input)
    date = int(date_input.replace('/', ''))
    time = int(time_input.replace(':', ''))
    type = tr_label.transform([type_input])[0]

    input = pd.DataFrame({
        'num_char_modified': [num_char], 'new_r_id': [upi_id_mod],
        'Amount': [amount], 'Date_mod': [date],
        'Time_mod': [time], 'Type_mod': [type]
    })
    pred_fin_rfc = model_rfc.predict(input)
    pred_fin_score_rfc = model_rfc.predict_proba(input)

    fin_res_rfc = pred_fin_rfc[0]
    risk_score_rfc = pred_fin_score_rfc[0][1]
    print("Fraud_Result: ", fin_res_rfc == 1)
    print("Risk_Score: ", int(risk_score_rfc * 100))

    return jsonify({
        'Fraud_Result': str(fin_res_rfc == 1),
        'Risk_Score': str(int(risk_score_rfc * 100))
    })


if __name__ == "__main__":
    app.run()
