import requests
import re
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from tkinter import Tk , Label , Frame ,StringVar , Entry , Button

root = Tk()
root.geometry("600x400")
root.maxsize(650, 450)
root.minsize(550, 350)
root.title("My Attendance Calculator")
my = Label(text="Attendance Calculator", bg='Green',
            fg='White', font=('comicsansms', 19, 'bold'))
my.pack()
f = Frame(root, bg="grey", padx=50, pady=50)

my1 = Label(f, text="Enter Username Here")
my1.pack()
user1 = StringVar()
user1.set("")
screen1 = Entry(f, textvar=user1, font='comicsansms 20 bold')
screen1.pack(pady=10)
my2 = Label(f, text="Enter Password Here")
my2.pack()

user2 = StringVar()
user2.set("")
screen2 = Entry(f, textvar=user2, font='comicsansms 20 bold')
screen2.pack(pady=10)

f.pack(pady=10)

def att():
    
    def calc(q,w):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
        }
        login_data = {
            'username': q,
            'password': w
        }
        with requests.Session() as s:
            url = "http://app.bmiet.net/student/login"
            r = s.get(url, headers=header)
            soup = BeautifulSoup(r.content, 'html.parser')
            login_data['_token'] = soup.find(
                'input', {'name': '_token'})['value']
            post = s.post('http://app.bmiet.net/student/student-login',
                            login_data, headers=header)

        def link_finder():
            dat = s.get('http://app.bmiet.net/student/attendance/view',
                        headers=header)
            soup = BeautifulSoup(dat.content, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]
            return links

        def pagecal(links):
            x = True
            i = 2
            while x:
                val = 'http://app.bmiet.net/student/attendance/view?page=' + \
                    str(i)
                if val in links:
                    i += 1
                else:
                    break
            return i
        Tot_absent = 0
        Tot_present = 0
        links = link_finder()
        num = pagecal(links)
        for j in tqdm(range(1, num), desc='Calculating'):
            info = s.get(
                'http://app.bmiet.net/student/attendance/view?page='+str(j), headers=header)
            res = re.findall(r'\w+', str(info.content))
            Tot_present += res.count('Present')
            Tot_absent += res.count('Absent')
            Tot_attend = round((Tot_present/(Tot_present+Tot_absent))*100, 2)
            time.sleep(1)
            x = print(' Total Present:',Tot_present,
                      '| Total Absent:',Tot_absent,'\n',
                      f'Total Attendance: {Tot_attend} %')
    
        
        
        
        
        if Tot_attend < 75:
            b = 0.75*(Tot_present+Tot_absent)
            q = int(b-(Tot_present))
            y = print(f" You Have to attend {q} classes")
                      
                        

        elif Tot_attend > 75:
            a = 0.75*(Tot_present+Tot_absent)
            q = int((Tot_present)-a)
            z  = print(f' You Can bunk {q} classes')
                       
        my3 = Label(text='Result is on Window')
        my3.pack(pady=50)
        result = StringVar()
        result.set(x)
        # screen_result = Entry(f, textvar=result, font='comicsansms 20 bold')
        # screen_result.pack(pady=10)
        
    q = screen1.get()
    w = screen2.get()
    calc(q,w)
b = Button(f, text="Enter",command = att)
b.pack(pady=10)


root.mainloop()
