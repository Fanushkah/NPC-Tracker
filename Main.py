import os, json, shutil

mainLoop = None
npcFolder = "./NPCs"
templateNPC = "./NPCs/template.json"
tempNPC = "./NPCs/tempNPC.json"

def npcSorter():
    for npc in os.listdir(npcFolder):
        print(npc)
    print("")

def createNPC():
    shutil.copy(templateNPC, tempNPC)
    print("Let's build an NPC! Keep in mind that you can skip any of these (besides the name) by just hitting enter without typing anything, you can always change them afterward.")
    npcName = input("What is their name?").lower()
    if f"{npcName}.json" not in npcFolder:
        os.rename(tempNPC, f"{npcName}")
    print("Make an NPC\n")

while mainLoop != "4":
    mainLoop = input("""What would you like to do? ()
1) Sort
2) Create
3) Edit
4) Exit
""")
    os.system('clear')
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