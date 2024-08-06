# 基于YOLOv4的安全帽检测系统（tensorflow）

## 1、简介

​本系统基于YOLOv4目标检测算法，采用开源的安全帽检测数据集和预训练权重不断进行迭代训练。最后，采用轻量型的Flask Web开发框架，将训练好的模型部署到Web服务中。

![1](https://github.com/user-attachments/assets/1c9f66d8-3f05-4db7-a32e-7b426f790da2)

## 2、功能模块

该安全帽检测系统主要提供以下功能：

（1）账号注册：新用户可以注册账号用于登陆系统。

（2）登录系统：用户可以通过账号密码登录系统，可以查看个人的信息。

（3）找回密码：如果用户忘记自己的登录密码，则可以使用注册时填写的邮箱找回密码。

（4）修改密码：已经登陆的用户可以使用修改密码功能修改自己的登录密码。

（5）个人信息：已经登录系统的用户可以查看个人相关信息。

（6）图片检测：用户可以在界面选择图片检测功能，然后选择本地图片进行检测并将检测结果反馈给用户。

（7）视频检测：用户可以在界面选择视频检测功能，然后选择本地视频进行检测并将检测结果反馈给用户。

（8）摄像头检测：用户可以在界面选择摄像头检测功能，然后系统调用摄像头并进行实时检测以及反馈检测结果给用户。

（9）帮助：系统帮助文档旨在于解决用户在系统使用过程中遇到的问题。

![4](https://github.com/user-attachments/assets/257dc954-2ea4-4db8-bdc5-40e78c881de1)


## 3、环境

tensorflow

flask

flask-bootstrap

flask-sqlalchemy

flask-mysqldb

flask-bcrypt

flask-login

Flask-WTF

flask-mail

PyJWT

PIL

scipy

numpy

opencv-python

wtforms

注意版本之间的依赖问题。

## 4、系统架构

​对于本系统，其核心的功能是安全帽检测。当用户使用安全帽检测功能时，前端用户的请求会发送给Web服务器，服务器通过路由进行响应，而路由会调用检测模型对用户的待检测文件进行检测。最终，路由会将检测结果信息返回给前端用户，包括置信度和类别等信息。该系统将采用基于Python的Flask Web开发，关于系统的整体架构见下图所示。

![2](https://github.com/user-attachments/assets/f1e01623-03ca-4cbd-b2ff-e419b6bbab06)

![3](https://github.com/user-attachments/assets/dfcbf911-0c7e-439a-9007-83f72e741f1e)


​用户只有登录(login)系统，才能进入用户首页(index)，没有账号的用户可以选择注册账号(register)，忘记密码的用户可以选择找回密码(send_password_reset_request)。用户进入首页以后可以使用系统提供的相关功能，即用户可以选择图片检测(image_detection)、视频检测(video_detection)、摄像头检测(camera_detection)、个人信息(personal_information)、修改密码(change_password)和查看帮助(help)等功能。对于图片检测和视频检测用户需要上传本地文件，然后点击确定按钮(image_detection_action/video_detection_action)进行检测，对于摄像头检测用户只需点击开启按钮(camera_detection_action)即可实时检测视频流，对于检测结果都将返回到前端展示给用户，进入用户首页的用户可以使用退出(logout)功能退出系统。对于上面的操作都有可能触发error，即没有访问权限(error_403)、网页未找到(error_404)和服务器错误(error_500)。面向用户的Web后端Flask路由构成见下图所示。

![6](https://github.com/user-attachments/assets/26c031e0-d30c-4fcb-be83-2ce828dd9806)


## 5、数据集

​在这次模型的训练过程中，主要用到了SHWD(Safety helmet (hardhat) wearing detect dataset)数据集，采用PASCAL VOC数据集格式。它是一个开源的安全帽检测数据集，提供用于安全头盔佩戴和人头检测的数据集。它包括7581张图像，其中9044人安全头盔佩戴对象（正类）和111514个正常头部物体（负类），其中一些负类的图像是从SCUT-HEAD头部检测数据集得到，用于判断未佩戴安全帽的人，这些图片收集来自谷歌和百度，使用LabelImg手动标记了部分对象。可以替换为自己的数据集，转成YOLO格式即可。

![5](https://github.com/user-attachments/assets/81a7c8f1-b87c-47f7-a49c-b853b18d1b6d)


## 6、例图

![image](https://github.com/user-attachments/assets/c5ef602a-3048-4020-8f1d-46b2d4c7c797)


![image](https://github.com/user-attachments/assets/a8e18800-108c-461e-85c0-c22b41544439)


![image](https://github.com/user-attachments/assets/164d377d-60db-48bc-b1fb-91d67a2423bc)


![image](https://github.com/user-attachments/assets/abd84e39-b2fb-40a4-93f1-ce5db72211b3)


![7](https://github.com/user-attachments/assets/c837655d-f1e7-45e3-96b5-fed285649102)


![8](https://github.com/user-attachments/assets/ae087f99-125e-444d-b4cc-4f75f52dff9a)


![9](https://github.com/user-attachments/assets/27507563-b951-4316-bea5-a54cba53b87d)



