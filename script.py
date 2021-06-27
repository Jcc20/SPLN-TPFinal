#!/usr/bin/python3
import os
from bs4 import BeautifulSoup
from bs4.builder import FAST  

import requests, re, json, sys



def validateJSON(jsonData):
    try:
        json_object = json.loads(jsonData)
        json_formatted_str = json.dumps(json_object, indent=2)
    except ValueError as err:
        return jsonData
    return json_formatted_str


def getJson(link,name):
    bool = True
    pag = requests.get(link) 
    soup = BeautifulSoup(pag.text, 'html.parser')
    matches = soup.find_all(string=re.compile(name))
    i=0
    for match in matches:
        match = re.sub(r"}\n","};\n",match) 
        match = re.sub(r"(?<=[^;])\n"," ",match) 
        #f = open('flash'+str(i)+'.txt', "w")
        #i+=1
        #f.write(match)
        #f.close()
        list = re.findall(rf'(?:const|var)\ ([\w]*)\ ?\=(.*{name}.*)\;', match)
        for (name,content) in list:
            bool = False
            if not os.path.exists('JsonsTemp/'):
                os.makedirs('JsonsTemp/')
            t = open('JsonsTemp/'+name+'.json', "w")
            json_prettify = validateJSON(content)
            t.write(json_prettify)
            t.close()
    if (bool):
        print("Não foram encontrados resultados!")
        return False
    else:
        print("Terminou com sucesso!")
        return True

def main():
    #getJson("https://ge.globo.com/futebol/futebol-internacional/futebol-portugues/",sys.argv[1])
    #getJson("https://www.flashscore.pt/",sys.argv[1])
    getJson(sys.argv[1],sys.argv[2])


