from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
# from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'helgj343lkjjdfhl0098'

@app.route('/')
def home():
    return render_template('home.html', codes = session.keys())

@app.route('/your-url', methods = ['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        
        if os.path.exists(os.getcwd()+"/urls.json"):
            f = open("urls.json")
            url_data = json.load(f)
            if request.form['code'] in url_data.keys():
                flash('That short name has already been taken. Choose another short name.')
                return redirect(url_for('home'))
            
            else:
                if 'url' in request.form.keys():   
                    url_data[request.form['code']] = {'url': request.form['url']}

                # else:
                #     f = request.files['file']
                #     full_name = request.form['code'] + secure_filename(f.filename)
                #     f.save(os.getcwd() + "/static/user_files/" + full_name)
                #     url_data[request.form['code']] = {'file': full_name}
                    
                with open("urls.json", "w") as f2:
                    json.dump(url_data, f2)
                    session[request.form['code']] = True
        
        else:
            url_data = {}
            if 'url' in request.form.keys(): 
                url_data[request.form['code']] = {'url': request.form['url']}

            # else:
            #     f = request.files['file']
            #     full_name = request.form['code'] + secure_filename(f.filename)
            #     f.save(os.getcwd() + "/static/user_files/" + full_name)
            #     url_data[request.form['code']] = {'file': full_name}
        
            with open("urls.json", "w") as f2:
                    json.dump(url_data, f2)
                    session[request.form['code']] = True

        return render_template('your_url.html', code = request.form['code'])
    else:
        return redirect(url_for('home'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists(os.getcwd()+"/urls.json"):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename = '/user_files/'+urls[code]['file']))
    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))



if __name__ == '__main__':
    app.run(debug=True, port=8000)

