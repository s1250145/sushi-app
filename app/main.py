from flask import request, Flask, render_template
from flask_cors import CORS
from PIL import Image
import base64
from io import BytesIO
from Sushi_AI import SushiAI

app = Flask(__name__)
CORS(app)

title = '寿司食いねェ!'

def create_image_src(image):
    buffer = BytesIO()
    image.save(buffer, format='png')
    b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    image_src = f'data:image/jpg;base64,{b64}'
    return image_src

@app.route('/')
def index():
    return render_template('index.html', title=title)

@app.route('/helloai', methods=['GET', 'POST'])
def getResult():
    if request.method == 'POST':
        file = request.files['sushi']
        image = Image.open(file)
        ai = SushiAI(image)
        result = ai.predict()
        src = create_image_src(result[2])
        if len(result) == 4:
            return render_template('index.html', title='おあいそ', flag=True, fail=False, shop=result[0], neta=result[1], src=src, detail=result[3])
        else:
            return render_template('index.html', title='またきて', flag=True, fail=True, shop=result[0], neta=result[1], src=src)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
