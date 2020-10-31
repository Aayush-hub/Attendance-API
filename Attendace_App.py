import requests
import re 
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

def calc(username,password):
   
    # Represents browser information
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
    }
      
    # Represents login credentials
    login_data = {                     
        'username': username,
        'password': password
    }
    
    # Session created for information scraping
    with requests.Session() as s:
        url = "http://app.bmiet.net/student/login"
        r = s.get(url, headers=header)
        soup = BeautifulSoup(r.content, 'html.parser')
        login_data['_token'] = soup.find('input', {'name': '_token'})['value']
        post = s.post('http://app.bmiet.net/student/student-login',login_data, headers=header)
    
    # Find all the links present on the curret page
    def link_finder():
        dat = s.get('http://app.bmiet.net/student/attendance/view',headers=header)
        soup = BeautifulSoup(dat.content, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links
    
    # Calculate total pages
    def pagecal(links):
        x = True 
        i = 2
        while x:
            val = 'http://app.bmiet.net/student/attendance/view?page='+ str(i)
            if val in links: i += 1
            else: break
        return i

    Tot_absent = 0
    Tot_present = 0
    links = link_finder()
    num = pagecal(links)
    for j in tqdm(range(1,num),desc = 'Calculating'):
        info = s.get('http://app.bmiet.net/student/attendance/view?page='+str(j), headers=header)
        res = re.findall(r'\w+', str(info.content))
        Tot_present += res.count('Present')
        Tot_absent += res.count('Absent')
        Tot_attend = round((Tot_present/(Tot_present+Tot_absent))*100,2)
        time.sleep(1)
    print(' Total Present:',Tot_present,'| Total Absent:',Tot_absent,'\n',f'Total Attendance: {Tot_attend} %')
    
    if Tot_attend < 75:
        b = 0.75*(Tot_present+Tot_absent)
        q = int(b-(Tot_present))
        print(f" You Have to attend {q} classes")
    elif Tot_attend > 75:
        a = 0.75*(Tot_present+Tot_absent)
        q = int((Tot_present)-a)
        print(f' You Can bunk {q} classes')

    
username = input("Enter Username: ")
password = input("Enter Password: ")
calc(username,password)
