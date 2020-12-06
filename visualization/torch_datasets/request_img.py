import requests
# url = 'http://127.0.0.1:8000/snippets/6/predict/'
# file_path = 'C:/Users/Jose Eduardo/Desktop/Charite/nilt/XAI/done/IoU_0.001_00218044_20200218_132007_46dm.jpg'
# files = {'upload_file': open(file_path,'rb')}
# #values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}
# r = requests.post(url, files=files)
# print(r)

url = "http://localhost:5050/shutdown"
r = requests.post(url)
print(r)
