# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template, flash, redirect, request

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from jieba_process import search_by_words
from jieba_process import __init__ as jieba_init

app = Flask(__name__)
app.config.from_object('config')


class SearchForm(Form):
    keyword = StringField('keyword',
                          render_kw={'placeholder':u'搜索宁大新闻'},
                          validators=[DataRequired(message=u'请输入关键词')])


@app.route('/hello/<keyword>')
def hello_world(keyword=None):
    return render_template('hello.html', name=keyword)


@app.route('/')
@app.route('/index')
def search_index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect('/search')

    return render_template('index.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    keywords = request.args.get('keyword')
    print(keywords)
    results, text_titles, keywords = search_by_words(keywords=keywords)
    return render_template('result.html',
                           results=results,
                           titles=text_titles,
                           keywords=keywords)


if __name__ == '__main__':
    jieba_init()
    app.run()
