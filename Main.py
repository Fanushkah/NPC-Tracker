import os, json, shutil

mainLoop = None
templateNPC = "template.json"
tempNPC = "tempNPC.json"

os.chdir("./NPCs/")

def clear():
    if os.name=="nt":
        os.system("cls")
    else:
        os.system('clear')


def npcSorter():
    for npc in os.listdir("./"):
        print(npc)
    print("")

#Initialize the NPC file off of a template and get a first pass at filling the specifics in.
def createNPC():
    #Copy the template to a new file so I can overwrite it.
    shutil.copy(templateNPC, tempNPC)
    print("Let's build an NPC! Keep in mind that you can skip any of these (besides the name) by just hitting enter without typing anything, you can always change them afterward.")
    
    while True:
        clear()
        #Get the NPC's name and initialize files
        npcName = input("What is their name?\n").lower()
        npcNameFile = f"{npcName}.json"
    
        #If there isn't already a file with that name, make it.
        if npcNameFile not in os.listdir("./"):
            clear()
            os.rename(tempNPC, npcNameFile)
            print("File named!")
            break

        #If there is already a file with that name, give them the option to rename it or add a signifier onto it.
        elif npcNameFile in os.listdir("./"):
            clear()
            nameError = input(f"{npcName} is already in use.\nDo you want to:\n1)Rename the NPC.\n2)Add a moniker to the end and keep this name. ")
            #If they wanna rename just restart the while loop
            if nameError == "1":
                continue
            #If the user wants a moniker, give it to them and break out of the while loop to continue.
            elif nameError == "2":
                clear()
                moniker = input("What would you like the moniker added to be? It will be named as name(moniker).json\n")
                npcNameFile = f"{npcName}({moniker}).json"
                os.rename(tempNPC, npcNameFile)
                break

    #Now initialize the data, starting with putting the name into the file.
    with open(npcNameFile,'r') as file:
        data = json.load(file)
        for descriptor in data:
            print(descriptor)
    
    input("Continue?")

while mainLoop != "4":
    mainLoop = input("""What would you like to do? ()
1) Sort
2) Create
3) Edit
4) Exit
""")
    clear()
    if mainLoop == "1":
        npcSorter()
    elif mainLoop == "2":
        createNPC()
    elif mainLoop == "3":
        print("edit")
    elif mainLoop == "4":
        break
    else:
        print(f"I don't recognize {mainLoop} as an option. Try again.")