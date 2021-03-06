# -*—coding:utf8-*-
from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse,FileResponse
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
from datetime import datetime
from datetime import *
from backend.models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    return render(requset, 'index.html')


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

        user_status='S'
        print(user_status)
        user_profile = UserProfile(username=username, password=password, email=email, telephone=telephone,
                                   employeeID=employeeID, major=major, real_name=real_name, sex=sex)

        print(username)
        print(password)
        print("reg*************")
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
        username=str(username)
        password = json.loads(request.body.decode('utf-8'))['login_password']
        password=str(password)
        #判断用户是否存在
        print(username)
        print(password)
        #print(len(tmp))
        print("***")
        if(UserProfile.objects.filter(username=username)):
            user_profile = UserProfile.objects.get(username = str(username))
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
        user_profile = UserProfile.objects.get(username=str(username))
        print(user_profile)
        response['username']=username
        response['password'] = user_profile.password
        response['email'] = user_profile.email
        response['telephone'] = user_profile.telephone
        #response['modify_date'] = user_profile.modify_date.astimezone(timezone(timedelta(hours=8)))
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
        user_profile = UserProfile.objects.get(username=str(username))

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
#TODO:
def msglist_ajax(request):
    response = {}
    try:
        class_id = json.loads(request.body.decode('utf-8'))['classid']
        lesson=Lessons.objects.get(id=class_id)
        messages=list(Notice.objects.filter(lessons=lesson).order_by('create_time'))
        msg_list=[]
        for msg in messages:
            tmp_dict={}
            tmp_dict['msg_title']=msg.notice_title
            #tmp_dict['create_time']=msg.create_time.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
            tmp_dict['create_time']=(msg.create_time+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
            tmp_dict['context']=msg.context
            tmp_dict['msgid']=msg.id
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
        username=json.loads(request.body.decode('utf-8'))['username']
        realname=UserProfile.objects.get(username=username).real_name
        lesson = Lessons.objects.get(id=class_id)
        notice=Notice(notice_title=notice_title,context=context,lessons=lesson,teachers=username)
        notice.save()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'

    return JsonResponse(response)


def notice_delete(request):
    response={}
    try:
        notice_id=json.loads(request.body.decode('utf-8'))['msgid']
        notice=Notice.objects.get(id=notice_id)
        notice.delete()
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'

    return JsonResponse(response)


##文件列表ajax
def filelist_ajax(request):
    print("filelist")
    response = {}
    try:
        class_id = json.loads(request.body.decode('utf-8'))['classid']
        lesson=Lessons.objects.get(id=class_id)
        files=list(Files.objects.filter(lessons=lesson).order_by('create_time'))
        file_list=[]
        for file in files:
            tmp_dict={}
            tmp_dict['file_name']=file.file_name
            tmp_dict['create_time']=(file.create_time+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
            tmp_dict['size']=file.size
            tmp_dict['field'] = file.field
            file_list.append(tmp_dict)
        response['tableData'] = file_list
        response['status'] = 'success'


    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'

    return JsonResponse(response)

##分组这部分我没有完全按照你的那种要求,我感觉你的要求有点奇怪
# 这个函数是添加分组
#TODO:自动分配 group_id
def group_add(request):
    print("group_add")
    response = {}
    try:
        user_list=json.loads(request.body.decode('utf-8'))['userlist']
        #group_id=json.loads(request.body.decode('utf-8'))['group_id']
        class_id=json.loads(request.body.decode('utf-8'))['classid']
        lessons=Lessons.objects.get(id=class_id)
        new_group=Group(lessons=lessons)
        new_group.save()
        for username in user_list:
            student=UserProfile.objects.get(username=str(username))
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
    print("group_dismiss")
    response = {}
    try:
        group_id = json.loads(request.body.decode('utf-8'))['group_id']
        group_id=str(group_id)
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
        group_id = json.loads(request.body.decode('utf-8'))['groupid']
        group_id=str(group_id)
        studentList=list(Group.objects.get(id=group_id).users.all())
        result = []
        if len(studentList)!=0:
            for s in studentList:
                user_dict={}
                user_dict['username']=s.username
                user_dict['realname']=s.real_name
                user_dict['group_id']=int(group_id)
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
        lessons=Lessons.objects.get(id=class_id)
        students=list(lessons.students.all())
        student_info_list=[]
        for s in students:
            if s.permission=='False':
                st_dict={}
                st_dict['username']=s.username
                st_dict['realname']=s.real_name
                group_list=Group.objects.filter(users=s,lessons=lessons)
                if len(group_list)==0:
                    group_id=0
                else:
                    group_id=group_list[0].id
                st_dict['group_id']=int(group_id)
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
        print(ddl)
        checking_list = []
        lesson=Lessons.objects.get(id=class_id)
        users_list=list(lesson.students.all())
        user_status={}
        for user in users_list:
            user_status[user.username]=-1
        user_status=json.dumps(user_status)
        print(user_status)
        print(checking_list_raw)
        if checking_permission =="no":
            print("aaa")
            print(checking_list_raw)
            for item in json.loads(checking_list_raw):
                print(item)
                print(item['starttime'])
                print(item['endtime'])
                start=datetime.strptime(item['starttime'], "%Y-%m-%d %H:%M")
                end=datetime.strptime(item['endtime'], "%Y-%m-%d %H:%M")
                print(start, end)
                cnt=item['cnt']
                timespan=(end-start).total_seconds()
                print(timespan)
                timespan = timespan / cnt
                tmp_start=start
                for i in range(cnt):
                    new_dict = {}
                    tmp_end=tmp_start+timedelta(seconds=timespan)
                    new_dict['starttime']=tmp_start.strftime("%Y-%m-%d %H:%M")
                    new_dict['endtime'] =tmp_end.strftime("%Y-%m-%d %H:%M")
                    new_dict['cnt']=1
                    new_dict['curcnt']=0
                    checking_list.append(new_dict)
                    tmp_start=tmp_end
        else:
            for item in json.loads(checking_list_raw):
                newitem=item
                newitem['curcnt']=0
                checking_list.append(newitem)

        print(checking_list)
        assignment=Assignment(distributor=distributor,lessons=lesson,title=title,ddl=ddl,context=context,
                              checking_list=json.dumps(checking_list),checking_permission=checking_permission,userstatus=user_status)
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
        lesson=Lessons.objects.get(id=class_id)
        assignment_list=list(Assignment.objects.filter(lessons=lesson).order_by('modify_date'))
        result=[]
        for item in assignment_list:
            tmp_result={}
            tmp_result['title']=item.title
            tmp_result['ddl']=item.ddl
            tmp_result['hwid']=item.id
            tmp_result['distributor']=item.distributor
            tmp_result['modify_time']=(item.modify_date+timedelta(hours=8))
            status=json.loads(item.userstatus)
            if username in status:
                if status[username]==-1:
                    tmp_result['upload_status']='False'
                else:
                    tmp_result['upload_status'] ='True'
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
        class_id = json.loads(request.body.decode('utf-8'))['classid']
        hwid = json.loads(request.body.decode('utf-8'))['hwid']
        lesson = Lessons.objects.get(id=class_id)
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
        response['modify_time'] = (assignment.modify_date+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
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
        class_id= json.loads(request.body.decode('utf-8'))['classid']
        hwid=json.loads(request.body.decode('utf-8'))['hwid']
        assignment=Assignment.objects.get(id=hwid)
        cur_time=datetime.now()
        ddl=datetime.strptime(assignment.ddl, "%Y-%m-%d")
        if (ddl.day-cur_time.day)<0:
            pass_due='True'
        else:
            pass_due='False'
        response['title'] = assignment.title
        response['ddl'] = assignment.ddl
        response['hwid'] = assignment.hwid
        response['distributor'] = assignment.distributor
        #response['modify_time'] = assignment.modify_time.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
        #response['modify_time'] = (assignment.modify_time+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
        response['userstatus'] = assignment.userstatus
        response['checking_list'] = eval(assignment.checking_list)
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
    print("upload_")
    response = {}
    try:
        username = json.loads(request.body.decode('utf-8'))['username']
        lesson_name = json.loads(request.body.decode('utf-8'))['lessonname']
        lesson = Lessons.objects.get(id=lesson_name)
        hwid = json.loads(request.body.decode('utf-8'))['hwid']
        index=json.loads(request.body.decode('utf-8'))['index']
        assignment = Assignment.objects.get(id=hwid)
        print(index)
        checking_list=json.loads(assignment.checking_list)
        checking_dict=checking_list[index]
        limitation=checking_dict['cnt']
        curnum=checking_dict['curcnt']
        if(curnum==limitation):
            response['status'] = 'filed'
            response['failed_reason'] = 'upload exceed the limitation'
        else:
            curr_status = json.loads(assignment.userstatus)
            tmpindex = curr_status[username]
            if (tmpindex != -1):
                checking_list[tmpindex]['curcnt']-=1
            curr_status[username] = index
            checking_list[index]['curcnt']+=1
            assignment.userstatus = json.dumps(curr_status)
            assignment.checking_list= json.dumps(checking_list)
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
        group_id = json.loads(request.body.decode('utf-8'))['groupid']
        context = json.loads(request.body.decode('utf-8'))['ctx']
        group=Group.objects.get(id=group_id)
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
        lesson=Lessons.objects.get(id=lesson_name)
        user = UserProfile.objects.get(username=username)
        group=Group.objects.get(lessons=lesson,users=user)
        #print(group)
        group_id = group.id
        chatlist=[]
        for chat in list(Chat.objects.filter(group=group).order_by('modify_time')):
            tmp_dict={}
            tmp_dict['userName']=chat.user.username
            tmp_dict['realname'] = chat.user.real_name
            tmp_dict['cont']=chat.context
            if (username == chat.user.username):
                tmp_dict['direction'] = "send"
            else:
                tmp_dict['direction'] = "notify"
            #tmp_dict['time']=chat.modify_time.astimezone(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
            tmp_dict['time']=(chat.modify_time+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
            chatlist.append(tmp_dict)
        response['group_id']=group_id
        print(group_id)
        print(len(chatlist))
        response['chatlist']=chatlist
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)




def download_template(request):
    print("request")
    response = {}
    try:
        filename =request.GET.get('name')
        print(filename)
        path = './fileset/'+ filename
        file = open(path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="'+filename+'"'
        response['status'] = 'success'
        return response
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
        return JsonResponse(response)


def upload(request):


    def formatByte(number):
        for (scale, label) in [(1024 * 1024 * 1024, "GB"), (1024 * 1024, "MB"), (1024, "KB")]:
            if number >= scale:
                return "%.2f %s" % (number * 1.0 / scale, label)
            elif number == 1:
                return "1 字节"
            else:
                byte = "%.2f" % (number or 0)
        return (byte[:-3]) if byte.endswith(".00") else byte + "字节"

    print("upload")
    response={}
    try:
        username = request.POST.get("username")
        field = request.POST.get("field")
        field = "teacher1"
        print(username)
        #这一部分实惠关联到文件的外键,所以你看情况是否需要加
        # class_id=request.POST.get("classid")
        # hwid=request.POST.get("hwid")
        # lesson=Lessons.objects.get(id=class_id)
        # hw=Assignment.objects.get(id=hwid)

        myFile = request.FILES.get("file")
        print(myFile.name)
        #print(os.path.join("fileset", myFile.name))
        path = "./fileset/" + myFile.name
        destination = open(path,'wb+')  
        for chunk in myFile.chunks():  
            destination.write(chunk)
        destination.close()

        
        fileinfo = os.stat(path)
        size=formatByte(fileinfo.st_size)

        file=Files(file_name=myFile.name,size=size,field=field, assignments_id=1, lessons_id=1)
        #file = Files(file_name=path, size=size, field=field,lessons=lesson)


        file.save()
        
        response['status'] = 'success'
    except Exception as e:
        print(repr(e))
        response['status'] = 'failed'
        response['failed_reason'] = 'failed due to exception'
    return JsonResponse(response)
