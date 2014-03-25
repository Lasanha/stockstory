import os
from flask import Flask, request, render_template, redirect
from flask.ext.pymongo import PyMongo
import flask_pymongo
from storyzer import storyze, format_story
from bson.objectid import ObjectId


app = Flask(__name__)
app.debug = True
app.config['MONGO_URI'] = os.environ.get('MONGOLAB_URI')
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # TODO: sanitize lines
        story = storyze(request.form['title'], request.form['text'], request.form['author'])
        story_id = mongo.db.stories.insert(story)
        return redirect('/story/' + str(story_id))
    stories = mongo.db.stories.find().sort("_id", flask_pymongo.DESCENDING)[:15]
    return render_template('home.html', stories=stories)


@app.route('/story/<story_id>')
def story(story_id):
    story = mongo.db.stories.find_one({"_id":ObjectId(story_id)})
    story = format_story(story)
    return render_template('story.html', story=story)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run()
