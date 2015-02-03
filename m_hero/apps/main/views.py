from flask import render_template, request
from apps.main import app, models, controllers
import json, math

@app.route('/')
def index():
    return render_template("main/index.html")

@app.route('/page')
def page():
    page = int(request.args.get('page'))
    diff = int(request.args.get('difference'))
    limit = 20
    phrases = models.Phrases.query.order_by(-models.Phrases.id).all()
    pages = math.ceil(len(phrases)/float(limit))
    count = len(phrases)
    phrases = phrases[page*limit+diff:(page+1)*limit+diff]
    return json.dumps({'phrases':phrases, 'pages':pages, 'count':count}, cls=controllers.AlchemyEncoder)

@app.route('/update')
def update():
    last_count = int(request.args.get('count'))
    phrases = models.Phrases.query.order_by(-models.Phrases.id).all()
    count = len(phrases)
    if count > last_count:
        phrases = phrases[:count-last_count]
        return json.dumps({'phrases':phrases, 'count':count}, cls=controllers.AlchemyEncoder)
    else:
        return json.dumps({'count':count})
