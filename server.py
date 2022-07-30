#for running a server
from flask import Flask
from flask import send_file
from flask import request

#get classes and properties for preparation of pdf
import exportpdf

#start server flask
app = Flask(__name__)

#define a route for downloading a pdf file, 
@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    try:
        #get all parameters from the url
        #this is the only one required param
        songNumber = request.args.get("songnumber")
        
        songName = exportpdf.makePdfSong(songNumber, request.args)

        #return proper pdf
        return send_file(songName,as_attachment=True)
    except Exception as e:
        return "An error occured: " + str(e) 

@app.route('/')
def home():
    return  """
                <h2>HELLO TO PROSCHOLY PDF EXPORT</h2>
                <h4>for use go to /download_pdf with sufficient params</h4>
            """