import json
import flask
# Made by ghalbeyou
app = flask.Flask(__name__)
app.secret_key = 'Generate_A_Secret_Key_Here'
pastes = []
with open('pastes.json', 'r') as f:
    pastes = json.load(f)
# routes
@app.route('/')
def index():
    print("[*] / was used")
    return flask.render_template('index.html', paster=len(pastes))
@app.route('/about')
def about():
    print("[*] /about was used")
    return flask.render_template('about.html')
@app.route('/contact')
def contact():
    print("[*] /contact was used")
    return flask.render_template('contact.html')
@app.route('/write')
def write():
    print("[*] /write was used")

    return flask.render_template('write.html')
@app.route('/write', methods=['POST'])
def write_post():
    post_title = flask.request.form['title']
    post_body = flask.request.form['body']
    if post_title == '' or post_body == '':
        return "<p>Empty values!</p>"
    illegial = [
        '<',
        '>'
    ]    
    for i in illegial:
        if i in post_title:
            return "Illegial Characters in Title"
        if i in post_body:
            return "Illegial Characters in Body"
    if post_title in pastes:
        post_title = f"{post_title}-{len(pastes)}"
    if post_body in pastes:
        return  "<p>Your paste is already in the database!</p>"
    pastes.append({
        'title': post_title,
        'body': post_body
    })
    with open('pastes.json', 'w') as f:
        json.dump(pastes, f)
    return f"<p>Your paste has been submitted.<br/>ID for paste: {len(pastes)-1}<br/>URL: site-address.com/{len(pastes)-1}</p>"
@app.route('/<int:id>')
def read(id):
    # check if id is in pastes
    if id in range(len(pastes)):
        return flask.render_template('read.html', past_title=pastes[id]['title'], past_body=pastes[id]['body'])
    else:
        return notfound("Paste not found")
@app.route('/paste/<int:id>')
def read_paste(id):
    return read(id)
@app.route('/new')
def new():
    return flask.redirect('/write')

# Error handler
@app.errorhandler(404)
def notfound(error):
    return flask.render_template('error/404.html', error=error)
@app.errorhandler(500)
def forbidden(error):
    return flask.render_template('error/500.html', error=error)
app.run(debug=True)
