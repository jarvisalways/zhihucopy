from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import jsonify
from flask import session


from models import User


app = Flask(__name__)
app.secret_key = 'random string'


# 通过 session 来获取当前登录的用户
def current_user():
    # print('session, debug', session.permanent)
    username = session.get('username', '')
    u = User.query.filter_by(username=username).first()
    return u


@app.route('/')
def index():
    view = 'login_view'
    return redirect(url_for(view))


# 显示登录界面的函数  GET
@app.route('/login')
def login_view():
    return render_template('login.html')


# 处理登录请求  POST
@app.route('/login', methods=['POST'])
def login():
    # u = User(request.form)
    form = request.get_json()
    username = form.get('username', '')
    user = User.query.filter_by(username=username).first()
    r = {
        'success': False,
        'message': '登录失败',
    }
    if user is not None and user.validate_auth(form):
        r['success'] = True
        r['next'] = url_for('login_view')
        session.permanent = True
        session['username'] = username
    else:
        r['success'] = False
        r['message'] = '登录失败'
    return jsonify(r)


# 处理注册的请求  POST
@app.route('/register', methods=['POST'])
def register():
    form = request.get_json()
    u = User(form)
    r = {
    }
    status, msgs = u.valid()
    if status:
        u.save()
        r['success'] = True
        # 下面这句可以在关闭浏览器后保持用户登录
        session.permanent = True
        session['username'] = u.username
    else:
        r['success'] = False
        r['message'] = '\n'.join(msgs)
    return jsonify(r)


if __name__ == '__main__':
    config = {
        'debug': True,
    }
    app.run(**config)
