from flask import Flask , render_template, request, send_file
from forms import ExtrairJson
import zipfile
import io
import pathlib
import shutil

from script import getJson

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SPLN2021'
app.config['UPLOAD_FOLDER'] = 'JsonsTemp/'

@app.route("/", methods=['GET','POST'])
def home():
    form = ExtrairJson()
    if(form.is_submitted()):
        result = request.form 
        try:
            shutil.rmtree("JsonsTemp/")
        except OSError as e:
          print ("Error: %s - %s." % (e.filename, e.strerror))
        
        getJson(result['link'],result['palavra'])

    return render_template('ExtrairJson.html',form=form)

@app.route('/download')
async def downloadFile ():
    form = ExtrairJson()

    base_path = pathlib.Path('./JsonsTemp/')
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as z:
        for f_name in base_path.iterdir():
            z.write(f_name)
    data.seek(0)

    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='data.zip'
    )
