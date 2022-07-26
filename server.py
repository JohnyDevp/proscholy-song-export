#for running a server
from flask import Flask
from flask import send_file


if __name__ == "__name__":
    #start server flask
    app = Flask(__name__)

    #define a route for downloading a pdf file, 
    #TODO there should be a params specification for more sufficient file according to specifications
    @app.route('/download_pdf/')
    def download_pdf():
        try:
            return send_file('./out.txt',as_attachment=True)
        except Exception as e:
            return str(e)
