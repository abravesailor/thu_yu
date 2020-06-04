# -*—coding:utf8-*-
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
import json
import time
import os
import sys
import qrcode
# import PIL
import random
import traceback

from backend.models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    return render(requset, 'index.html')


def admin_send_ajax(request):
    print("admin send ajax")
    response = {}
    try:
        user_list = UserProfile.objects.filter(admissions = 'Yes')
        print(UserProfile.objects.filter(admissions = 'Yes'))
        print(UserProfile.objects.filter())
        for user in user_list:
            print(user)
            admission_info_pushing(user)
    except Exception as e:
        response['status'] = 'failed'
    return JsonResponse(response)





def register_ajax(request):
    print("register ajax")
    response = {}
    try:
        username = json.loads(request.body.decode('utf-8'))['register_name']
        email = json.loads(request.body.decode('utf-8'))['register_email']
        password = json.loads(request.body.decode('utf-8'))['register_password']
        major = json.loads(request.body.decode('utf-8'))['register_major']
        telephone = json.loads(request.body.decode('utf-8'))['register_phonenumber']
        employeeID = json.loads(request.body.decode('utf-8'))['register_StudentID']  #需要改成  employeeID
        real_name = json.loads(request.body.decode('utf-8'))['register_realname']
        sex = json.loads(request.body.decode('utf-8'))['register_sex']
        print(sex)
        #user_status=json.loads(request.body.decode('utf-8'))['user_status']
        user_status='S'
        print(user_status)
        user_profile = UserProfile(username=username, password=password, email=email, telephone=telephone,
                                   employeeID=employeeID, major=major, real_name=real_name, sex=sex)
        #user_profile.pri = json.dumps([])
        print(username)
        print(password)
        print("reg*************")
        print("aaa")
        user_profile.save()
        print("saved")

        response['status'] = 'success'
    except Exception as e:
        print(e);
        response['status'] = 'failed'
    return JsonResponse(response)

# 这部分逻辑我修改了一下, 可能还需要根据权限做进一步修改
def login_ajax(request):
    print("login ajax")
    response = {}
    try:
        username = json.loads(request.body.decode('utf-8'))['login_name']
        password = json.loads(request.body.decode('utf-8'))['login_password']
        #判断用户是否存在
        print(username)
        print(password)
        #print(len(tmp))
        print("***")
        if(UserProfile.objects.filter(username=username)):
            user_profile = UserProfile.objects.get(username = username)
            #print('permission||||' + user_profile.permission)
            #判断密码是否正确
            if (user_profile.password == password):
                request.session['login_id'] = user_profile.id
                response['permission'] = 'S'
                response['status'] = 'success'
                response['username'] = username
            else:
                response['status'] = 'failed'
                response['failed_reason'] = 'failed due to password failed'
        else:
            response['status'] = 'failed'
            response['failed_reason'] ='failed due to no user'
    except Exception as e:
        print(e)
        print("login exception")
        # traceback.print_exc()
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    print('--------')
    print(response)
    return JsonResponse(response)


def person_info_ajax(request):
    print("personal information")
    response = {}
    try:
        print(request.body)
        user_profile_id = request.session['login_id']
        user_profile = UserProfile.objects.get(id = user_profile_id)
        print(user_profile)
        response['username'] = user_profile.username
        response['password'] = user_profile.password
        response['email'] = user_profile.email
        response['telephone'] = user_profile.telephone
        response['modify_date'] = user_profile.modify_date
        response['major'] = user_profile.major
        response['realname'] = user_profile.real_name
        response['sex'] = user_profile.sex
        print(response)

        response['status'] = 'success'
        print("personal information returned")
    except Exception as e:
        response['status'] = 'failed'
    return JsonResponse(response)


def modify_ajax(request):
    print("modify information")
    response = {}
    try:

        print(request.body)
        user_profile_id = request.session['login_id']
        user_profile = UserProfile.objects.get(id = user_profile_id)

        print(user_profile)

        #username = json.loads(request.body.decode('utf-8'))['modify_name']
        email = json.loads(request.body.decode('utf-8'))['modify_email']
        major = json.loads(request.body.decode('utf-8'))['modify_major']
        telephone = json.loads(request.body.decode('utf-8'))['modify_phonenumber']


        if (email != ''):
            user_profile.email = email
        if (major != ''):
            user_profile.major = major
        if (telephone != ''):
            user_profile.telephone = telephone

        user_profile.save()
        response['status'] = 'success'
    except Exception as e:
        response['status'] = 'failed'
    return JsonResponse(response)


