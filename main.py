# Searching files in the computer's logical storage devices:

#importing subprocess to run command line for scanning the available logical devices
import subprocess
from sys import stdout 
# importing the os module for searching
import os

# creating a file and storing all the info and script there
path=__file__
path=path.replace('main.py','')
os.chdir(path)
storage='file_search'
change_path=path+storage+'\main.py'
if 'file_search' not in __file__:
    try:
        os.mkdir(path+storage)
    except:
        pass
    try:
        os.replace(__file__,change_path)
    except:
        pass
try:
    os.chdir(path+storage)
except:
    pass
print(os.getcwd())

run=True
locations=""
flag_c=os.getcwd()+'\\flag_counter.txt'  # counter for number of files found
file_location=os.getcwd()+'\\file_loc.txt' # txt file for storing locations of files found

# Function: searching the required file
def file_search(file_name,l):
    try:
        # function of the module that returns a list of other files inside the directory
        list_dir=os.listdir(l)  
    except:
        # some folders need root permission to avoid error we use the except block
        print("Access denied by",l)
        return
    c=0
    for i in list_dir:
        loc=l+'\\'+i  # taking the location of the file

        # checks wether the location is a file or folder location
        # if file: checks if it macthes the file requested and then exiting
        # if folder: entering into another recursive function to check for the files and folder
        if os.path.isfile(loc) :
            c+=1
            if file_name in i.lower():

                # file found then 1 added to counter flag 
                with open('flag_counter.txt','a') as f:  
                    f.write('1')

                # location of the file saved in the .txt file
                with open(file_location,'a') as f: 
                    print(loc,file=f)  

        # else is the location is a folder not a file    
        else:
            file_search(file_name,loc)

        # if all the files are checked then exit the recursive fuction to the previous one
        if c== len(list_dir):  
                return

    # ends the particular recursive function 
    # if all the files and folder are checked in the list of the directory
    return

# narrowing down the search with location entered by user
def locationOfSearch(dir):
    
    # we give an option to the user to select a subfolder to run the sacn into
    list=os.listdir(dir)
    print("\nPlease select the folder of drive D:\\ you want to search in: ")
    for index,i in enumerate(list):
        print(f'\t{index+1}. {i}')
    print("\t99. Full scan")

    # by selecting the number the location of the folder to search in is taken and returned
    # if user selects 99 == runs a full scan 
    #location would be the Drive location only
    option=int(input("\nEnter your choice: "))
    if option==99:
        return dir
    # if!= 99 then finds the selected folder and returns the location
    else:
        option-=1
        for index,i in enumerate(list):
            if option == index:
                dir= dir+i
                return dir


# runs the program until run is not false
while run == True:

    # initialising both of the files to none
    with open(flag_c,'w') as f:
        f.write('')
    with open(file_location,'w') as f:
        f.write('')

    print()
    name=input("Enter the file name or type you want to search: ")

    # Scanning the available drives and asking the user to select one
    result=subprocess.run(['wmic','logicaldisk','get','deviceid'], capture_output=True).stdout.decode()
    result=result.split()
    result=result[1:]
    print("\nSelect the Drive you want to search in: ")
    for index,i in enumerate(result):
        print(f"\t{index+1}. {i}")
    drive=input("Please select your option: ")
    for index,i in enumerate(result):
        if drive==str(index+1) or drive in i.lower():
            l=i+'\\'
 
    # based on the drive now it is send to function to narrow down the search
    # user selects the sub folder of the drive in which the scan will run on
    search_loc=locationOfSearch(l)
    print("Location you selected is:", search_loc)
    print("\nSearching...")
    print("May take a while -- please wait\n")

    # After the location is finallised the earching begins...
    file_search(name,search_loc)

    # reading the txt files to get the files found anf locations respectively
    with open (flag_c) as f:
        flag=f.read()
    with open (file_location) as f:
        locations=f.read()

    # if the counter flag is not none == a file is found
    # displaying all the relevant details we found
    if flag != '':
        print("\nThe file you requested for is found\n")
        print("Locations are saved in", file_location )
        print("Locations are as follows:")
        print('-------------------------')
        print(locations)
        print("Total number of files found: ",len(flag))

    # if the counter flag is none then no file is found
    else:
        print('\nYour file is not found in the location')

    # given choice to user if he wants to exit
    # if yes run == false
    print('\nDo you want to search again (y) for yes and (n) for no: ')
    x=input("")
    if x=='n':
        run= False  # the program will end
        print('\nTHANK YOU SIR')
        