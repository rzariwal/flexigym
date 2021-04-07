x = '106.10.28.73 - Galvin [21/Mar/2021:12:18:57 -0700] "GET /doc/readme.txt HTTP/2.0" 200 7053'

print(x.split(' ')[3].lstrip('[').rstrip(' '))
