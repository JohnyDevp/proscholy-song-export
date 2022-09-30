# for running a server
import base64
from flask import Flask
from flask import send_file
from flask import request
from io import BytesIO
import requests, json
import threading
import time

# get classes and properties for preparation of pdf
from src import core, props
from props import bcolors

# const for url address of server for the second flask app
url_of_second_api = "http://127.0.0.1:3000/data_to_file_export"

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
        
        song_data_json_format = core.exportSongToJson(songNumber, request.args)
        
        # get the file-export format (pdf | ppt) for future possibility of decoding file received from the second API
        export_format = song_data_json_format['file']['export-format']
        match export_format:
            case 'rawpdf':
                export_format='pdf'
            case _:
                export_format = export_format

        # get song name for reason written right above
        song_name = song_data_json_format['file']['name']

        # send json file to the api to format the song as required (pdf or ppt)
        # res will handle the content of the exported file
        
        res = requests.post(url_of_second_api, json=json.dumps(song_data_json_format))
        if res.ok:
            # straight write received bytes (from res) to a file according to an extension
            with open(song_name+'.'+export_format, 'wb') as f:
                f.write(res.content)
            
            # when all is written then start a function, which will remove the file after 10s (# FIXME countdown)
            threading.Timer(10, props.remove_exported_files).start()
            
            # then send file
            return send_file(song_name+'.'+export_format, as_attachment=True)
        else:
            raise Exception

    except Exception as e:
        print(e)
        return "An error occured. Song probably doesnt exist, parameters were set wrongly or there's an internal server error."

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