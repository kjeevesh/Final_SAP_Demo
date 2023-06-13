from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/submitData', methods=['POST'])
def submit_data():
    data = request.json

    # Perform any necessary operations with the received data
    # ...

    # Prepare the response JSON data
    response_data = {
        'message': 'Data received successfully',
        'data': data
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run()
