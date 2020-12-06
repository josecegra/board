
def Sortifier(img_path_list):
    import requests
    url = "http://localhost:5050/sortifier"

    if isinstance(img_path_list,str):
        img_path_list = [img_path_list]

    pred_dict = {}
    for img_path in img_path_list:
        #try:
        resp = requests.post(url, files={"file": open(img_path,'rb')}).json() 
        print(resp)    
        pred_dict.update({img_path:resp['class_name']})
        #except:
        #print(f'Something went wrong when predicting {img_path}') 

    return pred_dict


img_path_list = ['tmp.jpg']
pred_dict = Sortifier(img_path_list)
print(pred_dict)
