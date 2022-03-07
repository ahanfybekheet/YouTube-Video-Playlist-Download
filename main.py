#-------------------------------------------------------------------
# YouTube (Video/Playlist) Download.
# Author        : Ahmed Hanfy Bekheet && 
# Version       : 1.0
# Python Version: 3.9.10
# Date          : 3/7/2022
#-------------------------------------------------------------------
# The User InterFace:
#   +------------+--------------------------------+
#   |     1      |             Video              |
#   |     2      |            Playlist            |
#   +------------+--------------------------------+
#
#-------------------------------------------------------------------
# Pesuado Code:
#       - Create Good User Interface For User:
#           - Ask User If He Want To Download Video Or Playlist.
#           - If He Choose Video Ask Him About quality.
#           - If He Choose Playlist Should Have To Option:
#               - If He Want Choose Group Of Videos On Playlist.
#               - Or If He Want To Download all Video.
#               - After It Choose Quality.
#           - Show The Title Of Video Of Download And Show Download Progress.
#--------------------------------------------------------------------


from pytube import Playlist
from pytube import YouTube
from prettytable import PrettyTable
import os




def user_interface():

    print("if it your first time to use this app enter 0.0 .\n".title())
    table = PrettyTable(["Choose num","What Do You Want To Download ?"])
    table.add_row(["1","Video"])
    table.add_row(["2","Playlist"])
    table.add_row(["3","Audio"])
    table.add_row(["4","Playlist As Audio"])
    table.add_row(["5","Playlist Time"])
    print(table)

    while True:
        try:
            user_input = input()
            if user_input in ["1","2","3","4","5"]: ##valid input list
                break
            else:
                print("Please Choose Valid Number")
        except:
            print("Please Enter Int Num")
    if user_input == '1':
        download_video("video")         ## call download video function as video
    elif  user_input =="2":
        download_playlist("video")      ## call download playlist function as video
    elif user_input == '3':
        download_video("audio")         ## call download video function as audio
    elif user_input == "4":
        download_playlist("audio")      ## call download playlist function as audio
    elif user_input == "5":
        download_playlist("time")       ## call download playlist function as time
    else:
        guid()


def choose_path():
    global path

    # Show the directories and make user to choose one from it
    while True:
        print("To Select Folder enter 0.\nEnter -1 To Create New Folder.\nEnter -2 To Go Back\n ".title())
        sub_dirs = [[dir.name for dir in os.scandir() if dir.is_dir() ],[dir.path for dir in os.scandir() if dir.is_dir()]] ##first list to make dir list with name seconde one is to make list with pathes

        table = PrettyTable()
        table.add_column("Index",list(range(1,len(sub_dirs[0])+1))) ##list(range(1,len(sub_dirs[0])+1)) make range equal to len dirs in current path
        table.add_column("Folders",sub_dirs[0])
        table.add_row(["The Current Path Is: ",os.getcwd()])
        print(table)
        #Start Of Validating input of user to make sure that there is no error will raise
        try:
            while True:
                user_input = int(input("Please Choose Folder: "))
                if user_input >= -2 and user_input <= len(sub_dirs[0]):
                    break
                else:
                    print(f"Please Enter Int Between -2 to {len(sub_dirs[0])}.\n")
        except:
            print("Please Enter Int Number.\nAnd Try Agian!!..")
            return choose_path()
        #End Of Validating

        ### Create New Folder And Change Dir To That Folder When User Enter -1
        if user_input == -1:
            folder_name =input("Please Enter Folder Name: ")
            os.mkdir(folder_name) 
            os.chdir(f".\\{folder_name}")
        ### Go to The Parent Dir When User Enter -2
        elif user_input == -2:
            os.chdir("..")
        ### Select Current Path As Download Path 
        elif user_input == 0:
            break
        else:
            os.chdir(sub_dirs[1][user_input-1])



