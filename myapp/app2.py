from flask import Flask, render_template, json, request, flash, redirect, url_for, session

from base64 import b64encode, b64decode, encodestring, decodestring
import base64

import cloudant
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.query import Query

serviceURL = "$enter bluemix url$"

client = Cloudant("$your username$",
                  "$your password$",
                  url=serviceURL)
client.connect()

databaseName = "volunteer"

myDatabase = client.create_database(databaseName)
if myDatabase.exists():
    print("'{0}' successfully created.\n".format(databaseName))

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def main():
    return render_template('index.html')


@app.route("/maps")
def volunteerLocation():

    return render_template('maps.html', dicto=dicto)

@app.route("/showSignUp", methods=['GET', 'POST'])
def showSignUp():
    if request.method == 'POST':
        _name = request.form.get('inputName')
        _email = request.form.get('inputEmail')
        _phoneme = request.form.get('phone')
        _items = request.form.get('item')
        _weight = request.form.get('weight')
        file = request.files['file']
        file_name = file.filename
        uploaded_file_content = encodestring(file.read())
        _lat = request.form.get('lat')
        _lon = request.form.get('lon')

        name = _name
        email = _email
        items = _items


        jsonDocument = {
            "nameField": _name,
            "emailField": _email,
            "phoneField": _phoneme,
            "itemsField": _items,
            "weightField": _weight,
            "lonField": _lon,
            "latField": _lat,
            "fileField": uploaded_file_content
        }

        #image_encode = uploaded_file_content
        #image_64_decode = base64.decodestring(image_encode)
        #image_result = open('deer_decode.jpg','wb')  # create a writable image and write the decoding result
        #image_result.write(image_64_decode)

        if name and email and items and _phoneme and _weight and _lat and _lon:
            newDocument = myDatabase.create_document(jsonDocument)

            if newDocument.exists():
                flash("Successfully Donated")
                print("Document '{0}' successfully created.".format(_name))
                return redirect(url_for('thanks'))

        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    else:
        return render_template('signup copy.html')


@app.route("/thanks")
def thanks():
    return render_template('donated.html')

@app.route('/showdownload', methods=['GET', 'POST'])
def showdownload():
    if request.method == 'POST':
        _name = request.form.get('database')
        return redirect(url_for('showDatabase'))

    else:
        return render_template('download.html')


@app.route('/showDatabase')
def showDatabase():
    databaseName = "volunteer"

    end_point = '{0}/{1}'.format(serviceURL, databaseName + "/_all_docs")
    params = {'include_docs': 'true'}

    response = client.r_session.get(end_point, params=params)

    query = cloudant.query.Query(myDatabase, selector={'_id': {'$gt': 0}}, fields=['latField', 'lonField', 'weightField', 'itemsField'])

    dicto = {'lat': [], 'lon': [], 'weight':[], 'items': []}

    for doc in query(limit=100)['docs']:
        #print doc
        dicto['lat'].append(doc['latField'].encode("ascii","replace"))
        dicto['lon'].append(doc['lonField'].encode("ascii","replace"))
        dicto['weight'].append(doc['weightField'].encode("ascii","replace"))
        dicto['items'].append(doc['itemsField'].encode("ascii","replace"))


    #return json.dumps("{0}\n".format(doc))
    return render_template('thankyou.html', dicto = dicto)



if __name__ == "__main__":
    app.secret_key = 'SuperFly'
    app.run()
