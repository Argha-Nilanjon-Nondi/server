from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route('/api/upload', methods=['POST'])
def example():
  name = request.args.get('name')
  if name:
    message = f'Hello, {name}!'
  else:
    message = 'Hello, stranger!'
  
  response = {'message': message}
  return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
