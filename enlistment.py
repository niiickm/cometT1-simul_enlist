class Classes:

    def __init__(self, classCode = "", classCourse = "", classUnits = 3, className = "", coursePreReqs = list(), classProf = "", classSection = "", classDay = "", classStart = "", classEnd = "", classRoom = "", classCap = 40, classNStudents = 0):
        self.classCourse = classCourse
        self.classCode = classCode
        self.classUnits = classUnits
        self.className = className
        self.coursePreReqs = coursePreReqs
        self.classDay = classDay
        self.classStart = classStart
        self.classEnd = classEnd
        self.classProf = classProf
        self.classSection = classSection
        self.classRoom = classRoom
        self.classCap = classCap
        self.classNStudents = classNStudents
    
    def addStudent(self):
        if self.classNStudents < self.classCap:
            self.classNStudents += 1
            return True
        else:
            return False

class Users:

    def __init__(self,username = "username", password = "password", nickname = "nickname"):
        self.username = username
        self.password = password
        self.nickname = nickname

class Student(Users):

    def __init__(self, username, password, nickname):
        super().__init__(username,password, nickname)
        self.curClasses = list()
        self.coursesTaken = list()

    def addClass(self, classCode):
        self.curClasses.append(classCode)
    
    def addCourseTaken(self, courseCode):
        self.coursesTaken.append(courseCode)

    def removeClass(self, classCode):
        if classCode in self.curClasses:
            self.curClasses.remove(classCode)

    def removeCourseTaken(self, courseCode):
        if courseCode in self.coursesTaken:
            self.coursesTaken.remove(courseCode)

class Admin(Users):

    def __init__(self, username, password, nickname):
        super().__init__(username,password,nickname)

#for checking if all elements in l2 are present in l1
def subList(l1,l2):
    return all(item in l1 for item in l2)

#loading the classes
def loadClasses():
    global classList
    try:
        classesFile = open("classes.txt","rt")
        for x in classesFile:
            tempS = x.split()
            tempPreqs = next(classesFile)
            if not tempPreqs.strip():
                tempPreqs = list()
            else:
                tempPreqs = tempPreqs.split()
            classList.append(Classes(tempS[0],tempS[1],int(tempS[2]),tempS[3],tempPreqs,tempS[4],tempS[5],tempS[6],tempS[7],tempS[8],tempS[9],int(tempS[10]),int(tempS[11])))
        classesFile.close()
        print("Loaded classes successfully!")
    except Exception as e:
        print(e)
        print("Cannot load classes file! Exiting program.")
        raise SystemExit

#loading the student accounts
def loadStudents():
    global studentList
    try:
        accountFile = open("students.txt","rt")
        for x in accountFile:
            tempS = x.split()
            tempC = next(accountFile)
            tempCT = next(accountFile)
            if not tempC.strip():
                tempC = list()
            else:
                tempC = tempC.split()
            if not tempCT.strip():
                tempCT = list()
            else:
                tempCT = tempCT.split()
            newUser = Student(tempS[0],tempS[1],tempS[2])
            newUser.curClasses = tempC
            newUser.coursesTaken = tempCT
            studentList.append(newUser)
        accountFile.close()
        print("Loaded student accounts successfully!")
    except Exception as e:
        print(e)
        print("Cannot load student accounts file! Exiting program.")
        raise SystemExit

#loading the admin accounts
def loadAdmins():
    global adminList
    try:
        accountFile = open("admins.txt","rt")
        for x in accountFile:
            tempS = x.split()
            newUser = Admin(tempS[0],tempS[1],tempS[2])
            adminList.append(newUser)
        accountFile.close()
        print("Loaded admin accounts successfully!")
    except Exception as e:
        print(e)
        print("Cannot load admin accounts file! Exiting program.")
        raise SystemExit

#saving the student accounts
def saveStudents():
    global studentList
    try:
        accountFile = open("students.txt", "wt")
        for x in studentList:
            accountFile.write("%s %s %s\n" % (x.username, x.password, x.nickname))
            tempStr = ' '.join(x.curClasses)
            accountFile.write("%s\n" % (tempStr,))
            tempStr = ' '.join(x.coursesTaken)
            accountFile.write("%s\n" % (tempStr,))
        accountFile.close()
        print("Saved student accounts successfully!")
    except Exception as e:
        print(e)
        print("Cannot save accounts file! Exiting program without saving.")
        raise SystemExit

#saving the admin accounts
def saveClasses():
    global classList
    try:
        classFile = open("classes.txt", "wt")
        for x in classList:
            classFile.write("%s %s %s %s %s %s %s %s %s %s %s %s\n" % (x.classCode, x.classCourse, x.classUnits, x.className, x.classProf, x.classSection, x.classDay, x.classStart, x.classEnd, x.classRoom, x.classCap, x.classNStudents))
            tempStr = ' '.join(x.coursePreReqs)
            classFile.write("%s\n" % (tempStr,))
        classFile.close()
        print("Saved classes successfully!")
    except Exception as e:
        print(e)
        print("Cannot save classes file! Exiting program without saving.")
        raise SystemExit

