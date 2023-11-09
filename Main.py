import os, json, shutil, pyperclip as pc

#TODO: Replace the Y/N at the end of editing with a "Select another descriptor or use /exit to save."
#TODO: Let the user /exit at any point in the editing process. 
#TODO: Maybe retool the edit function to take an argument for an NPC name so that the user can go to the edit menus directly from the viewing menu
#TODO: Definitely make editing available from the viewing menu at the very least.
#TODO: Let the user copy NPC data to the clipboard using pyperclip so they can use it elsewhere.

#Initialize some info for later.
mainLoop = None
templateNPC = "template.json"
tempNPC = "tempNPC.json"

#Change the working directory so I don't have to deal with specifying that every single file I change in this is in /NPCs
os.chdir("./NPCs/")

#Used to clear the terminal/command line without worrying about what OS I'm on.
def clear():
    if os.name=="nt":
        os.system("cls")
    else:
        os.system('clear')

#Gives the option of pulling the data from an NPC, returning None, or returning a /menu call.
def dataPuller(name):
    if name != "/menu":
        npcFile = f"{name.lower().strip().replace(' ','_')}.json"
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

#function to go through every single option in a json file and save the responses so if I have to do it more than once I can just call it.
def initialize(name, file):
    print(f"{name}- {file}")

    with open(file,'r') as npc:
        npcFile = json.load(npc)
    print(f"Time to make {name}! Keep in mind that you can skip any of these by just hitting enter without typing anything, you can always change them afterward.")

    #Iterate through each descriptor, ignoring the name.
    done = {"name": name}
    for descriptor in npcFile:
        clear()

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
                print(f'{x.capitalize()}:{done[x]}')

        #Get user input for what the description is.
        userDescription = input(f"{descriptor.capitalize()}: {descriptions[descriptor]}\n")
        npcFile[descriptor] = userDescription

        #Update Done so its ready on the next pass.
        done[descriptor]= userDescription
    
    clear()
    #print Done again.
    for x in done:
        print (f"{x}:{done[x]}")

    #Push all of the updates to the file using the dataPusher function
    dataPusher(file,done)

def npcSorter():
    for npc in os.listdir("./"):
        print(npc)
    input("Continue?")

#Initialize the NPC file off of a template and get a first pass at filling the specifics in.
def createNPC():
    #Copy the template to a new file so I can overwrite it.
    shutil.copy(templateNPC, tempNPC)
    print("Let's build an NPC! ")
    
    while True:
        clear()
        #Get the NPC's name and initialize files
        npcName = input("What is their name?\n")
        fnpcName = npcName.lower().strip().replace(" ","_")
        npcFile = f"{fnpcName}.json"
    
        #If there isn't already a file with that name, make it.
        if npcFile not in os.listdir("./"):
            clear()
            os.rename(tempNPC, npcFile)
            print("File named!")
            break

        #If there is already a file with that name, give them the option to rename it or add a signifier onto it.
        elif npcFile in os.listdir("./"):
            clear()
            nameError = input(f"{npcName} is already in use.\nDo you want to:\n1)Rename the NPC.\n2)Add a moniker to the end and keep this name. ")
            #If they wanna rename just restart the while loop
            if nameError == "1":
                continue
            #If the user wants a moniker, give it to them and break out of the while loop to continue.
            elif nameError == "2":
                clear()
                moniker = input("What would you like the moniker added to be? It will be named as name(moniker).json\n")
                npcFile = f"{fnpcName}({moniker}).json"
                os.rename(tempNPC, npcFile)
                break

    #Now initialize the data, starting with putting the name into the file.
    with open(npcFile,'r') as file:
        descriptor = json.load(file)
    descriptor["name"] = npcName
    dataPusher(npcFile, descriptor)
    #Initialize the rest of the data. Make this abstract as fuck so that it takes up less space. If you hard code this you can go fuck yourself.
    initialize(npcName, npcFile)
    input("Continue?")
    clear()

def viewNPC():
    while True:
        clear()
        name = input("What NPC do you want to view? Type \"/menu\" to return to the main menu.\n")
        data = dataPuller(name)
        if data != None:
            for x in data:
                print(f"{x.capitalize()}: {data[x]}")
            input("Press any button to continue.")
            continue
        elif name == "/menu":
            break
        else:
            input(f'Could not find {name} in the NPC list, try again.')

def editNPC():
    while True:    
        clear()
        name = input("What NPC do you want to edit? Type \"/menu\" to return to the main menu.\n")
        npcFile = f"{name.lower().strip().replace(' ','_')}.json"
        if npcFile in os.listdir("./"):
            with open(npcFile, 'r') as file:
                descriptor = json.load(file)
            for x in descriptor:
                print(f"{x.capitalize()}: {descriptor[x]}")


            outFile = descriptor
            while True:
                clear()
                #print the NPC file.
                for x in descriptor:
                    print(f"{x.capitalize()}: {descriptor[x]}")
                
                #get user input
                edit = input(f'What part of {name} would you like to edit?\n').lower().strip()
                #nts is in all caps on the file so I have to do this for it to match with the sanitizing I did.
                if edit == "nts":
                    edit = "NTS"
                
                #if the input is actually there, let them edit the file.
                if edit in descriptor:
                    #Get the input for what they want the new description to be.
                    description = input(f'{edit.capitalize()}: {outFile[edit]}\n New description for {edit}: ')
                    #Temporary edit of the outFile with their change.
                    outFile[edit] = description
                    #Make sure they're done before closing so that user doesn't have to come all the way back around to edit again.
                    stillEditing = input('Would you like to edit another description? Y to continue, any other button to save and close.').lower().strip()
                    if stillEditing == "y":
                        continue
                    else:
                        #Save the data.
                        dataPusher(npcFile, outFile)
                        break
                #If the input isn't there, make them retry.
                else:
                    input(f'{edit.capitalize()} is not one of the descriptors.')

        elif name == "/menu":
            break
        else:
            input(f'Could not find {name} in the NPC list, try again.')

#Main loop that runs the program, once this ends the entire program ends.
while mainLoop != "5":
    clear()
    #Main Menu text
    mainLoop = input("""What would you like to do?
1) Create
2) Sort
3) View
4) Edit
5) Exit
""")
    clear()
    if mainLoop == "1":
        #Basic idea finished
        createNPC()
    elif mainLoop == "2":
        #Can technically show you the current json files lmao.
        npcSorter()
    elif mainLoop == "3":
        #Basically finished
        viewNPC()
    elif mainLoop == "4":
        #Pretty much works!
        editNPC()
    elif mainLoop == "5":
        break
    else:
        print(f"I don't recognize {mainLoop} as an option. Try again.")