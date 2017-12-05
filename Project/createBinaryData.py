import json

with open('data.txt', mode='r') as f:
    content = f.readlines()
    content = [x.strip() for x in content]
    content.remove(content[0])

    symptoms = dict()
    symptomsList = []
    diseases = dict()
    
    #res = []
    for item in content:
        p = item.split("\t")
        
        if(p[0] not in symptoms):
            symptomsList.append(p[0])
            symptoms[p[0]] = 0

        if(p[1] not in diseases):
            diseases[p[1]] = []

        symptoms[p[0]] += 1
        diseases[p[1]].append(p[0])
    
    data = []

    i=0
    for key in diseases:
        data.append([])
        for symptom in symptomsList:
            if(symptom in diseases[key]):
                data[i].append(1)
            else:
                data[i].append(0)
        data[i].append(key)
        i += 1

    print(data)