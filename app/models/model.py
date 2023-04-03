from app import db, login
from flask import current_app
from flask_login import UserMixin
from app.utils.yolo import YOLO
from PIL import Image
from datetime import datetime
import numpy as np
import jwt
import cv2


@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer)
    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return self.username

    def generate_reset_password_token(self):
        return jwt.encode({'id': self.id}, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def check_reset_password_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.filter_by(id=data['id']).first()
        except:
            return


class CameraResult(db.Model):
    __tablename__ = 'cameras'
    id = db.Column(db.Integer, primary_key=True)
    camera_path = db.Column(db.String(100), unique=True, nullable=False)
    data_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class VideoCamera(object):
    def __init__(self):
        # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(0)
        self.yolo = YOLO()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ref, frame = self.video.read()
        # 格式转变，BGRtoRGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 转变成Image
        frame = Image.fromarray(np.uint8(frame))
        # 进行检测
        frame = np.array(self.yolo.detect_image(frame))
        # RGBtoBGR满足opencv显示格式
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), frame