#enlistment menu for adding classes for student accounts
def enlistClasses():
    exitCond = True
    global classList
    global currentAccount

    while exitCond:
        innerCond = True
        choice = input("----------\n1. Search for Classes\n2. Add a class to your account\n3. Exit\nInput: ")
        while innerCond:
            if(not choice.isdigit()):
                choice = input("Invalid input. Please try again: ")
            elif int(choice) < 1 or int(choice) > 3:
                choice = input("Invalid input. Please try again: ")
            else:
                choice = int(choice)
                innerCond = False
        
        if choice == 1:
            inputCCode = input("Search for available classes using Course Code.\nInput course code: ")
            if any(y.classCourse == inputCCode for y in classList):
                print("Class offerings for %s: " % (inputCCode,))
                tempClassList = [z for z in classList if z.classCourse == inputCCode]
                for z in tempClassList:
                    print("Class Code: %s - %s" % (z.classCode, z.classCourse))
                    print("\tProfessor: %s, Days: %s" % (z.classProf, z.classDay))
                    print("\t%s - %s" % (z.classStart, z.classEnd))
                    print("\tAvailable Slots: %s" % (str(int(z.classCap) - int(z.classNStudents)),))

            else:
                print("There are no class offerings for %s at the moment." % (inputCCode,))
        
        elif choice == 2:
            inputCCode = input("Enroll in a class using Class Code.\nInput class code: ")
            if not any(x == inputCCode for x in currentAccount.curClasses):
                if not any(y.classCourse == inputCCode for y in classList):
                    currClass = next((z for z in classList if z.classCode == inputCCode), None)
                    currClassList = [z for z in classList if z.classCode in currentAccount.curClasses]
                    if(int(currClass.classNStudents) >= int(currClass.classCap)):
                        print("That class is already full!")
                    elif not subList(currentAccount.coursesTaken,currClass.coursePreReqs):
                        print("You do not meet the prerequisites required for this class!")
                    elif any(currClass.classStart >= z.classStart and currClass.classStart <= z.classEnd and currClass.classDay in z.classDay for z in currClassList):
                        print("There will be conflicts in schedule if you add this class.")
                    else:
                        currentAccount.addClass(inputCCode)
                        currentAccount.addCourseTaken(currClass.classCourse)
                        currClass.classNStudents = str(int(currClass.classNStudents) + 1)
                        print("Successfully added class!")
                else:
                    print("No class with such class code exists!")

            else:
                print("You are already enrolled in that class!")

        elif choice == 3:
            exitCond = False

#viewing enlisted classes for student accounts
def viewEnlistedClasses():
    global classList
    global currentAccount
    if(len(currentAccount.curClasses) > 0):
        print("Here are the current classes %s is enrolled in:" % (currentAccount.nickname,))
        currentClasses = [ x for x in classList if x.classCode in currentAccount.curClasses]
        for x in currentClasses:
            print("%s - %s - %s" % (x.classCode, x.classCourse, x.className))
            print("\tProfessor: %s, Room: %s, Days: %s" % (x.classProf, x.classRoom, x.classDay))
            print("\t%s - %s" % (x.classStart, x.classEnd))
    else:
        print("%s is not currently enrolled in any classes!" % (currentAccount.nickname,))

#removing classes for student accounts
def dropClasses():
    global classList
    global currentAccount
    if(len(currentAccount.curClasses)>0):
        inputCCode = input("Select a class to drop.\nInput class code: ")
        if any(x.classCode for x in classList):
            if inputCCode in currentAccount.curClasses:
                selectedClass = next((c for c in classList if c.classCode == inputCCode),None)
                selectedClass.classNStudents = str(int(selectedClass.classNStudents)-1)
                currentAccount.removeClass(inputCCode)
                currentAccount.removeCourseTaken(selectedClass.classCourse)
                print("Successfully removed %s!" % (inputCCode,))
            else:
                print("You are not enrolled in that class!")
        else:
            print("That class doesn't exist!")
    else:
        print("%s is not currently enrolled in any classes!" % (currentAccount.nickname,))

#login menu for students
def studentLogin():
    exitCond = True
    global studentList
    global currentAccount
    while exitCond:
        username = input("USERNAME: ")
        password = input("PASSWORD: ")
        for x in studentList:
            if x.username == username and x.password == password:
                exitCond = False
                currentAccount = x
                print("Logged in successfully! Welcome, %s" % (currentAccount.nickname,))
                break

        else:
            print("Wrong username and/or Password!") 

