
import requests

class ModelAPI():

    def __init__(self,endpoint_name,port = 5000):
        self.url = f"http://localhost:{port}/{endpoint_name}"

    def is_active(self):
        try:
            requests.get(self.url).json() 
            active = True
        except:
            active = False

        return active

    def encoding_dict(self):
        encoding_dict = None
        if self.is_active():
            resp = requests.get(self.url).json()
            encoding_dict = resp['encoding_dict']
        return encoding_dict
        
    
    def predict(self,img_path_list):
        if not self.is_active():
            return None

        if isinstance(img_path_list,str):
            img_path_list = [img_path_list]

        pred_dict = {}
        for img_path in img_path_list:
            try:
                resp = requests.post(self.url, files={"file": open(img_path,'rb')}).json() 
                #print(resp)    
                pred_dict.update({img_path:{'class':resp['class_name'],'XAI_path':resp['XAI_path']}})
            except:
                print(f'Something went wrong when predicting {img_path}') 

        return pred_dict


# model = ModelAPI('sortifier',port = 5000)


# img_path_list = ['tmp.jpg']

# pred_dict = model.predict(img_path_list)
# encoding_dict = model.encoding_dict()
# print(pred_dict)


