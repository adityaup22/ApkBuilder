from flask import Flask, request, send_from_directory
from commands import getstatusoutput
import os

app = Flask(__name__)


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
    data = """
    <!DOCTYPE html>
<html>
<head>
<script>
window.location="http://192.168.0.11:5000/utm_apk?campaign=aditya&source=unchi&medium=english&term=mid" 
</script>
</head>
<body>
<img src="https://www.tes.com/lessons/hI4HX9oibSNFSA/et-words">
</body>
</html>
    """
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0')
