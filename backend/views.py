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
import datetime

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
        #user_profile.pri = []
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
                response['permission'] = user_profile.permission
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
        username = json.loads(request.body.decode('utf-8'))['username']
        user_profile = UserProfile.objects.get(username=username)
        print(user_profile)
        response['username']=username
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
        username = json.loads(request.body.decode('utf-8'))['username']
        user_profile = UserProfile.objects.get(username=username)

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
        username = json.loads(request.body.decode('utf-8'))['username']
        user_profile = UserProfile.objects.get(username=username)

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
        username = json.loads(request.body.decode('utf-8'))['username']
        user_profile = UserProfile.objects.get(username=username)
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
#TODO: 要修改  要检查!!
def msglist_ajax(request):
    print("msglist_ajax")
    response = {}
    try:
        class_id = json.loads(request.body.decode('utf-8'))['classid']
        lesson=Lessons.objects.get(id=class_id)
        messages=list(Notice.objects.filter(lessons=lesson))
        msg_list=[]
        for msg in messages:
            tmp_dict={}
            tmp_dict['msg_title']=msg.notice_title
            datetime.datetime.strptime(msg.create_time, "%Y-%m-%d %H:%M")
            tmp_dict['create_time']=datetime.datetime.strptime(msg.create_time, "%Y-%m-%d %H:%M")
            tmp_dict['context']=msg.context
            #tmp_dict['msgid']=msg.msgid
            tmp_dict['teachers'] = msg.teachers
            msg_list.append(tmp_dict)
        response['tableData'] = msg_list
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'

    return JsonResponse(response)
#TODO: 接收公告  要检查!!
def add_notice(request):
    response = {}
    try:
        class_id = json.loads(request.body.decode('utf-8'))['classid']
        notice_title = json.loads(request.body.decode('utf-8'))['msg_title']
        context = json.loads(request.body.decode('utf-8'))['context']
        lesson = Lessons.objects.get(id=class_id)
        notice=Notice(notice_title=notice_title,context=context,lessons=lesson)
        notice.save()
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
        class_id = json.loads(request.body.decode('utf-8'))['classid']
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
    print("group_add")
    response = {}
    try:
        user_list=json.loads(request.body.decode('utf-8'))['userlist']
        print(user_list)
        group_id=json.loads(request.body.decode('utf-8'))['group_id']
        lessons_id=json.loads(request.body.decode('utf-8'))['classid']
        lessons=Lessons.objects.get(id=lessons_id)
        new_group=Group(group_id=group_id,lessons=lessons)
        for username2 in user_list:
            username = str(username2)
            print(username+'aaa')
            student=UserProfile.objects.get(username=str(username))
            print("***")
            print(student)
            print(type(student))
            print("***")
            #print(username)
            print("&&&")
            new_group.users.add(student)
            print("&&&")
            #print(username)
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
        group_id = json.loads(request.body.decode('utf-8'))['group_id']
        Group.objects.filter(id=group_id).delete()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)

