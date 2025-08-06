from flask import Flask
app = Flask(__name__)
@app.route('/data/appInfo/<name>', methods=['GET'])
def queryDataMessageByName(name):
    print("type(name) : ", type(name))
    return 'String => {}'.format(name)
