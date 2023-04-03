from flask import render_template, flash, jsonify, Response
from flask import redirect, url_for, make_response, session, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from flask_bcrypt import check_password_hash
from app.forms.form import RegisterForm, LoginForm, PasswordResetRequestForm, ResetPasswordForm, ChangePasswordForm
from app import bcrypt
from app.utils.email import send_reset_password_mail
from app.models.model import User
from app.utils.verificationCode import get_verify_code
from io import BytesIO
from PIL import Image
from app.utils.yolo import YOLO
from app.models.model import VideoCamera, CameraResult
from datetime import datetime
import numpy as np
import cv2
import os


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/code')
def get_code():
    image, code = get_verify_code()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = code
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(username=username).first()
        if session.get('image').lower() != form.verify_code.data.lower():
            flash('验证码错误')
            return render_template('user/login.html', form=form)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember)
            flash('登陆成功！', category='info')
            return render_template('index.html')
        flash("用户不存在或密码不匹配", category='danger')
    return render_template('user/login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('login'))


@app.route('/send_password_reset_request', methods=['GET', 'POST'])
def send_password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        token = user.generate_reset_password_token()
        send_reset_password_mail(user, token)
        flash('密码重置请求邮件已发送，请检查您的邮件', category='info')
    return render_template('user/send_password_reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.check_reset_password_token(token)
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash('密码重置成功', category='info')
            return redirect(url_for('login'))
        else:
            flash("此用户不存在", category='info')
            return redirect(url_for('login'))
    return render_template('user/reset_password.html', form=form)


@app.route('/change_password/<username>', methods=['GET', 'POST'])
def change_password(username):
    user = User.query.filter_by(username=username).first()
    form = ChangePasswordForm()
    if user.is_authenticated:
        if form.validate_on_submit():
            if not check_password_hash(user.password, form.old_password.data):
                flash("旧密码错误！", category='info')
                return render_template('index.html', current_user=user)
            user.password = bcrypt.generate_password_hash(form.password.data)
            db.session.commit()
            flash("密码修改成功！", category='info')
            return render_template('index.html', current_user=user)
    return render_template('main/change_password.html', form=form, current_user=user)


@app.route('/personal_information/<username>', methods=['GET', 'POST'])
def personal_information(username):
    user = User.query.filter_by(username=username).first()
    return render_template('main/personal_information.html', current_user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('login'))
    return render_template('user/register.html', form=form)


@app.route('/image_detection_action', methods=['POST'])
def image_detection_action():
    filename = ''
    if request.method == 'POST':
        yolo = YOLO()
        f = request.files['file']
        filename = f.filename
        filepath_in = 'app/static/temporary/in.' + filename.split(".")[1]
        filepath_out = 'app/static/temporary/out.' + filename.split(".")[1]
        f.save(filepath_in)
        try:
            image = Image.open(filepath_in)
        except:
            flash('文件打开失败，请重新尝试！')
        else:
            image_result = yolo.detect_image(image)
            image_result.save(filepath_out)
        yolo.close_session()
    return jsonify({"filepath_result": '/static/temporary/out.'+filename.split(".")[1]})


@app.route('/video_detection_action', methods=['POST'])
def video_detection_action():
    if request.method == 'POST':
        yolo = YOLO()
        video = request.files['file']
        filename = video.filename
        filepath_in = 'app/static/temporary/in.' + filename.split(".")[1]
        filepath_out = 'app/static/temporary/out.mp4'
        video.save(filepath_in)
        capture = cv2.VideoCapture(filepath_in)
        fourcc = cv2.VideoWriter_fourcc(*'X264')  # 确定解码器
        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(filepath_out, fourcc, fps, (frame_width, frame_height))
        # 参数依次为：文件；视频解码器选择；之后的两个参数：每秒帧数（浮点数）以及帧大小(框架大小——即视频窗体大小)
        ret, frame = capture.read()
        while ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 转变成Image
            frame = Image.fromarray(np.uint8(frame))
            # 进行检测
            frame = np.array(yolo.detect_image(frame))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)
            ret, frame = capture.read()
        capture.release()  # 释放视频捕获
        out.release()  # 释放存储对象
        yolo.close_session()
    return jsonify({"video_result": '/static/temporary/out.mp4'})


def gen(camera):
    fourcc = cv2.VideoWriter_fourcc(*"X264")  # 确定解码器
    #fps = camera.video.get(cv2.CAP_PROP_FPS)
    frame_width = int(camera.video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(camera.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    filepath_out = 'app/static/temporary/camera_out.mp4'
    out = cv2.VideoWriter(filepath_out, fourcc, 8, (frame_width, frame_height))
    # 参数依次为：文件；视频解码器选择；之后的两个参数：每秒帧数（浮点数）以及帧大小(框架大小——即视频窗体大小)
    while True:
        frame, img = camera.get_frame()
        out.write(img)
        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/camera_detection_end', methods=['GET', 'POST'])
def camera_detection_end():
    path = 'app/static/temporary/camera_out.mp4'
    cap = cv2.VideoCapture(path)
    if cap.isOpened():
        filepath_out = os.getcwd() + '/' + path
        camera_result = CameraResult(camera_path=filepath_out, data_time=datetime.now())
        db.session.add(camera_result)
        db.session.commit()
    else:
        return jsonify({"save_result": 'error'})
    os.remove(path)
    return jsonify({"save_result": 'success'})


@app.route('/camera_detection_action', methods=['GET', 'POST'])
def camera_detection_action():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('company/home.html')


@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('main/homepage.html')


@app.route('/image_detection', methods=['GET', 'POST'])
def image_detection():
    return render_template('main/image_detection.html')


@app.route('/video_detection', methods=['GET', 'POST'])
def video_detection():
    return render_template('main/video_detection.html')


@app.route('/camera_detection', methods=['GET', 'POST'])
def camera_detection():
    return render_template('main/camera_detection.html')


@app.route('/help', methods=['GET', 'POST'])
def help():
    return render_template('main/help.html')


@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('main/test.html')


@app.route('/caseshow')
def caseshow():
    return render_template('company/caseshow.html')


@app.route('/product')
def product():
    return render_template('company/product.html')


@app.route('/service')
def service():
    return render_template('company/service.html')


@app.route('/about')
def about():
    return render_template('company/about.html')


@app.errorhandler(403)
def error_403(e):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def error_404(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def error_500(e):
    return render_template('errors/500.html'), 500
