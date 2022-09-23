# for running a server
from flask import Flask
from flask import send_file
from flask import request
import requests

# get classes and properties for preparation of pdf
from src import core

# const for url address of server for the second flask app
url_of_second_api = ""

# start server flask
app = Flask(__name__)

#define a route for downloading a pdf file, 
@app.route('/export_song_json', methods=['GET'])
def export_song_json():
    """function for exporting desired song

    Returns:
        file : exported song
        In case of exception it returns a warning
    """
    try:
        #get all parameters from the url
        #this is the only one required param
        songNumber = request.args.get("songnumber")
        
        songName = core.exportSongToJson(songNumber, request.args)

        # send json file to the api for format it as required file (pdf or ppt)
        return send_file(songName,as_attachment=True)
        
    except Exception as e:
        print(e)
        return "An error occured. Song probably doesnt exist or parameters were set wrongly."

@app.route('/doc')
def doc():
    """function for handling showing the documentation for this API

    Returns:
        Either file with documentation or string describing error.
    """
    try:
        return send_file('/doc/readme.pdf', as_attachment=True)
    except Exception as e:
        print(e)
        return "An error occured!"

@app.route('/')
def home():
    """function for main window

    Returns:
        html: content shortly describes this API
    """    
    return  """
                <h2>WELCOME TO PROSCHOLY PDF EXPORT</h2>
                <h4>for use of this API go to /export_song with sufficient params</h4>
                <h4>for more info read the <a href="/doc">doc</a>
            """