#main student menu
def studentMenu():
    studentLogin()
    global currentAccount
    exitCond = True
    while exitCond:
        innerCond = True
        choice = input("----------\n1. Enlist in Classes\n2. Drop Classes\n3. View Classes\n4. Exit\nInput: ")
        while innerCond:
            if(not choice.isdigit()):
                choice = input("Invalid input. Please try again: ")
            elif int(choice) < 1 or int(choice) > 4:
                choice = input("Invalid input. Please try again: ")
            else:
                choice = int(choice)
                innerCond = False

        if choice == 1:
            enlistClasses()
        elif choice == 2:
            dropClasses()
        elif choice == 3:
            viewEnlistedClasses()
        elif choice == 4:
            print("Exiting Class Enlistment.")
            currentAccount = None
            exitCond = False

#login menu for admins
def adminLogin():
    exitCond = True
    global adminList
    global currentAccount
    while exitCond:
        username = input("USERNAME: ")
        password = input("PASSWORD: ")
        for x in adminList:
            if x.username == username and x.password == password:
                exitCond = False
                currentAccount = x
                print("Logged in successfully! Welcome, %s" % (currentAccount.nickname,))
                break

        else:
            print("Wrong username and/or Password!") 

#view ALL classes for admins
def viewClasses():
    global classList
    print("Here are all the current classes available: ")
    for x in classList:
        print("\t%s - %s - %s (Max: %s, Current: %s)" % (x.classCode, x.classCourse, x.className, x.classCap, x.classNStudents))
        print("\t\tProf: %s, Room: %s, Days: %s, Start Time: %s, End Time: %s" % (x.classProf,x.classRoom,x.classDay,x.classStart,x.classEnd))
        print("\t\tPrerequisites: ")
        for y in x.coursePreReqs:
            print("\t\t\t%s" % (y,))

#adding classes into the system for admins
def addClasses():
    global classList
    exitCond = True
    while exitCond:
        innerCond = True
        choice = input("----------\n1. Add a class\n2. Exit\nInput: ")
        while innerCond:
            if(not choice.isdigit()):
                choice = input("Invalid input. Please try again: ")
            elif int(choice) < 1 or int(choice) > 2:
                choice = input("Invalid input. Please try again: ")
            else:
                choice = int(choice)
                innerCond = False

        if choice == 1:
            innerCond2 = True
            while innerCond2:
                innerCond3 = True
                preqList = list()
                innerChoice = input("----------\n1. Set course code\n2. Set class name\n3. Set no. of units\n4. Set class Professor\n5. Set classSection\n6. Set class days\n7. Set start time\n8. Set end time\n9. Set room\n10. Set max no. of students\n11. Add prerequisites\n12. Remove prerequisites\n13. Show prerequisites\n14. Save class\n15. Exit without saving\nInput: ")
                while innerCond3:
                    if not innerChoice.isdigit():
                        innerChoice = input("Invalid input. Please try again: ")
                    elif int(innerChoice) < 1 or int(innerChoice) > 15:
                        innerChoice= input("Invalid input. Please try again: ")
                    else:
                        innerChoice = int(innerChoice)
                        innerCond3 = False
                if innerChoice == 1:
                    inputCCourse = input("Enter the course code for the class: ")
                    inputCCourse = inputCCourse.replace(" ", "_")
                elif innerChoice == 2:
                    inputCName = input("Enter the name of the course for the class: ")
                    inputCName = inputCName.replace(" ", "_")
                elif innerChoice == 3:
                    innerCond4 = True
                    while innerCond4:
                        inputCUnits = input("Enter the number of units for this class: ")
                        if not inputCUnits.isdigit():
                            inputCUnits = input("Invalid input. Please try again: ")
                        elif int(inputCUnits) < 0:
                            inputCUnits = input("Invalid input. Please try again: ")
                        else:
                            innerCond4 = False
                elif innerChoice == 4:
                    inputCProf = input("Enter the name of the professor for this class: ")
                    inputCProf = inputCProf.replace(" ", "_")
                elif innerChoice == 5:
                    inputCSection = input("Enter the section: ")
                    inputCSection = inputCSection.replace(" ", "_")
                elif innerChoice == 6:
                    inputCDays = input("Enter the days when the class is held (Please use M,T,W,H,F,Sa,Su, no spaces e.g. MW): ")
                    inputCDays = inputCDays.replace(" ", "")
                elif innerChoice == 7: 
                    innerCond4 = True
                    while innerCond4:
                        inputCStart = input("Enter the start time for the class. Please use a four digit military time format (e.g. 0940, 1755): ")
                        if len(inputCStart) != 4:
                            inputCStart = input("Invalid input. Please try again: ")
                        elif inputCStart >= "0000" and inputCStart <= "2400":
                            innerCond4 = False
                        else:
                            inputCStart = input("Invalid input. Please try again: ")
                elif innerChoice == 8:
                    innerCond4 = True
                    while innerCond4:
                        inputCEnd = input("Enter the end time for the class. Please use a four digit military time format (e.g. 0940, 1755): ")
                        if len(inputCEnd) != 4:
                            inputCEnd = input("Invalid input. Please try again: ")
                        elif inputCEnd >= "0000" and inputCEnd <= "2400":
                            innerCond4 = False
                        else:
                            inputCEnd = input("Invalid input. Please try again: ")
                elif innerChoice == 9:
                    inputCRoom = input("Enter the room number for the class: ")
                    inputCRoom = inputCRoom.replace(" ", "_")
                elif innerChoice == 10:
                    innerCond4 = True
                    while innerCond4:
                        inputCCap = input("Enter the max number of students for the class: ")
                        if(not inputCCap.isdigit()):
                            inputCCap = input("Invalid input. Please try again: ")
                        elif int(inputCCap) < 0:
                            inputCCap= input("Invalid input. Please try again: ")
                        else:
                            innerCond4 = False
                elif innerChoice == 11:
                    tempInput = input("Add a prerequisite course for this course/class. Input the course code: ")
                    tempInput = tempInput.replace(" ", "_")
                    preqList.append(tempInput)
                elif innerChoice == 12:
                    if len(preqList) > 0:
                        tempInput = input("Remove a prerequisite course for this course/class. Input the course code: ")
                        if tempInput in preqList:
                            preqList.remove(tempInput)
                        else:
                            print("%s is currently not a prerequisite for this class. " % (tempInput,))
                    else:
                        print("There are currently no prerequisites for this class.")
                elif innerChoice == 13:
                    if len(preqList) > 0:
                        print("Here are the prerequisite courses for this class: ")
                        for x in preqList:
                            print("\t>%s" % (x,))
                    else:
                        print("There are currently no prerequisites for this class.")
                elif innerChoice == 14:
                    if None not in (inputCCourse, inputCName, inputCUnits, inputCProf, inputCSection, inputCDays, inputCStart, inputCEnd, inputCRoom, inputCCap):
                        tempCCode = str("{:03d}".format(len(classList) + 1))
                        classList.append(Classes(tempCCode, inputCCourse, int(inputCUnits), inputCName, preqList, inputCProf, inputCSection, inputCDays, inputCStart, inputCEnd, inputCRoom, int(inputCCap),0))
                        print("Successfully added class! Class code: %s" % (tempCCode,))
                        innerCond2 = False
                    else:
                        print("One or more of the settings are still unconfigured! Please fill in the settings. (Prerequisites can be left blank)")
                elif innerChoice == 15:
                    exitInput = input("Are you sure you want to exit without saving the class? (Y/N)")
                    if exitInput == "Y" or exitInput == "y" or exitInput == "Yes" or exitInput == "yes":
                        innerCond2 = False
        elif choice == 2:
            exitCond = False

