from collections import OrderedDict
import copy

applicantsList = []
coursesList = []
preferencesDict = OrderedDict()
coursesInTies = []
applicantQuota = {}
courseQuota = {}
flag = True

print ("GENERALIZED SERIAL DICTATORSHIP WITH TIES\n")
#While user gives applicants names, ends when there are no more applicants.
while flag == True:
    i = 1
    flag2 = True
    quotaCheck = False
    personalPreferences = []
    applicant = input("Give applicant's name or 0 if there are no more applicants: \n")
    if (applicant != '0'):
            while quotaCheck == False:
                    quota = input("Give the course quota of this applicant, not 0 : \n")
                    if quota !='0':
                            applicantQuota[applicant] = quota
                            quotaCheck = True
                    else:
                            quotaCheck = False
            while flag2 == True:
                    print ("For (",i,") preference")
                    lesson = input("Give name of the course or names separated with (,) or press 0 if there are no more courses for this applicant: \n")
                    if lesson != '0':
                            if ',' in lesson:
                                coursesInTies = lesson.split(',')
                                for course in coursesInTies:
                                        if (course not in coursesList):
                                                coursesList.append(course)
                                personalPreferences.append(coursesInTies)
                            else:
                                if (lesson not in coursesList):
                                    coursesList.append(lesson)
                                personalPreferences.append([lesson])
                            i=i+1
                    else:
                            flag2=False
            preferencesDict[applicant] = personalPreferences
            applicantsList.append(applicant)
    else:
            flag=False

for course in coursesList:
        print ("For lesson ",course)
        courseQuota[course] = input("Give this course's quota :\n")

for applicant in applicantsList:
    if int(applicantQuota[applicant])>len(preferencesDict[applicant]):
        print ("Ο υποψήφιος : ",applicant," δεν έχει δώσει αρκετές προτιμήσεις σχετικά με το quota του.")
        while flag2 == True:
                print ("For (",i,") preference")
                lesson = input("Give name of the course or names separated with (,) or press 0 if there are no more courses for this applicant: \n")
                if lesson != '0':
                        if ',' in lesson:
                            coursesInTies = lesson.split(',')
                            for course in coursesInTies:
                                    if (course not in coursesList):
                                            coursesList.append(course)
                            personalPreferences.append(coursesInTies)
                        else:
                            if (lesson not in coursesList):
                                coursesList.append(lesson)
                            personalPreferences.append([lesson])
                        i=i+1
                else:
                        flag2=False
        preferencesDict[applicant] = personalPreferences

#print (courseQuota)
#print (applicantQuota)               
#print (preferencesDict)
#print (coursesList)
#print (applicantsList)

def create_start_nodes (applicantsList, preferencesDict, coursesList):
    start_nodes = []
    start_nodes += ["s"] * len(applicantsList)

    number_of_ties = {}

    for applicant in preferencesDict:
        number_of_ties[applicant] = len(preferencesDict[applicant])

    for applicant in applicantsList:
        start_nodes += [applicant] * number_of_ties[applicant]

    for applicant in preferencesDict:
        for tie in preferencesDict[applicant]:
            start_nodes += [tie] * len(tie)

    for course in coursesList:
        start_nodes += [course]

    return start_nodes

def create_end_nodes (applicantsList, preferencesDict, coursesList):
    end_nodes = []
    for applicant in applicantsList:
        end_nodes += [applicant]

    for applicant in preferencesDict:
        for tie in preferencesDict[applicant]:
            end_nodes += [tie]

    for applicant in preferencesDict:
        for tie in preferencesDict[applicant]:
            for lesson in tie:
                end_nodes += [lesson]

    end_nodes += ["t"] * len(coursesList)

    return end_nodes

def create_capacities (applicantsList, preferencesDict, coursesList, courseQuota):
    capacity = []
    for applicant in applicantsList:
        capacity += [0]

    for applicant in preferencesDict:
        for tie in preferencesDict[applicant]:
            capacity += [0]

    for applicant in preferencesDict:
        for tie in preferencesDict[applicant]:
            for lesson in tie:
                capacity += [1]

    for course in coursesList:
        capacity += [int(courseQuota[course])]

    return capacity

def create_flow (applicantsList, preferencesDict, coursesList):
    flow = []
    for applicant in applicantsList:
        flow += [0]

    for applicant in preferencesDict:
        for tie in preferencesDict[applicant]:
            flow += [0]

    for applicant in preferencesDict:
        for tie in preferencesDict[applicant]:
            for lesson in tie:
                flow += [0]

    for course in coursesList:
        flow += [0]

    return flow

#print ("\n")
start_nodes_list = create_start_nodes(applicantsList, preferencesDict, coursesList)
#print (start_nodes_list)
#print ("\n")
end_nodes_list = create_end_nodes(applicantsList, preferencesDict, coursesList)
#print (end_nodes_list)
#print ("\n")
capacity_list = create_capacities(applicantsList, preferencesDict, coursesList, courseQuota)
#print (capacity_list)
#print ("\n")
flow_list = create_flow(applicantsList, preferencesDict, coursesList)
#print (flow_list)

