from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.json  # İstekten veriyi al
    # Veriyi işle (örneğin, karesini al)
    processed_data = data ** 2
    return jsonify({"processed_data": processed_data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
