#for making a graphql request and further result get
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

#for converting json into pdf
import jpype
jpype.startJVM() 

#regex
import re

# my module for color for string
from props import bcolors

# song object
from song import Song


#FOR WINDOWS======================================================
# path_wkhtmltopdf = r"C:\\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

#constants
PROSCHOLY_PATH = "https://zpevnik.proscholy.cz/graphql"    
    
def exportSongToJson(songNumber, rest_of_params):
    """callable function for creating asked song json export

    Args:
        
        songNumber (int): id of song in database of proscholy.cz
        rest_of_params (dict): meaning optional params, which include resX, resY,songFormat, outFormat

    Returns:
        string : name of exported song file
    """

    try:
        #extract the rest of the param
        params = extractOptionalParams(rest_of_params)

        #then download desired song
        downloadedSong = downloadSong(songNumber)

        #extract song text and song name
        downloadedSongText = downloadedSong['lyrics_no_chords_no_comments']
        downloadedSongName = downloadedSong['name']
        
        #create a proper song object, which handle the rest
        songObject = Song(downloadedSongText, downloadedSongName, params)

        #create proper output file, get its name and return it
        return songObject.exportJson()
        
    except Exception as e:
        print(bcolors.WARNING + "An error occured: " + str(e) + bcolors.ENDC)
        print(bcolors.FAIL + "Song may not exist" + bcolors.ENDC)
        return False

def extractOptionalParams(rest_of_params):
    """extract the rest of the params, possible params are: \n
    resx - for X component of resolution of the output screen \n
    resy - for Y component of resolution of the output screen \n
    fileformat - either pdf or ppt \n
    songformat - consisting of numbers, B (bridge), R, C (chorus) - how the text should go \n
    songnumber

    Args:
        rest_of_params (__dict__): array of params
    
    Returns:
        array : all optional parameters with their set or default values

    """

    #set up default params for every possible params
    resX = 0
    resY = 0
    fileFormat = 'pdf'
    songFormat = 0
    
    #check whether params were set and check for their correctness
    if 'resx' in rest_of_params : 
        if str(rest_of_params['resx']).isnumeric() : resX = rest_of_params['resx']
    if 'resx' in rest_of_params : 
        if str(rest_of_params['resy']).isnumeric() : resY = rest_of_params['resy']
    if 'fileformat' in rest_of_params : 
        if str(rest_of_params['fileformat']) in ['pdf', 'ppt'] : fileFormat = rest_of_params['fileformat']
    if 'songformat' in rest_of_params :
        pattern = re.compile("[0-9BbRrCc]+")
        if pattern.fullmatch(str(rest_of_params['songformat'])) : songFormat = rest_of_params['songformat']
    
    retArray = {
        "resx" : resX,
        "resy" : resY,
        "fileformat" : fileFormat,
        "songformat" : songFormat,
        "songnumber" : rest_of_params['songnumber']
    }

    #return the prepared array
    return retArray

def downloadSong(songNumber):   
    """private function for downloading song

    Args:
        songNumber (int): id of song in database of proscholy.cz

    Returns:
        Array with result
    """
    transport = AIOHTTPTransport(url=PROSCHOLY_PATH)
    
    #create client from 
    client = Client(transport=transport, fetch_schema_from_transport=True)

    #create query
    query = gql(
        """
            query getSongLyrics ($id: ID!) {
                song_lyric(id: $id){
                    id
                    name
                    lyrics_no_chords_no_comments
                }
            } 
        """
    )

    params = {"id" : songNumber}
    
    result = client.execute(query, variable_values=params)
    
    return result['song_lyric']

