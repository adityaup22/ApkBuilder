from flask import Flask, request, send_from_directory, render_template, make_response
from commands import getstatusoutput
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})


def run_command():
    os.chdir('/home/sportsunity/SportsUnityAndroid')
    cmd = 'sudo ./gradlew assembleDevDebug'
    output = getstatusoutput(cmd)
    return output


def write_utm_file(campaign, source, medium, term):
    data = """
            package com.sports.unity.login.model;

        /**
         * Created by aditya on 15/03/18.
         */

        public class UtmConstants {{
            public static final String CAMPAIGN = "{0}";
            public static final String SOURCE = "{1}";
            public static final String MEDIUM = "{2}";
            public static final String TERM = "{3}";
        }}

            """.format(campaign, source, medium, term)
    f = open('/home/sportsunity/SportsUnityAndroid/app/src/main/java/com/sports/unity/login/model/UtmConstants.java',
             'w')
    f.write(data)
    f.close()


@app.route('/utm_apk')
def generate_utm_specific_apk():
    # Getting Campaign Params From Url
    campaign = request.args.get('campaign')
    source = request.args.get('source')
    medium = request.args.get('medium')
    term = request.args.get('term')
    # -- #

    write_utm_file(campaign=campaign, source=source, medium=medium, term=term)

    out = run_command()

    if out[0] == 0:
        for i in os.listdir('/home/sportsunity/SportsUnityAndroid/app/build/outputs/apk/dev/debug'):
            if i.endswith('.apk'):
                print i
                return send_from_directory(
                    directory='/home/sportsunity/SportsUnityAndroid/app/build/outputs/apk/dev/debug',
                    filename=str(i), as_attachment=True)
        return 'No File Found'
    else:
        return out[1]


@app.route('/download')
def send_file():
    # os.chdir('/Users/aditya/Downloads')
    for i in os.listdir('/home/sportsunity/SportsUnityAndroid/app/build/outputs/apk/dev/debug'):
        if i.endswith('.apk'):
            return send_from_directory(directory='/home/sportsunity/SportsUnityAndroid/app/build/outputs/apk/dev/debug',
                                       filename=str(i), as_attachment=True)
    return 'No File'


@app.route('/test')
def html():
    client_ip = str(request.remote_addr)
    device = str(request.headers['User-Agent']).split('(')[1].split(')')[0]

    print client_ip + device
    # respone = make_response(render_template(template_name_or_list="init.html"))
    # respone.headers['Set-Cookie'] = 'fileDownload=true; path=/'
    # respone.set_cookie('fileDownload', True)
    response = (client_ip + device).encode('base64', 'strict')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
