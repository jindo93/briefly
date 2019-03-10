#!/usr/bin/env python3

from flask import Blueprint, render_template, request, redirect, url_for, session
from ..models.public import Public
from ..models.user import User

controller = Blueprint('public', __name__, url_prefix='/')


@controller.route('/', methods=['GET', 'POST'])
def public_page():
    if request.method == 'GET':
        logout()
        # TODO get tweets and retweets to display in public page
        public = Public()
        public.initialize()

        return render_template(
            'public_home.html',
            msg='Welcome to BRIEFLY',
            tweets=public.tweets
            # time=public.get_time(public.tweets)
        )
    else:
        # Login
        user = User()
        username = request.form.get('username')
        password = request.form.get('password')
        if user.login(username, password):
            session['username'] = username
            print('session: ', session['username'])
            return redirect('/user-home')
        else:
            return render_template(
                'public_home.html',
                msg='Invalid credentials. Try again man.'
            )


@controller.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User()
        # if not (type(password) == str and type(username) == str):
        #     return redirect('/signup')
        # if not (len(password) > 2 and len(username) > 2):
        #     return redirect('/signup')
        if user.check_username_exists(username):
            return render_template(
                'signup.html',
                msg="Username already exists"
            )
        else:
            user.signup(username, password)
            return redirect('/')


@controller.route('/log-out', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect('/')


@controller.route('/brief', methods=['POST'])
def brief():
    user = User()
    user.initialize(session['username'])
    twt_content = request.form.get('brf_content')
    if user.tweet(twt_content):
        return redirect('/user-home')
    else:
        return render_template(
            'user_home.html',
            msg="Something went wrong with your briefing"
        )


@controller.route('/rebrief', methods=['POST'])
def rebrief():
    user = User()
    user.initialize(session['username'])
    content_type = request.form.get('content_type')
    if content_type == 'brief':
        twt_id = request.form.get('twt_id')
    elif content_type == 'rebrief':
        twt_id = request.form.get('twt_id_re')
    else:
        return redirect('/')
    print("tweet id: ", twt_id)
    try:
        user.retweet(twt_id)
        return redirect('/briefings')
    except:
        return render_template(
            'user_home.html',
            msg='Something went wrong with rebriefing!'
        )


@controller.route('/briefings', methods=['GET', 'POST'])
def briefings():
    if request.method == 'GET':
        public = Public()
        public.initialize()
        return render_template(
            'briefings.html',
            msg="Welcome to BRIEFLY EXPLORER",
            tweets=public.tweets
        )


@controller.route('/user-home', methods=['GET', 'POST'])
def user_home():
    if request.method == 'GET':
        user = User()
        user.initialize(session['username'])

        #print('id: ', user.user_id)
        #print('username: ', user.username)
        #print('tweets: ', user.tweets)
        #print('time: ', user.get_time(user.tweets))
        return render_template(
            'user_home.html',
            username=session['username'],
            tweets=user.tweets
        )