#返回分组的所有成员
#TODO: username realname
def group_display(request):
    response = {}
    try:
        groupId = json.loads(request.body.decode('utf-8'))['groupid']
        studentList=list(Group.objects.get(id=groupId).users.all())
        result = []
        if len(studentList)!=0:
            for s in studentList:
                user_dict={}
                user_dict['username']=s.username
                user_dict['realname']=s.real_name
                user_dict['group_id']=groupId
                result.append(user_dict)
            response['tableData'] = result
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)
#TODO:
def groups_in_lessons(request):
    response = {}
    try:
        class_id = json.loads(request.body.decode('utf-8'))['classid']
        print(class_id)
        lessons=Lessons.objects.get(id=class_id)
        students=list(lessons.students.all())
        student_info_list=[]
        for s in students:
            st_dict={}
            st_dict['username']=s.username
            st_dict['realname']=s.real_name
            group_list=Group.objects.filter(users=s,lessons=lessons)
            if len(group_list)==0:
                group_id=0
            else:
                group_id=group_list[0].group_id

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
        distributor=json.loads(request.body.decode('utf-8'))['username']
        class_id=json.loads(request.body.decode('utf-8'))['classid']
        title=json.loads(request.body.decode('utf-8'))['title']
        ddl=json.loads(request.body.decode('utf-8'))['ddl']
        context=json.loads(request.body.decode('utf-8'))['context']
        checking_list_raw=json.loads(request.body.decode('utf-8'))['list']
        checking_permission=json.loads(request.body.decode('utf-8'))['permission'] #yes or no
        checking_list = []
        lesson=Lessons.objects.get(class_id=class_id)
        users_list=list(lesson.students.all())
        user_status={}
        for user in users_list:
            user_status[user.username]=-1
        user_status=json.dumps(user_status)
        if checking_permission =="no":
            for item in json.loads(checking_list_raw):
                start=datetime.datetime.strptime(item['starttime'], "%Y-%m-%d %H:%M")
                end=datetime.datetime.strptime(item['endtime'], "%Y-%m-%d %H:%M")
                cnt=item['cnt']
                timespan=(end-start).total_seconds()/cnt
                tmp_start=start
                for i in range(cnt):
                    new_dict = {}
                    tmp_end=tmp_start+timespan
                    new_dict['starttime']=tmp_start
                    new_dict['endtime'] =tmp_end
                    new_dict['cnt']=1
                    new_dict['curcnt']=0
                    checking_list.append(new_dict)
                    tmp_start=tmp_end
        else:
            for item in checking_list_raw:
                newitem=item
                newitem['curcnt']=0
                checking_list.append(newitem)
        assignment=Assignment(distributor=distributor,lessons_name=lesson.lesson_name,title=title,ddl=ddl,context=context,
                              checking_list=json.dumps(checking_list),checking_permission=checking_permission,user_status=user_status)
        assignment.save()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)

def assignment_display_for_user(request):
    response = {}
    try:
        username=json.loads(request.body.decode('utf-8'))['username']
        class_id=json.loads(request.body.decode('utf-8'))['classid']
        lesson_name=json.loads(request.body.decode('utf-8'))['lessonname']
        lesson=Lessons.objects.get(class_id=class_id)
        assignment_list=list(Assignment.objects.filter(lessons=lesson))
        result=[]
        for item in assignment_list:
            tmp_result={}
            tmp_result['title']=item.title
            tmp_result['ddl']=item.ddl
            tmp_result['hwid']=item.hwid
            tmp_result['distributor']=item.distributor
            tmp_result['modify_time']=item.modify_time.strftime("%Y-%m-%d %H:%M")
            status=json.loads(item.userstatus)
            if status[username]==-1:
                tmp_result['upload_status']=False
            else:
                tmp_result['upload_status'] =True
            result.append(tmp_result)
        response['result']=result
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)


##TODO: ok

#教师查看某一门的某一个作业的提交情况
def  assignment_check_for_teacher(request):
    response = {}
    try:
        username = json.loads(request.body.decode('utf-8'))['username']
        class_id = json.loads(request.body.decode('utf-8'))['classid']
        hwid = json.loads(request.body.decode('utf-8'))['hwid']
        lesson = Lessons.objects.get(class_id=class_id)
        assignment = Assignment.objects.get(hwid=hwid,lessons=lesson)
        userstatus=json.loads(assignment.userstatus)
        result = []
        for username in list(userstatus.keys()):
            user=UserProfile.objects.get(username=username)
            tmp_dict={}
            tmp_dict['username']=username
            tmp_dict['realname']=user.real_name
            tmp_dict['status']=userstatus[username]
            result.append(tmp_dict)
        response['title'] = assignment.title
        response['ddl'] = assignment.ddl
        response['hwid'] = assignment.hwid
        response['distributor'] = assignment.distributor
        response['modify_time'] = assignment.modify_date.strftime("%Y-%m-%d %H:%M")
        response['result'] = result
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)


