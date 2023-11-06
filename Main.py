import os, json, shutil

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

    #Push all of the updates to the file.
    with open(file, 'w') as file:
        json.dump(done, file, indent=4)

def npcSorter():
    for npc in os.listdir("./"):
        print(npc)
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
    with open(npcFile, 'w') as file:
        json.dump(descriptor, file, indent=4)
    #Initialize the rest of the data. Make this abstract as fuck so that it takes up less space. If you hard code this you can go fuck yourself.
    initialize(npcName, npcFile)
    input("Continue?")
    clear()

def viewNPC():
    while True:
        clear()
        name = input("What NPC are you wanting to view? Type \"/menu\" to return to the main menu.\n")
        npcFile = f"{name.lower().strip().replace(' ','_')}.json"
        if npcFile in os.listdir("./"):
            with open(npcFile,'r') as file:
                npcFile = json.load(file)
            for x in npcFile:
                print(f"{x.capitalize()}: {npcFile[x]}")
            input("Press any button to continue.")
            continue
        elif name == "/menu":
            break
        else:
            retry = input(f'Could not find {name}, try again? y/n').lower().strip()
            if retry == "y":
                continue
            else:
                break


while mainLoop != "5":
    clear()
    mainLoop = input("""What would you like to do?
1) Create
2) Sort
3) View
4) Edit
5) Exit
""")
    clear()
    if mainLoop == "1":
        createNPC()
    elif mainLoop == "2":
        npcSorter()
    elif mainLoop == "3":
        viewNPC()
    elif mainLoop == "4":
        print("Edit")
    elif mainLoop == "5":
        break
    else:
        print(f"I don't recognize {mainLoop} as an option. Try again.")