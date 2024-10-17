import requests
import json
import tkinter as tk
import random
from PIL import Image, ImageTk
from io import BytesIO

appIDList = []
storyGamesScore = []
nonStoryGamesScore = []
currentGameIndex = 0

#Gets the Steam API Key
#Put steam API key in steamAPIKey.txt and nothing else
apiFile = open("steamAPIKey.txt", "r")
apiKey = apiFile.readline()

def getGames(steamID):
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=" + apiKey + "&steamid=" + steamID + "&include_appinfo=1&include_played_free_games=1&format=json"
    response = requests.get(url)

    #Check to make sure we got a valid response
    if response.status_code == 200:
        print("Got a valid response")
        data = response.json()
        #with open("response.json", 'w') as outputFile:
        #    outputFile.write(json.dumps(data))

        for game in data ["response"]["games"]:
            playtime = int(game["playtime_forever"])
            appID = game["appid"]
            name = game["name"]
            appIDName = (appID, name)
            if (appIDName not in appIDList) and (playtime != 0): #Don't add duplicates or no play time games
                appIDList.append((appID, name))
            else:
                if (playtime == 0):
                    print(name+ " has zero playtime. Not adding it")
                else:
                    print(name + " is a duplicate. Not adding it")

    else:
        print("Did not get a valid response from the Steam API. Did you enter the right steamID and API Key?")

def submit_score():
    global currentGameIndex
    name = appIDList[currentGameIndex][1]
    #Get scores
    storyScore = story_entry.get()
    gameplayScore = gameplay_entry.get()
    artScore = art_entry.get()
    musicScore = music_entry.get()


    if(storyScore == "SAVE"):
        outputScores()
        root.destroy()
        outputScores()
        return

    if(gameplayScore == "" and artScore == "" and musicScore == "" and storyScore == ""):
        print("Skipping " + name)
    else:
        if gameplayScore == "":
            gameplayScore = 0
        if artScore == "":
            artScore = 0
        if musicScore == "":
            musicScore = 0

        #Save game name and scores
        if (storyScore == ""):
            print("Saving " + name + " as a non-story game (" + gameplayScore + "," + artScore + "," + musicScore + ")")
            avgScore = (float(gameplayScore) + float(artScore) + float(musicScore))/3
            nonStoryGamesScore.append((name, avgScore, gameplayScore, artScore, musicScore))
        else:
            print("Saving " + name + "as a story game (" + storyScore + "," + gameplayScore + "," + artScore + "," + musicScore + ")")
            avgScore = (float(gameplayScore) + float(artScore) + float(musicScore) + float(storyScore))/4
            storyGamesScore.append((name, avgScore, storyScore, gameplayScore, artScore, musicScore))

    #Clear
    story_entry.delete(0, tk.END)
    gameplay_entry.delete(0, tk.END)
    art_entry.delete(0, tk.END)
    music_entry.delete(0, tk.END)

    currentGameIndex = currentGameIndex + 1

    if currentGameIndex < len(appIDList):
        label.config(text=appIDList[currentGameIndex][1])
        update_image(appIDList[currentGameIndex][0])
    else: #We are finished
        root.destroy()
        outputScores()

def outputScores():
    storyGamesScore.sort(reverse=True, key = lambda x: x[1])
    nonStoryGamesScore.sort(reverse=True, key = lambda x: x[1])
    with open("Story.csv", 'w') as storyFile:
        for game in storyGamesScore:
            storyFile.write(game[0] + "," + str(game[1]) + "," + str(game[2]) + "," + str(game[3]) + "," + str(game[4]) + "," + str(game[5]) + "\n")
    with open("Non-Story.csv", 'w') as nonStoryFile:
        for game in nonStoryGamesScore:
            nonStoryFile.write(game[0]+ "," + str(game[1]) + "," + str(game[2]) + "," + str(game[3]) + "," + str(game[4]) + "\n")

def update_image(appID):
    response = requests.get("https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/" + str(appID) + "/header.jpg")
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    # Resize image to fit in the tkinter window
    img = img.resize((469, 215))
    img_tk = ImageTk.PhotoImage(img)

    # Update the image label with the new image
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection

#Loop contorl variable for user input
keepInputting = True
#Get games
while keepInputting:
    steamIDInput = input("Please enter a steam ID. Enter 'DONE' when finished. ")
    if(steamIDInput != "DONE"):
        getGames(steamIDInput)
    else:
        keepInputting = False

#Shuffle the list of games
random.shuffle(appIDList)

#Display games on window along with input
root = tk.Tk()
root.geometry("900x900")

label = tk.Label(root, text=appIDList[currentGameIndex][1], font=("Helvetica", 16))
label.pack(pady=20)

# Image label
image_label = tk.Label(root)
image_label.pack(pady=10)
update_image(appIDList[0][0])

story_label = tk.Label(root, text="Story", font=("Helvetica", 16))
story_label.pack(pady=20)
story_entry = tk.Entry(root, width=10)
story_entry.pack(pady=10)

gameplay_label = tk.Label(root, text="Gameplay", font=("Helvetica", 16))
gameplay_label.pack(pady=20)
gameplay_entry = tk.Entry(root, width=10)
gameplay_entry.pack(pady=10)

music_label = tk.Label(root, text="Music", font=("Helvetica", 16))
music_label.pack(pady=20)
music_entry = tk.Entry(root, width=10)
music_entry.pack(pady=10)

art_label = tk.Label(root, text="Graphics/Art", font=("Helvetica", 16))
art_label.pack(pady=20)
art_entry = tk.Entry(root, width=10)
art_entry.pack(pady=10)

submit_button = tk.Button(root, text="Submit Score", command=submit_score)
submit_button.pack(pady=20)

root.mainloop()