def max_flow_matches(applicantsList, preferencesDict, coursesList, courseQuota, applicantQuota):
    preferencesDict2 = copy.deepcopy(preferencesDict)
    M = {}
    max_Quota = 0

    for applicant in applicantQuota:
        if int(applicantQuota[applicant])>max_Quota:
            max_Quota = int(applicantQuota[applicant])

    max_Quota+=1

    #print (max_Quota)

    for i in range(1,max_Quota):

        for applicant in applicantsList:
            if int(applicantQuota[applicant]) >= i:

                k = return_capacity(start_nodes_list, end_nodes_list, "s", applicant)
                capacity_list[k] += 1
                flow_list[k] +=1
                print ("\nΜια μονάδα ροής πέρασε από τη πηγή στον υποψήφιο: ",applicant)

                k = return_capacity(start_nodes_list, end_nodes_list, applicant, preferencesDict[applicant][0])
                if capacity_list[k] < len(preferencesDict[applicant][0]):
                    capacity_list[k] += 1
                    if flow_list[k] < capacity_list[k]:
                        flow_list[k] =+ 1
                print ("Μια μονάδα ροής πέρασε από τον υποψήφιο: ",applicant," στην επιλογή του: ",preferencesDict[applicant][0])

                k = return_capacity(start_nodes_list, end_nodes_list, preferencesDict[applicant][0], preferencesDict[applicant][0][0])
                if flow_list[k] < 1:
                    flow_list[k] += 1
                print ("Μια μονάδα ροής πέρασε από την επιλογή: ",preferencesDict[applicant][0], " στο μάθημα: ",preferencesDict[applicant][0][0])

                k = return_capacity(start_nodes_list, end_nodes_list, preferencesDict[applicant][0][0], "t")
                if flow_list[k]<capacity_list[k]:
                    flow_list[k] += 1
                    if applicant in M:
                        M[applicant] = [M[applicant],preferencesDict[applicant][0][0]]
                    else:
                        M[applicant] = preferencesDict[applicant][0][0]
                    print ("Μια μονάδα ροής πέρασε από το μάθημα: ",preferencesDict[applicant][0][0], " στο τελικό κόμβο: ")
                    print ("Μέχρι τώρα τα ταιριάσματα είναι: ",M)
                else:
                    if can_someone_pick_something_else(preferencesDict[applicant][0][0], preferencesDict2, M, i) != [50,50]:
                        o = can_someone_pick_something_else(preferencesDict[applicant][0][0], preferencesDict2, M, i)
                        M[o[0]] = o[1]
                        M[applicant] = preferencesDict[applicant][0][0]
                        print ("Έγινε αναπροσαρμογή και τώρα τα ταιριάσματα είναι: ",M)
                    else:
                        print ("Δεν γίνεται να αλλάξει την επιλογή του: ")

                #if len(preferencesDict[applicant][0])>1:
                    #del preferencesDict[applicant][0][0]
                #else:
                del preferencesDict[applicant][0]
    return M

def return_capacity(start_nodes_list, end_nodes_list, start_node, end_node):
    for i in start_nodes_list:
        for j in end_nodes_list:
            if i == start_node and j == end_node:
                return start_nodes_list.index(i)

def can_someone_pick_something_else(lesson, preferencesDict2, M, i):
    #print (preferencesDict2)
    owner_list = []
    found = False

    for applicant in M:
        if M[applicant] == lesson:
            owner_list.append(applicant)
            #print ("Ο κάτοχος του μαθήματος ",lesson,"είναι ο ",owner)

    while found == False:

        for owner in owner_list:
            for tie in preferencesDict2[owner]:
                for les in tie:
                    if les == lesson:
                        #print("βρεθηκε το μάθημα στο σύνολο ",tie)
                        tie_with_lesson = tie
                        p = preferencesDict2[owner].index(tie_with_lesson)
                        #print (p)
                        r = preferencesDict2[owner][p].index(lesson)
                        #print (r)

            if len(preferencesDict2[owner][p]) != 1:
                #del preferencesDict2[owner][p][r]
                #if p == i:
                for course in preferencesDict2[owner][p]:
                    if course != lesson:
                        #print (return_capacity(start_nodes_list, end_nodes_list, preferencesDict2[owner][p], course))
                        #if flow_list[return_capacity(start_nodes_list, end_nodes_list, preferencesDict2[owner][p], le)] == 0:
                        l = return_capacity(start_nodes_list, end_nodes_list, course, "t")
                        if flow_list[l] < capacity_list[l]:
                            found = True
                            #print ("θα παρει αλλο")
                            return [owner, course]
                        else: 
                            return[50,50]

print ("Pareto Optimal Matches are: ",max_flow_matches(applicantsList, preferencesDict, coursesList, courseQuota, applicantQuota))