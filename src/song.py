import re
import json

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
        
        #create json model
        song_data = { 
            "data" : {
                "song-name" : self.songName,
                "song-number" : self.params['songnumber'],
                "num-of-slides" : 40,
                "export-format" : self.params['fileformat']
            },
            "slides" : []
        }
        # handle the song format - how the verses should go
        self.__putSongInOrder()

        # write json file
        with open(self.songName + ".json", "w") as file:
            file.write(json.dumps(song_data))

        # return json file name
        return self.songName + ".json"