def assignment_check(request):
    response = {}
    try:
        username = json.loads(request.body.decode('utf-8'))['username']
        class_id= json.loads(request.body.decode('utf-8'))['classid']
        lesson = Lessons.objects.get(class_id=class_id)
        hwid=json.loads(request.body.decode('utf-8'))['hwid']
        assignment=Assignment.objects.get(hwid=hwid)
        cur_time=datetime.datetime.now()
        ddl=datetime.datetime.strptime(assignment.ddl, "%Y-%m-%d")
        if (ddl.day-cur_time.day)<0:
            pass_due='True'
        else:
            pass_due='False'
        response['title'] = assignment.title
        response['ddl'] = assignment.ddl
        response['hwid'] = assignment.hwid
        response['distributor'] = assignment.distributor
        response['modify_time'] = assignment.modify_time.strftime("%Y-%m-%d %H:%M")
        response['userstatus'] = assignment.userstatus
        response['checking_list'] = assignment.checking_list
        response['context'] = assignment.context
        response['pass_due']=pass_due
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)
# pre: 在这个作业的userstatus中 当前user的值为-1
def assignment_upload(request):
    response = {}
    try:
        username = json.loads(request.body.decode('utf-8'))['username']
        lesson_name = json.loads(request.body.decode('utf-8'))['lessonname']
        lesson = Lessons.objects.get(lesson_name=lesson_name)
        hwid = json.loads(request.body.decode('utf-8'))['hwid']
        index=json.loads(request.body.decode('utf-8'))['index']
        assignment = Assignment.objects.get(hwid=hwid)
        checking_list=json.loads(assignment.checking_list)
        checking_dict=checking_list[index]
        limitation=checking_dict['cnt']
        curnum=checking_dict['curcnt']
        cur_time=datetime.datetime.now()
        ddl=datetime.datetime.strptime(assignment.ddl, "%Y-%m-%d %H:%M")

        if(curnum==limitation):
            response['status'] = 'filed'
            response['failed_reason'] = 'upload exceed the limitation'
        else:
            curr_status = json.loads(assignment.userstatus)
            curr_status[username] = index
            checking_list[index]['curcnt']+=1
            assignment.userstatus = curr_status
            assignment.checking_list=checking_list
            assignment.save()
            response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)

def assignment_remove(request):
    response = {}
    try:
        distributor = json.loads(request.body.decode('utf-8'))['username']
        lessons_name = json.loads(request.body.decode('utf-8'))['lessonname']
        title = json.loads(request.body.decode('utf-8'))['title']
        Assignment.objects.filter(distributor=distributor,lessons_name=lessons_name,title=title)[0].delete()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)

def chat_save(request):
    response={}
    try:
        username = json.loads(request.body.decode('utf-8'))['username']
       # lesson_name = json.loads(request.body.decode('utf-8'))['lessonname']
        group_id = json.loads(request.body.decode('utf-8'))['groupid']
        context = json.loads(request.body.decode('utf-8'))['ctx']
        group=Group.objects.get(group_id=group_id)
        user=UserProfile.objects.get(username=username)
        chat=Chat(group=group,user=user,context=context)
        chat.save()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)

def chat_record(request):
    response = {}
    try:
        username = json.loads(request.body.decode('utf-8'))['username']
        lesson_name = json.loads(request.body.decode('utf-8'))['lessonname']
        lesson=Lessons.objects.get(lesson_name=lesson_name)
        user = UserProfile.objects.get(username=username)
        group=Group.objects.get(lessons=lesson,users=user)
        group_id = group.group_id
        chatlist=[]
        for chat in list(Chat.objects.filter(group=group)):
            tmp_dict={}
            tmp_dict['username']=chat.user.username
            tmp_dict['realname'] = chat.user.real_name
            tmp_dict['ctx']=chat.ctx
            tmp_dict['time']=chat.modify_time.strftime("%Y-%m-%d %H:%M")
            chatlist.append(tmp_dict)
        response['group_id']=group_id
        response['chatlist']=chatlist
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)
