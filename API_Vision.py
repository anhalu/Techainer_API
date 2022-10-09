import os
from xmlrpc.client import ResponseError
from google.cloud import vision
from googletrans import Translator 
from flask import Flask, request, json

import numpy as np

# image_path = '/home/anhalu/vscode/Techainer/API_GOOGLE/test1.jpg'

# with io.open(image_path, 'rb') as image_file:
#     content = image_file.read()

# construct an iamge instance
# image = vision.Image(content=content)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"key.json" 
client = vision.ImageAnnotatorClient()
translator = Translator() 
app = Flask(__name__)

class NumpyEncoder(json.JSONEncoder):
    '''
    Encoding numpy into json
    '''
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.int32):
            return int(obj)
        if isinstance(obj, np.int64):
            return int(obj)
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.float64):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

@app.route("/")
def _hello_world():
	return "Hello world" 
    

@app.route("/an" , methods=["POST"])
def get() : 
    """
    # or we can pass the image url
    image = vision.types.Image()
    image.source.image_uri = 'https://edu.pngfacts.com/uploads/1/1/3/2/11320972/grade-10-english_orig.png'
    """
    data={'process': False}
    if request.files.get("image"):
        image = request.files["image"].read()
        # image = Image.open(io.BytesIO(image))
        # print(type(image))
        
        image = vision.Image(content=image)
    # annotate Image Response
        response = client.text_detection(image=image)  # returns TextAnnotation
        texts = response.text_annotations
        input = texts[0].description 
        # print(input) 
        list_s = input.split('\n') 

        list_s = list_s[1:] 

        name = []
        price = []

        for s in list_s: 
            id = -1
            for i in range(len(s)) : 
                if(s[i] >= '0' and s[i] <='9' ): 
                    id = i 
                    break; 
            
            if(id==-1) : id = len(s)
            
            if(id != 0) : name.append(s[:id]) 
            if(id != len(s)) : price.append(s[id:]) 
        
        # print(name) 
        name_en = [] 
        
        
        for i in range(len(name)): 
            name_en.append(translator.translate(name[i], dest='en').text) 
            

        print(name_en)

        dic = {} 
        #
        for i in range(len(name_en)):  
            dic[i] = {
                'food' : name_en[i], 
                'price' : price[i]
            }
        print(dic) 
    return json.dumps(dic, ensure_ascii=False, cls=NumpyEncoder)
    # return json.dumps(dic)

if __name__ == "__main__":
	print("App run!")
	# Load model
	# model = utils._load_model()
	app.run(debug=False, host="127.0.0.1", threaded=False)
    
    
