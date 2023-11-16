import os, json, shutil
from colorama import Fore, Back

#TODO: Maybe retool the edit function to take an argument for an NPC name so that the user can go to the edit menus directly from the viewing menu
#TODO: Let the user copy NPC data to the clipboard using pyperclip so they can use it elsewhere.
#TODO: Fix the formatting for making a character
#TODO: Pressing the number should take you to options on the view menu

#Initialize some info for later.
mainLoop = None
templateNPC = "template.json"
tempNPC = "tempNPC.json"
defaultTemplate = {
    "name": "",
    "tags": "",
    "age" : "",
    "species": "",
    "town": "",
    "country":"",
    "description": "",
    "voice":"",
    "quirks": "",
    "wants": "",
    "relationships": "",
    "beliefs": "",
    "NTS": ""
}

#If you come across anything you'd use that isn't part of this list, please send it to me to be added.
affirmative = ["affirmative","yes","yea","ye","yup","y","ya","indeed","surely","uh-huh","sure","agreed","i guess","why not","yessir", "amen", "fine", "okay", "all right", "aye", "certainly", "definitely", "gladly", "indubitably"]
negatory = ["no", "nope", "nah", "n","never","nuh-uh","nay","negatory","no way"]

#Used to clear the terminal/command line without worrying about what OS I'm on.
def clear():
    if os.name=="nt":
        os.system("cls")
    else:
        os.system('clear')


#First time initialization if it can't find the NPCs folder. This is to make updating the script easier.
#Find if the NPCs folder exists. If not, ask if they already have one. If not, create one.
if "NPCs" not in os.listdir("./"):
    clear()
    options = input(Fore.MAGENTA+"The \"NPCs\" folder can not be found."+Fore.WHITE+"\n1)I already have an NPCs folder from a different version.\n2)This is a fresh install.\n>").strip()
    clear()
    if options == "1":
        input("Please move your NPCs folder into the same folder as Main.py. Make sure it is named \"NPCs\" exactly. Then start the program again.")
        exit()
    elif options == "2":
        os.mkdir("NPCs")
        with open("./NPCs/"+templateNPC,"w") as outfile:
            outfile.write(json.dumps(defaultTemplate, indent=4))


    


#Change the working directory so I don't have to deal with specifying that every single file I change in this is in /NPCs
#The program is running in the main folder, but this makes it so every action from here on out is editing files in /NPCs by default
os.chdir("./NPCs/")

#These next three are some special tools that we'll use later ;^)
#Gives the option of pulling the data from an NPC, returning None, or returning a /menu call.
def dataPuller(name):
    name = name.lower()
    if name != "/menu":
        if name[-5:] != ".json":
            npcFile = f"{name.strip().replace(' ','_')}.json"
        else:
            npcFile = name
        if npcFile in os.listdir("./"):
            with open(npcFile, 'r') as file:
                npcFile = json.load(file)
            data = npcFile
            return(data)
        else:
            data = None
            return(data)
    else:
        return(name)

def dataPusher(npcFilePath, data):
    if npcFilePath in os.listdir("./"):
        with open(npcFilePath, 'w') as file:
            json.dump(data, file, indent=4)

def npcDeleter(name):
    clear()
    npcFile = f"{name}.json"
    if npcFile in os.listdir("./") and npcFile != "template.json":
        data = dataPuller(name)
        for x in data:
            print(Fore.MAGENTA + f"{x.title()}: {data[x]}")
        confirmation = input(Fore.WHITE + f"Are you sure you want to delete {name.title()}? There's no way to reverse this.\n>").lower()
        if confirmation in affirmative:
            os.remove(npcFile)
            clear()
            input(Fore.RED + f"{name.title()} has been permanently removed from existence.")
        elif npcFile == "template.json":
            input("No. You really don't want to do that.")
        else:
            clear()
            input(Fore.RED +f"{name.title()} has been spared.")
    else:
        input(f"{name.title()} could not be found in your NPCs.")



#function to go through every single option in a json file and save the responses so if I have to do it more than once I can just call it.
def createNPC(name, file):
    clear()

    with open(file,'r') as npc:
        npcFile = json.load(npc)
    print(f"Time to make {name}! Keep in mind that you can skip any of these by just hitting enter without typing anything, you can always change them afterward.")

    #Iterate through each descriptor, ignoring the name.
    done = {"name": name}
    for descriptor in npcFile:
        #We already have a name, please don't edit it.
        if descriptor == "name":
            continue

        #descriptions of each descriptor
        descriptions = {
            "tags":"These are used to group NPCs together outside of common descriptors like location. Then later you can search for all NPCs with the tag to quickly find these groups.",
            "age":f"How old is {name}?",
            "species":"What are they? Who are their people?",
            "town":"What town do they frequent or were they found in by the party?",
            "country":"Wider scope that can be useful for you to sort NPCs by later.",
            "description":"What do they look like physically?",
            "voice":"How do they convey themselves (Also how do you convey them to the players)",
            "quirks":"What are the small things that make them instantly memorable?",
            "wants":"What do they want out of life and what are they doing to get it?",
            "relationships":"Who do they know, who knows them?",
            "beliefs":"What gods do they follow? What are they passionate about?",
            "NTS":"Important information outside of everything else that will help you remember them."
        }
        
        #print what has already been added.
        if done != {"name":name}:
            for x in done:
                print(f'{x.title()}: {done[x]}')

        #Get user input for what the description is.
        userDescription = input(f"{descriptor.title()}: {descriptions[descriptor]}\n{descriptor.capitalize()}: ")
        npcFile[descriptor] = userDescription

        #Update Done so its ready on the next pass.
        done[descriptor]= userDescription
        clear()
    
    clear()
    #print Done again.
    for x in done:
        print (f"{x.title()}: {done[x]}")

    #Push all of the updates to the file using the dataPusher function
    dataPusher(file,done)
    input(f"You've finished making {name}, they're beautiful. I pray for their souls that you don't have murderhobos.")

