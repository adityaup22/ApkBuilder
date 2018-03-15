from flask import Flask, request
from commands import getoutput
import os

app = Flask(__name__)


@app.route('/')
def run_command():
    os.chdir('/home/sportsunity/SportsUnityAndroid')
    cmd = 'sudo ./gradlew assembleDevDebug'
    output = getoutput(cmd)
    return output


@app.route('/utm_apk')
def generate_utm_specific_apk():
    CAMPAIGN = request.args.get('CAMPAIGN')
    SOURCE = request.args.get('SOURCE')
    MEDIUM = request.args.get('MEDIUM')
    TERM = request.args.get('TERM')

    print(CAMPAIGN, SOURCE, MEDIUM, TERM)

    data = """
        package com.sports.unity.login.model;

    /**
     * Created by aditya on 15/03/18.
     */

    public class UtmConstants {
        public static final String CAMPAIGN = "{}";
        public static final String SOURCE = "{}";
        public static final String MEDIUM = "{}";
        public static final String TERM = "{}";
    }

        """.format(CAMPAIGN, SOURCE, MEDIUM, TERM)
    f = open('/home/sportsunity/SportsUnityAndroid/app/src/main/java/com/sports/unity/login/model/UtmConstants.java',
             'w')
    f.write(data)
    f.close()


def write_file():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0')
