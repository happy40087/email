import urllib,re
f = urllib.urlopen("https://www.cs.ccu.edu.tw/index2.php")
s = f.read()


print(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s))