def npcList():
    for npc in os.listdir("./"):
        if npc != "template.json": 
            print(Fore.MAGENTA + npc[:-5].replace("_"," ").title())

#Initialize the file based off of template.json, get the name of the NPC
def initialize():
    #Copy the template to a new file so I can overwrite it.
    shutil.copy(templateNPC, tempNPC)
    
    while True:
        #Get the NPC's name and sanitize it to make the new file name.
        npcName = input("Let's build an NPC! What is their name?\n")
        fnpcName = npcName.lower().strip().replace(" ","_")
        npcFile = f"{fnpcName}.json"
    
        #If there isn't already a file with that name, make it.
        if npcFile not in os.listdir("./"):
            os.rename(tempNPC, npcFile)
            break

        #If there is already a file with that name, give them the option to rename it or add a signifier onto it.
        elif npcFile in os.listdir("./"):
            clear()
            nameError = input(f"{npcName} is already in use.\nDo you want to:\n1)Rename the NPC.\n2)Add a moniker to the end and keep this name. ")
            #If they wanna rename just restart the while loop
            if nameError == "1":
                clear()
                continue
            #If the user wants a moniker, give it to them and break out of the while loop to continue.
            elif nameError == "2":
                clear()
                moniker = input("What would you like the moniker added to be? It will be named as name(moniker).json\n")
                npcFile = f"{fnpcName}({moniker}).json"
                os.rename(tempNPC, npcFile)
                break

    ##Initialize the rest of the data. Make this abstract as fuck so that it takes up less space. If you hard code this you can go fuck yourself.
    createNPC(npcName, npcFile)

def viewNPC(name):
    while True:
        clear()
        data = dataPuller(name)
        if data != None and data != "/menu":
            for x in data:
                print(Fore.MAGENTA + f"{x.title()}: {data[x]}")
            choice = input(Fore.WHITE +"Edit or Press any button to continue.\n>").lower().strip()
            if choice == "edit":
                editNPC(name)
                break
            else:
                break
        elif name == "/menu":
            break
        else:
            input(f'Could not find {name.title()} in the NPC list, try again.')
            break

def editNPC(name):    
    npcFile = f"{name}.json"
    descriptor = dataPuller(npcFile)

    #Initialize the outFile so it can be used in the loop
    outFile = descriptor
    while True:
        clear()
        #print the NPC file.
        for x in descriptor:
            print(Fore.MAGENTA + f"{x.title()}: {descriptor[x]}")
                
        #get user input
        edit = input(Fore.WHITE + f'What part of {name.replace("_"," ").title()} would you like to edit?\n>').lower().strip()

        #nts is in all caps on the file so I have to do this for it to match with the sanitizing I did. I hate this.
        if edit == "nts":
            edit = "NTS"

        #if the input is actually there, let them edit the file.
        while edit in descriptor:
            clear()
            for x in descriptor:
                print(Fore.MAGENTA + f"{x.title()}: {descriptor[x]}")

            #Get the input for what they want the new description to be.
            description = input(Fore.WHITE + f'New description for {edit}: ')
            #Temporary edit of the outFile with their change.
            outFile[edit] = description
            clear()
            #Print the NPC again with new changes
            for x in descriptor:
                print(Fore.MAGENTA + f"{x.title()}: {descriptor[x]}")
            #Make sure they're done before closing so that user doesn't have to come all the way back around to edit again.
            edit = input(Fore.WHITE+'Select another descriptor or use /exit to save.\n> ').lower().strip()
                   
            #TODO:Find a way to fix this ungodly mess. This shouldn't be necessary
            if edit =="nts":
                edit = "NTS"

            if edit == "/exit":
                #Save the data.
                dataPusher(npcFile, outFile)
                break
            else:
                continue
        #If the input isn't there, make them retry.
        if edit == "/exit":
            break
        else:
            input(f'{edit.title()} is not one of the descriptors.')

def findLoop():
    while(True):
        clear()
        npcList()
        print(Fore.WHITE + "To use these commands, type the selection followed by the name of the NPC you want. E.g. 1 Bobert Hobbert")
        choice = input("1)View an NPC 2)Sort for tags 3)Edit an NPC 4)Delete an NPC\n>").capitalize().strip().replace(" ","_")
        #Get rid of any spaces between text
        if choice[1:2] == "_":
            choice = choice[:1] + choice[2:] 
        #Do the menu thing.
        if choice[:1] == "1":
            #Takes the choice and sends it to the viewNPC function. 
            #TODO: Verify using Regex that the choice is an applicable name so that there are less options needed inside of viewNPC
            viewNPC(choice[1:])
            continue
        elif choice[:1] == "2":
            input("Sort ")
        elif choice[:1] == "3":
            editNPC(choice[1:])
        elif choice[:1] == "4":
            npcDeleter(choice[1:])
        elif choice == "/exit":
            break
        else:
            input(f'"{choice.lower().replace("_"," ")}" is not a recognized command or name. Please try again. ')



#Main loop that runs the program, once this ends the entire program ends.
while(True):
    clear()
    #Main Menu text
    mainLoop = input("""What would you like to do?
1) Create
2) Find
3) Exit
>""")
    clear()
    if mainLoop == "1":
        #Basic idea finished
        initialize()
    elif mainLoop == "2":
        #Enter the find loop
        findLoop()
    elif mainLoop == "3":
        #Break out of the main loop and end the program
        break
