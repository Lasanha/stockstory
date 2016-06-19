import os
from flask import Flask, request, render_template, redirect, url_for, g
from flask_pymongo import PyMongo
import flask_pymongo
from flask_babel import Babel
from storyzer import storyze, format_story
from bson.objectid import ObjectId


app = Flask(__name__)
app.debug = True
babel = Babel(app)
app.config['MONGO_URI'] = os.environ.get('MONGOLAB_URI')
app.config['GSE_API_KEY'] = os.environ.get('GSE_API_KEY')
app.config['GSE_CX_ID'] = os.environ.get('GSE_CX_ID')
mongo = PyMongo(app)


@app.before_request
def before():
    if request.view_args and 'lang_code' in request.view_args:
        g.current_lang = request.view_args['lang_code']
        request.view_args.pop('lang_code')


@babel.localeselector
def get_locale():
    return g.get('current_lang', 'en')


@app.route('/')
def root():
    return redirect(url_for('home', lang_code='pt_br'))


@app.route('/<lang_code>', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # TODO: sanitize lines
        st = storyze(request.form['title'], request.form['text'], request.form['author'])
        story_id = mongo.db.stories.insert(st)
        return redirect(get_locale() + '/story/' + str(story_id))
    stories = mongo.db.stories.find().sort("_id", flask_pymongo.DESCENDING)[:15]
    return render_template('home.html', stories=stories)


@app.route('/<lang_code>/story/<story_id>')
def story(story_id):
    st = mongo.db.stories.find_one({"_id": ObjectId(story_id)})
    st = format_story(st)
    return render_template('story.html', story=st)


@app.route('/<lang_code>/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run()
