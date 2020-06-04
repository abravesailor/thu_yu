# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
#import jsonfield

# Create your models here.
class UserProfile(models.Model):
    STATUS=(
        ('Te','Teacher'),
        ('S','Student'),
    )
    username = models.CharField('Username', max_length = 64, unique = True)
    password = models.CharField('Password', max_length = 64)
    email = models.CharField('Email', max_length = 64, blank = True)
    telephone = models.CharField('Telephone', max_length = 64, blank = True)
#there are four kinds if permission : normal, interviewer, teamAdministrator and topAdministrator
    # permission = models.CharField('Permission',max_length = 64,default = 'normal')

    #user_status = models.CharField(max_length=1, choices=STATUS,default='S')


    employeeID = models.CharField('StudentID', max_length = 64, blank = True)
    modify_date = models.DateTimeField('Last modified', auto_now = True)
    major = models.CharField('Major', max_length = 128, blank = True)
    #priority = jsonfield.JSONField()
    sex = models.CharField('Sex', max_length = 128, blank = True)
    real_name = models.CharField('Real name', max_length = 64, blank = True)
    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.username

    def get_permission(self):
        if(self.user_status=='Te'):
            return "Teacher"
        else:
            return "Student"

    # TODO: 需要json化
    def get_group_list(self):
        return ','.join([i.group_name for i in self.group_set.all()])
    def get_lessons_list(self):
        lesson_list=[]
        for lesson in self.lessons_set.all():
            lesson_dict={}
            lesson_dict["classname"]=lesson.lesson_name
            lesson_dict["teacher"]=lesson.teachers
            lesson_dict["time"]=lesson.time_span
            lesson_dict["id"]=lesson.id  #这个id每个数据库中自带的
           # lesson_dict["id"]=hash(lesson.lesson_name)
            lesson_list.append(lesson_dict)
        return lesson_list

class Teacher(models.Model):
    teacher_name=models.CharField('Teachername', max_length=64)
    teacher_id=models.CharField('Teachername', max_length=64)
    class Meta:
        db_table='Teacher'
        ordering=['teacher_name']
    def __str__(self):
        return self.teacher_name


class Lessons(models.Model):
    lesson_name=models.CharField('Lesson Name',max_length=64,unique=True)
    class_id=models.CharField('Lesson id',max_length=64,default=hash(lesson_name))
    teachers=models.CharField('Teacher Name',max_length=64,unique=True,blank=True)
    time_span=models.CharField('Time Span',max_length=128)
    students=models.ManyToManyField(UserProfile,related_name='Students')
    #students_list=models.CharField('List',max_length=10000000,unique=True,blank=True)  # 直接保存
    class Meta:
        db_table='Lessons'
        ordering = ['lesson_name']
    def __str__(self):
        return self.lesson_name

    def get_user_list(self):
        return ','.join([i.user_name for i in self.students.all()])
    def get_msg_list(self):
        msg_list=[]
        for msg in self.notices.objects.all():
            msg_dict={}
            msg_dict["classname"]=msg.notice_title
            msg_dict["teacher"]=msg.teachers
            msg_dict["time"]=msg.create_time
            msg_dict["id"]=msg.id  #这个id每个数据库中自带的
           # lesson_dict["id"]=hash(lesson.lesson_name)
            msg_list.append(msg_dict)
        return msg_list
    def get_file_list(self):
        file_list=[]
        for file in self.files.objects.all():
            file_dict={}
            file_dict["classname"]=file.notice_title
            file_dict["teacher"]=file.teachers
            file_dict["time"]=file.create_time
            file_dict["id"]=file.id  #这个id每个数据库中自带的
           # file_dict["id"]=hash(lesson.lesson_name)
            file_list.append(file_dict)
        return file_list

class Notice(models.Model):
    notice_title=models.CharField('Notice Title',max_length=64)
    teachers=models.CharField('Instructor',max_length=64)
    create_time = models.DateTimeField('Sent time',auto_now=True)
    msgid=models.CharField('Lesson Id',max_length=64,default=hash(notice_title))
    lessons = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    class Meta:
        db_table='Notice'
        ordering = ['notice_title']
    def __str__(self):
        return self.notice_title


class Assignment(models.Model):
    distributor=models.CharField("Distributor",max_length=64,blank=True)
    title=models.CharField("Assignment Title",max_length=128,default="No title",blank=True)
    lessons=models.ForeignKey(Lessons,on_delete=models.CASCADE)
    ddl=models.CharField("DeadLine",max_length=64,blank=True)
    context=models.CharField("Context",max_length=1000000,blank=True)
    checking_permission=models.CharField("Permission",max_length=20,blank=False)
    checking_list=models.CharField("Check List",max_length=100000,blank=True)  #一个检查list,每个元素是一个字典,key为时间段,value 为最大检查数量
    userstatus=models.CharField("User Status",max_length=1000000,blank=True)
    #includedFiles
    class Meta:
        db_table='Assignment'
        ordering = ['title']
    def __str__(self):
        return self.title


class Files(models.Model):
    file_name=models.CharField('File Name', max_length=64)
    size=models.CharField('Size',max_length=64)
    create_time = models.DateTimeField('Sent time', auto_now=True)
    field=models.CharField('Field',max_length=64)
    lessons = models.ForeignKey(Lessons, on_delete=models.CASCADE,blank=True)
    assignments = models.ForeignKey(Assignment, on_delete=models.CASCADE, blank=True)
    class Meta:
        db_table='Files'
        ordering = ['file_name']
    def __str__(self):
        return self.file_name

class Group(models.Model):
    group_id=models.CharField('Group Id',max_length=64,default="1")
    users=models.ManyToManyField(UserProfile,related_name='Groups')
    lessons = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    class Meta:
        db_table='Group'
        ordering = ['group_id']
    def __str__(self):
        return self.group_id
    # TODO: 需要json化
    def get_user_list(self):
        return ','.join([i.user_name for i in self.user.all()])

