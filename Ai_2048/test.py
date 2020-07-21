
import GameManager as gm
import os
def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)



def initTest(each=10):
    trial=[]
    for k in range(each):
        trial.append(gm.main())
    t=sorted(trial)
    p=t
    t=t[5:]
    q=f'least is {t[0]}, most is {t[-1]}, median is {t[int(len(t)/2)]} mean/average is {sum(t)/len(t)} raw top 5 data is {t}, raw is {p}'
    addToClipBoard(q)
    print(q)
initTest()