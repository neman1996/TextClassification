import json

with open('data.txt', mode='r') as f:
    content = f.readlines()
    content = [x.strip() for x in content]
    content.remove(content[0])

    symptoms = dict()
    diseases = dict()
    #res = []
    for item in content:
        p = item.split("\t")
        
        if(p[0] not in symptoms):
            symptoms[p[0]] = 0

        if(p[1] not in diseases):
            diseases[p[1]] = []

        symptoms[p[0]] += 1
        diseases[p[1]].append(p[0])
    
    #print(json.dumps(symptoms, indent=4))

    minCount = 320

    
    minCountSymptoms = []

    # Considering symptoms with count more than minCount
    for key in symptoms.keys():
        if(symptoms[key] > minCount):
            minCountSymptoms.append(key)

    minCountDiseases = {}
    for key in diseases.keys():
        flag = True
        for symptom in diseases[key]:
            flag = flag and symptom in minCountSymptoms
        if(flag):
            minCountDiseases[key] = diseases[key]

    trainingSet = {}
    testingSet = {}
    
    i = 0
    for key in minCountDiseases.keys():
        if(i < 800):
            trainingSet[key] = minCountDiseases[key]
        else:
            testingSet[key] = minCountDiseases[key]
        i +=1

    print(json.dumps(testingSet, indent=4))
    #print( len(trainingSet.keys()), len(testingSet.keys()) ) 
    #print(json.dumps(minCountDiseases, indent=4))

    """newDiseases = {}
    minSymTh = 5
    maxSymTh = 10

    for key in diseases.keys():
        if(len(diseases[key]) <= maxSymTh and len(diseases[key]) >= minSymTh):
            newDiseases[key] = diseases[key]
    
    newSymptoms = []
    for key in newDiseases.keys():
        for symptom in newDiseases[key]:
            if(symptom not in newSymptoms):
                newSymptoms.append(symptom)
    
    
    print(len(newSymptoms))"""
    
    #print(json.dumps(newDiseases, indent=4))
    
    #print(json.dumps(diseases, indent=4))
        
        
    """    curr = dict()
        for i in range(len(p)):
            if(i is 0):
                curr['symptom'] = p[i]
            if(i is 1):
                curr['disease'] = p[i]
            if(i is 2):
                curr['occurrence'] = p[i]
            if(i is 3):
                curr['tfidf'] = p[i]
        res.append(curr)
    print(json.dumps(res,indent=4))"""