def modify_password_ajax(request):
    print("modify password")

    response = {}
    try:
        print(request.body)
        user_profile_id = request.session['login_id']
        user_profile = UserProfile.objects.get(id = user_profile_id)

        password = json.loads(request.body.decode('utf-8'))['password']
        new_password = json.loads(request.body.decode('utf-8'))['newpassword']
        #password = request.GET.get('password')
        #new_password = request.GET.get('newpassword')

        if (user_profile.password == password):
            print(1)
            user_profile.password = new_password
            print(user_profile.password)
            user_profile.save()
            print(3)
            response['status'] = 'success'
        else:
            response['status'] = 'failed'
            response['failed_reason'] = 'failed due to password failed'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)

##课程列表 ajax


def classlist_ajax(request):
    print("get classlist password")
    response = {}
    try:
        user_profile_id = request.session['login_id']
        user_profile = UserProfile.objects.get(id = user_profile_id)
        lessons_set=Lessons.objects.filter(students=user_profile)
        lessons_list=[]
        for lesson in list(lessons_set):
            lesson_dict = {}#改成json
            lesson_dict["classname"] = lesson.lesson_name
            lesson_dict["teacher"] = lesson.teachers
            lesson_dict["time"] = lesson.time_span
            lesson_dict["id"] = lesson.id
            lessons_list.append(lesson_dict)
        response['tableData']=lessons_list
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)
##公告列表ajax
def msglist_ajax(request):
    response = {}
    try:
        class_id = request.session['classid']
        lesson=Lessons.objects.get(id=class_id)
        response['tableData'] =lesson.get_msg_list()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'

    return JsonResponse(response)

##文件列表ajax
def filelist_ajax(request):
    response = {}
    try:
        class_id = request.session['classid']
        lesson=Lessons.objects.get(id=class_id)
        response['tableData'] =lesson.get_file_list()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'

    return JsonResponse(response)


##分组这部分我没有完全按照你的那种要求,我感觉你的要求有点奇怪
# 这个函数是添加分组
def group_add(request):
    response = {}
    try:
        user_list=request.session['userlist']
        group_id=request.session['group_id']
        lessons_id=request.session['classid']
        lessons=Lessons.object.get(id=lessons_id)
        new_group=Group(group_id=group_id,lessons=lessons)
        for username in user_list:
            student=UserProfile.objects.filter(username=username)
            new_group.users.add(student)
        new_group.save()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'

    return JsonResponse(response)
#这个函数是解散分组
def group_dismiss(request):
    response = {}
    try:
        group_id = request.session['group_id']
        Group.objects.filter(id=group_id).delete()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)

#返回分组的所有成员
def group_display(request):
    response = {}
    try:
        groupId = request.session['groupid']
        studentList=list(Group.objects.get(id=groupId).users.all())
        response['tableData'] = studentList
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)

def groups_in_lessons(request):
    response = {}
    try:
        lessons_id = request.session['classid']
        lessons=Lessons.object.get(id=lessons_id)
        students=list(lessons.students.all())
        student_info_list=[]
        for s in students:
            st_dict={}
            st_dict['username']=s.username
            st_dict['realname']=s.realname
            group_id=Group.objects.filter(users=s,lessons=lessons)
            st_dict['group_id']=group_id
            student_info_list.append(st_dict)
        response['tableData'] = student_info_list
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)

def assignment_distribute(request):
    response = {}
    try:
        distributor=request.session['username']
        lessons_name=request.session['lessonname']
        title=request.session['title']
        ddl=request.session['ddl']
        context=request.session['context']
        checking_list_raw=request.session['list']
        checking_permission=request.session['permission'] #yes or no
        checking_list = []
        if checking_permission =="no":
            pass  #
        else:

            checking_dict={}
            time_span=checking_list_raw[0]+checking_list_raw[1]
            checking_dict[time_span]=checking_list_raw[-1]
            checking_list.append(checking_dict)
        assignment=Assignment(distributor=distributor,lessons_name=lessons_name,title=title,ddl=ddl,context=context,
                              checking_list=checking_list,checking_permission=checking_permission)
        assignment.save()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)

def assignment_display(request):


def assignment_remove(request):
    response = {}
    try:
        distributor = request.session['username']
        lessons_name = request.session['lessonname']
        title = request.session['title']
        Assignment.objects.filter(distributor=distributor,lessons_name=lessons_name,title=title)[0].delete()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)