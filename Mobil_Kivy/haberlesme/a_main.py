from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/send_data', methods=['POST'])
def send_data():
    data = 5  # İstekten veriyi al
    # İkinci uygulamaya veriyi gönder
    response = requests.post('http://192.168.0.103:5001/process_data', json=data)
    # Üçüncü uygulamaya veriyi gönder
    response = requests.post('http://192.168.0.103:5002/process_data', json=data)
    return jsonify({"message": "Veri başarıyla gönderildi."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
