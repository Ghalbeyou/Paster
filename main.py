import json
import flask

app = flask.Flask(__name__)
app.secret_key = 'Generate_A_Secret_Key_Here'
pastes = []
with open('pastes.json', 'r') as f:
    pastes = json.load(f)
# routes
@app.route('/')
def index():
    return flask.render_template('index.html', paster=len(pastes))
@app.route('/about')
def about():
    return flask.render_template('about.html')
@app.route('/contact')
def contact():
    return flask.render_template('contact.html')
@app.route('/write')
def write():
    return flask.render_template('write.html')
@app.route('/write', methods=['POST'])
def write_post():
    post_title = flask.request.form['title']
    post_body = flask.request.form['body']
    illegial = [
        '<',
        '>'
    ]    
    for i in illegial:
        if i in post_title:
            return "Illegial Characters in Title"
        if i in post_body:
            return "Illegial Characters in Body"

        # return "<p>Your paste has been rejected because it contains illegal characters.</p>"
    pastes.append({
        'title': post_title,
        'body': post_body
    })
    with open('pastes.json', 'w') as f:
        json.dump(pastes, f)
    return f"<p>Your paste has been submitted.<br/>ID for paste: {len(pastes)}<br/>URL: site-address.com/{len(pastes)}</p>"
@app.route('/<int:id>')
def read(id):
    # check if id is in pastes
    if id in range(len(pastes)):
        return flask.render_template('read.html', past_title=pastes[id]['title'], past_body=pastes[id]['body'])
    else:
        return "<p>Paste not found.</p>"

app.run(debug=True)