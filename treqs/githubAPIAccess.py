import requests

r = requests.get('https://api.github.com/repos/regot-chalmers/treqs/issues?state=open')
data = r.json()

for currentItem in data:
    print('ITEM:')
    labelSet = set()
    for currentLabel in currentItem['labels']:
        print currentLabel['name']
        labelSet.add(currentLabel['name'])
        
    if 'user story' in labelSet:
        print currentItem['body']
    
    print('')
    
#print data[0]['labels'][0]['name']
#print data[0]['body']