def choose_quality():
    global quality

    # Create Good Design Table To Choose Quality
    table = PrettyTable()
    vid_res = {1:"144p",2:"360p",3:"720p"}
    table.add_column("Choose num",list(vid_res.keys()))
    table.add_column("Video resolution",list(vid_res.values()))
    print(table)
    #The Start Of Validation Of User Input
    try:
        while True:
            user_input = int(input("Please Choose Your Suitable Quality: "))
            if user_input >= 1 and user_input <= 5:
                break
            else:
                print("Please Enter Int Between 1 to 5.\n")
        quality = vid_res[user_input]
    except:
        print("Please Enter Int Number.\n")
    #End Of Validation Of User Input

def guid():
    '''Show Guid For Application'''
    print("when you open this app you first choose if you want to download video or playlist so you must input 1 or 2 if you input none of them the app will ask you about input again and again and so on.\nthen the app ask you about url of (video/playlist) you must enter valid url,please enter valid becouse the app will ask you again and again if you put invalid url.\nafter you enter the url, will ask you about the path then the quality\nif you choose to download playlist you can choose collection of videos or enter select or choose then the download will start.".title())
    while True:
        user_input = input("Do You Want To Start Application (y/n): ")
        user_input =user_input.upper
        if user_input == 'Y' or user_input =='N':
            break
        else:
            print("Enter Valid Input")
    if user_input == 'Y':
        user_interface()
    else:
        quit()
    

def download_video(Type):
    url = input("please enter url of video: ".title())
    try:
        video = YouTube(url)
    except:
        print("Please, Enter Valid Youtube Video Url!!..\nAnd Try Again.")
        return download_video(Type)
    choose_path()
    print(video.title)
    if Type == 'video':
        choose_quality()
        video.streams.filter(res=quality,progressive=True).last().download()
    else:
        video.streams.filter(type="audio").last().download()

def download_playlist(Type):
    url = input("please Enter playlist url: ".title())
    try:
        playlist= Playlist(url)
        len(playlist.video_urls) ### To raise Error if url is not valid
    except:
        print("Please, Enter Valid Youtube Playlist Url!!..\nAnd Try Again.")
        return download_playlist(Type)
    if Type != "time":
        choose_path()
    if Type == 'video':
        choose_quality()
    videos_title = [YouTube(video).title for video in playlist]
    table = PrettyTable()
    table.add_column("Index",list(range(1,len(playlist)+1)))
    table.add_column("Videos",videos_title)
    table.add_row([len(playlist)+1,"Select All"])
    print(table)

    ##Start of validating user input
    while True:
        try:
            user_input = list(map(int,input(f"Please Enter Your Wanted Videos Seperated By Comma (e.g:3,5,6,7): ").split(',')))
            valid_input = [x for x in user_input if x >= 1 and x <= len(playlist)+1 ]
            if valid_input:
                if not(len(playlist)+1 in valid_input and len(valid_input)>1) :
                    break
                else:
                    print("Please Enter Valid Input")
            else:
                print("Please Follow Instructions!!..")
        except:
            print('Please Enter Int Number')
    ##end of validating
    time = 0     ### to add time of each video to it
    ## If user choose select all option
    if user_input == [len(playlist)+1]:
        for vid in playlist:
            video = YouTube(vid)
            print(video.title)
            if Type == 'video':
                video.streams.filter(res=quality,progressive=True).last().download()
            elif Type == 'audio':
                video.streams.filter(type="audio").last().download()
            else:
                time += video.length
    ## If user choose collection of videos
    else:
        for i in user_input:
            video = YouTube(playlist[i-1])
            print(video.title)
            if Type == 'video':
                video.streams.filter(res=quality,progressive=True).last().download()
            elif Type == 'audio':
                video.streams.filter(type="audio").last().download()
            else:
                time += video.length
    ## If user choose time To print Time of playlist
    if Type == 'time':
        print(f"The Video Duration Is {time/60} min")


if __name__ == '__main__':
    user_interface()