from flask import Flask, request

app = Flask(__name__)

response = ""


@app.route('/ussd/am', methods=['POST', 'GET'])
def ussd_callback():
    global response
    
    if request.method == 'GET':
        try:
            session_id = request.args['sessionId']
            service_code = request.args['serviceCode']
            phone_number = request.args['phoneNumber']
            text = request.args['text']
        except KeyError:
            return '''
                CON Welcome to the USSD testing interface
                Send POST requests with the following parameters:
                - sessionId
                - serviceCode
                - phoneNumber
                - text
            '''
    else:
        # Handle JSON POST data
        if not request.is_json:
            return "Content-Type must be application/json", 400
            
        try:
            data = request.get_json()
            if data is None:
                session_id = ''
                service_code = ''
                phone_number = ''
                text = ''
            else:
                session_id = data.get('sessionId', '')
                service_code = data.get('serviceCode', '')
                phone_number = data.get('phoneNumber', '')
                text = data.get('text', '')
        except Exception:
            session_id = ''
            service_code = ''
            phone_number = ''
            text = ''

    if text == '':
        response = '''
            CON What would you want to check\n
            1. My Account\n
            2. My phone number\n
        '''
    elif text == '1':
        response = '''
            CON Choose account information you want to view\n
            1. Account number\n
            2. Account balance\n
        '''
    elif text == '1*1':
        account_number = "ACC10001"
        response = "END Your account number is " + account_number
    elif text == "1*2":
        balance = "MWK 10,000"
        response = "END Your balance is " + balance
    elif text == '2':
        response = "END This is your phone number " + phone_number

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
