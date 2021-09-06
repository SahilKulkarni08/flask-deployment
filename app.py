from flask import Flask,render_template,request
import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
app=Flask(__name__)
model=load_model('model1.h5')
def model_predict(img_path,model):

    test_image=image.load_img(img_path,target_size=(64,64))
    test_image=image.img_to_array(test_image)
    test_image=test_image/255
    test_image=np.expand_dims(test_image,axis=0)
    result=model.predict(test_image)
    return result

@app.route('/',methods=['GET'])
def index():
    return render_template('web.html')


@app.route('/success',methods=['GET','POST'])
def upload_file():
   if request.method == 'POST':
       f = request.files['u_img']
       basepath = os.path.dirname(os.path.realpath('__file__'))
       file_path = os.path.join(basepath, 'static/upload_img', secure_filename(f.filename))
       f.save(file_path)
       print(file_path)
       result = model_predict(file_path,model)
       print(result)
       if (result<0.5):
          return render_template('web.html', pred="it's a Kitty")
       else:
         return render_template('web.html', pred1="it's a Doggo")


if __name__ == '__main__':
        app.debug = True
        app.run(
