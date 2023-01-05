import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
from colorama import Fore, init
from numpy import *
init(convert=True)
def check(cls):
    ncls = []
    for i in cls:
        if i.get_text():
            ncls.append(i)
    return ncls          
LINK = "https://economictimes.indiatimes.com/marketstats/pid-3,pageno-1,sortby-,sortorder-value,service-valuemovers,exchange-50.cms"
def main_work():
    print("[server]Connecting to site...")

    r = requests.get(LINK)


    print(f"[server]Connected! code[{r}]")


    soup = BeautifulSoup(r.content, 'html.parser')

    print("[server]Searching data...")

    raw_C_Name  = soup.find_all("p",class_="flt")
    raw_LTP     = soup.find_all("span",class_="ltp")
    raw_Change  = soup.find_all("span",class_="change")
    raw_PChange = soup.find_all("span",class_="pchange")
    raw_Value   = soup.find_all("span",class_="vol")
    _flt   = soup.find_all("span", class_ = "flt")
    _flr   = soup.find_all("span", class_ = "flr")

    raw_flt = check(_flt)
    raw_flr = check(_flr)

    lis_C_Name  = []
    lis_LTP     = []
    lis_Change  = [] 
    lis_PChange = []
    lis_Value   = []
    lis_flt = []
    lis_flr = []


    print("[server]Data Found")
    print(f"[server]Total Rows[{len(raw_C_Name)}]")
    print("[server]Formatting Data...")

    one_per = int(100/len(raw_C_Name))

    for i in range(1,len(raw_C_Name)+1):
        print(f"completed[{i*one_per}%]")
        C_Name  = raw_C_Name[i-1].get_text()
        LTP     = raw_LTP[i-1].get_text()
        Change  = raw_Change[i-1].get_text()
        PChange = raw_PChange[i-1].get_text()
        Value   = raw_Value[i-1].get_text()
        flt = raw_flt[i-1].get_text()
        flr = raw_flr[i-1].get_text()
        
        lis_C_Name.append(C_Name)
        lis_LTP.append(LTP)
        lis_Change.append(Change)
        lis_PChange.append(PChange)
        lis_Value.append(Value)
        lis_flt.append(flt)
        lis_flr.append(flr)

    print("succesfull! ")
    variables = {"Company":1,
                "LTP":2,
                "Day's Low":3, 
                "Day's High":4, 
                "Change":5,
                "%Change":6,
                "Value(Cr.)":7}
    main_lis = [["Index", "Company", "LTP", "Day's Low", "Day's High", "Change", "%Change", "Value(Cr.)"]]

    for i in range(1,len(raw_C_Name)+1):
        index = i
        color = ""
        if index > 0:
            if float(lis_Change[i-1])< 0:
                color = Fore.RED
            else:
                color = Fore.GREEN

        main_lis.append([color+str(i),lis_C_Name[i-1], lis_LTP[i-1], lis_flt[i-1], lis_flr[i-1], lis_Change[i-1], lis_PChange[i-1], lis_Value[i-1]])

    for index, val in enumerate(main_lis, start=0):
        pass
    print(tabulate(main_lis, headers="firstrow", tablefmt="fancy_grid"))
    print(Fore.WHITE)
    
    return array(main_lis), variables

main_lis,variables = main_work()

while True:
    inp = input()
    if not(inp.isnumeric()):
        if "-" in inp:
            a,b = inp.split("-")
            print(tabulate(main_lis[int(a):int(b)+1], headers=main_lis[0], tablefmt="fancy_grid"))
            print(Fore.WHITE)
    
        elif inp.lower() == "r":
            main_lis,variables = main_work()
        elif inp == "c":
            print(".> Select Coulomns using their Coulumn numbers")
            print(".> Press enter to confirm selection")
            print(variables)
            c = [0]

            for i in range(0,7):
                n = input(f".> Coulomn[{i+1}]: ")
                if not(n.isnumeric()):
                    break
                else:
                    c.append(int(n))

            if c != [0]:
                lis = []

                for x in main_lis:
                    lis.append(x[c])
                print("Select Row or press enter to select all rows")
                row = input(".> ")
                
                if not(row.isnumeric()):
                    
                    if "-" in row:
                        a,b = row.split("-")
                        print(tabulate(lis[int(a):int(b)+1], headers=lis[0], tablefmt="fancy_grid"))

                    else:
                        print(tabulate(lis, headers=lis[0], tablefmt="fancy_grid"))
                else:
                    print(tabulate([lis[int(row)]], headers=lis[0], tablefmt="fancy_grid"))
        else:
            break
    else:
        print(tabulate([main_lis[int(inp)]], headers=main_lis[0], tablefmt="fancy_grid"))
        print(Fore.WHITE)