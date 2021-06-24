from flask import Flask , render_template, request, send_file,flash
import zipfile
import io
import pathlib
import shutil

from script import getJson

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SPLN2021'

@app.route("/", methods=['GET'])
def home():
    cond = False
    return render_template('ExtrairJson.html',condition=cond)

@app.route("/procurar", methods=['POST'])
def procurar():
    
    try:
        shutil.rmtree("JsonsTemp/")
    except OSError as e:
      print ("Ficheiro ainda não existe: %s - %s." % (e.filename, e.strerror))
    
    cond = getJson(request.form.get("link"),request.form.get("palavra"))
    if(cond):
        flash("Foram encontrados jsons!")
    else:
        flash("Não foram encontrados jsons!")

    return render_template('ExtrairJson.html',condition=cond)

@app.route('/download', methods=['POST'])
async def downloadFile ():

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

if __name__ == "__main__":
    app.run(debug=True)