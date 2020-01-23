#!/usr/bin/python3
import pytube
from pytube import Playlist
import os
import subprocess
import pymongo
import uuid

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dwndata = myclient["downloaded"]
mp3 = dwndata["bollyfavmp3"]
link_dict = {}

def getAllLinks(playlist):
    '''
    : This function take a link of playlist and return the link of each videos
    :param playList:
    :return: A list of all Url links
    '''
    allLinks = []
    youtubeLink = 'https://www.youtube.com'
    pl = Playlist(playlist)
    for linkprefix in pl.parse_links():
        allLinks.append(youtubeLink + linkprefix)
    return allLinks

def downloadPlaylist(playlistLink):
    linkArray = getAllLinks(playlistLink)
    for link in linkArray:
        link_dict = {
            'url': link,
            '_id': uuid.uuid4()
            } #'id'
        downloaded_links = mp3.find()
        #print(link_dict)
        #print(downloaded_links.count())
        if downloaded_links.count() == 0:
            mp3.insert_one(link_dict)
            #print(link_dict)
        else:
            if not (mp3.find_one({"url": link})):
                downloadVideo(link)
                #print(downloaded_links.count())
                mp3.insert_one(link_dict)
                #print("Internal Looop:")
                #print(link_dict)


def downloadVideo(link):
    stream = pytube.YouTube(link)
    song = stream.streams.filter(only_audio=True).first()
    if song !=None:
        song.download('/home/navdeep/media')
        #print(stream.streams.filter(only_audio=True).first())
    else:
        print(stream.title)
        #print(stream.streams.first())
def convert_To_mp3():
    path = '/home/navdeep/media'
    listing = os.listdir(path)
    for file in listing:
        base = file.split('.')
        newname = base[0]+'.mp3'
        subprocess.call(['ffmpeg','-i', os.path.join(path, file), os.path.join(path, newname), '-n'])

#playlist = 'https://www.youtube.com/playlist?list=PLesn1W5rqWw1c6X8KofFjhrk-6DEfTTYz'
playlist = 'https://www.youtube.com/playlist?list=PLesn1W5rqWw3Lerhh5Y93AO8aA3fgGNPZ'

#downloadPlaylist(playlist)
convert_To_mp3()