#removing classes from the system for admins
def removeClasses():
    global classList
    inputCode = input("Select a class to delete. Enter the class code: ")
    if any(x.classCode == inputCode for x in classList):
        tempClass = next((x for x in classList if x.classCode == inputCode), None)
        classList.remove(tempClass)
        print("%s successfully removed!" % (tempClass.classCode))
    else:
        print("The class with that class code does not exist!")

#main admin menu
def adminMenu():
    adminLogin()
    global currentAccount
    exitCond = True
    while exitCond:
        innerCond = True
        choice = input("----------\n1. Add Classes\n2. Remove Classes\n3. View Classes\n4. Exit\nInput: ")
        while innerCond:
            if(not choice.isdigit()):
                choice = input("Invalid input. Please try again: ")
            elif int(choice) < 1 or int(choice) > 4:
                choice = input("Invalid input. Please try again: ")
            else:
                choice = int(choice)
                innerCond = False

        if choice == 1:
            addClasses()
        elif choice == 2:
            removeClasses()
        elif choice == 3:
            viewClasses()
        elif choice == 4:
            print("Exiting admin menu.")
            currentAccount = None
            exitCond = False

#main menu
def start():
    exitCond = True
    while exitCond:
        innerCond = True
        choice = input("Welcome to Class Enlistment System.\n1. Log in as student\n2. Log in as admin\n3. Exit\nInput: ")
        while innerCond:
            if(not choice.isdigit()):
                choice = input("Invalid input. Please try again: ")
            elif int(choice) < 1 or int(choice) > 3:
                choice = input("Invalid input. Please try again: ")
            else:
                choice = int(choice)
                innerCond = False

        if choice == 1:
            studentMenu()
        elif choice == 2:
            adminMenu()
        elif choice == 3:
            saveStudents()
            saveClasses()
            exitCond = False



classList = list()
studentList = list()
adminList = list()
currentAccount = None

loadClasses()
loadStudents()
loadAdmins()

start()