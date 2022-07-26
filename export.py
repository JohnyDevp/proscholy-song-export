#for making a graphql request and further result get
from token import EXACT_TOKEN_TYPES
from warnings import catch_warnings
from attr import define
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

#for converting given graphql result into text
import json

#for converting json into pdf
import jpype
import asposecells
jpype.startJVM() 
from asposecells.api import Workbook
import pdfkit
import requests

#for running a server
from flask import Flask
from flask import send_file

#path for sending  graphql requests
PROSCHOLY_PATH = "https://zpevnik.proscholy.cz/graphql"


if __name__ == "__main__":
    print("ProScholy.cz song pdf converter")

    #get song number which will be converted
    songNumber = input("Please provide a song number: ")

    transport = AIOHTTPTransport(url=PROSCHOLY_PATH)
    
    #create client from 
    client = Client(transport=transport, fetch_schema_from_transport=True)

    #create query
    query = gql(
        """
            query getSongLyrics ($id: ID!) {
                song_lyric(id: $id){
                    id
                    lyrics_no_chords_no_comments
                }
            } 
        """
    )

    params = {"id" : songNumber}
    
    
    result = client.execute(query, variable_values=params)
    print(result['song_lyric']['lyrics_no_chords_no_comments'])

    html_content_first = """
        <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body> """       

    html_content_end = """
        </body>
        </html>
    """
    pdfkit.from_string(html_content_first + result['song_lyric']['lyrics_no_chords_no_comments'] + html_content_end, "output.pdf")
    # file = open('neco.txt', "x")
    # file.write(result['song_lyric']['lyrics_no_chords_no_comments'])
    # pdfkit.from_string(result['song_lyric']['lyrics_no_chords_no_comments'], 'output.pdf')
    #pdfkit.from_file('neco.txt', 'output.pdf')

    