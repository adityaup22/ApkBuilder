from flask import Flask
from commands import getoutput
import os

app = Flask(__name__)


@app.route('/')
def run_command():
    os.chdir('/home/sportsunity/SportsUnityAndroid')
    cmd = 'sudo ./gradlew assembleDevDebug'
    output = getoutput(cmd)
    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0')
