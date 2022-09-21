#for making a graphql request and further result get
from distutils.command.build import build
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


#for converting json into pdf
import jpype
jpype.startJVM() 
import pdfkit

#regex
import re

#my module for color for string
from props import bcolors

#constants
PROSCHOLY_PATH = "https://zpevnik.proscholy.cz/graphql"

HTML_HEAD = """
    <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body> """ 

HTML_FOOT = """
    </body>
    </html>
"""

class Song:
    """
    object handling exporting song \n
    here will be done every formating and preparation for final export
    """

    finalSongString = ""

    def __init__(self, songText, songName, params):
        """constructor

        Args:
            songText (string): plain text of the song
            songName (string): name of the song
            params (array): all params set or with default value
        """
        self.songText = songText # load text of song
        self.songName = songName # song name
        self.params = params # params defining the requirements for the output

    def __putSongInOrder(self):
        """it takes the song plain text and according to the param of song-format puts
        the verses into the right order
        """
        
        # check whether it should be in some specific order or not
        if self.params['songformat'] == 0 :
            # it should be only in its default variant
            self.finalSongString = self.songText
            return

        
        # split all verses, bridges and chorus in the song according to their signs
        songTextInParts = re.split("[0-9]+[:.]|[R][:.]|[C][:.]|[B][:.]", self.songText)
        songTextInParts.pop(0) # pop the first blank space in array
        # get the verses numbers from the lyrics, so the verses above could be find
        versesNumbers = re.findall("[0-9]+[:.]|[R][:.]|[C][:.]|[B][:.]", self.songText)

        # go through the string representing the desired song format (i.e. verses order)
        buildedSong = "" # here will be builded the final form of the song
        for part in self.params['songformat']:
            try:
                for i in versesNumbers: # find the desired part in existing parts found in song
                    if part in i : # if the sign of the verse is found, then add the verse to the final song form
                        verseSign = i
                        verseIndex = versesNumbers.index(verseSign)
                        buildedSong += verseSign + ' ' + songTextInParts[verseIndex].strip()
                        buildedSong += '\n' # append new line after each verse
                        break         
            except Exception as e:
                print(str(e)) # print into the terminal if any exception occurs

        # load the builded song into the variable for the final representation
        self.finalSongString = buildedSong

    def exportJson(self) :
        """method generating json file with text and display options

        Returns:
            string : file name with its extension
        """

        # handle the song format - how the verses should go
        self.__putSongInOrder()

        # handle the file format
        if self.params['fileformat'] == 'pdf' : 
            
            pdfkit.from_string(HTML_HEAD + self.finalSongString + HTML_FOOT, self.songName+".pdf")
            return self.songName + ".pdf"
        elif self.params['fileformat'] == 'ppt' : 
            return self.songName + ".ppt"
    
    
def makePdfSong(songNumber, rest_of_params):
    """callable function for creating asked song export

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
        return songObject.export()
        
    except Exception as e:
        print(bcolors.WARNING + "An error occured: " + str(e) + bcolors.ENDC)
        return False

def extractOptionalParams(rest_of_params):
    """extract the rest of the params, possible params are: \n
    resx - for X component of resolution of the output screen \n
    resy - for Y component of resolution of the output screen \n
    fileformat - either pdf or ppt \n
    songformat - consisting of numbers, B (bridge), R, C (chorus) - how the text should go \n

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
        "songformat" : songFormat
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

