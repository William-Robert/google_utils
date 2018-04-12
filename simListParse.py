from bs4 import BeautifulSoup as bs

def simListParse(item):

    soup = bs(item, 'lxml')
    tempList = soup.find('a').contents

    conList = [x.encode('utf-8') for x in tempList]
    out =  " ".join(conList)

    out = out.replace('<b>', '')
    out = out.replace('</b>', '')
    out = out.replace('  ', ' ')

    return out


