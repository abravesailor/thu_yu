from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.urls import path

from backend import views

urlpatterns = [

    # person-related urls
    url(r'register_ajax$', views.register_ajax, ),
    url(r'login_ajax$', views.login_ajax, ),
    # url(r'logout_ajax$', views.logout_ajax, ),
    url(r'person_info_ajax$', views.person_info_ajax, ),
    url(r'modify_ajax$', views.modify_ajax, ),
    url(r'modify_password_ajax$', views.modify_password_ajax, ),
    url(r'class_list_ajax$', views.classlist_ajax, ),
    url(r'msglist_ajax$', views.msglist_ajax, ),
    url(r'fileslist_ajax$', views.filelist_ajax, ),
    url(r'group_add_ajax$', views.group_add, ),
    url(r'group_dismiss_ajax$', views.group_dismiss, ),
    url(r'group_display_ajax$', views.group_display, ),
    url(r'groups_in_lessons_ajax$', views.groups_in_lessons, ),
    url(r'assignment_distribute_ajax$', views.assignment_distribute, ),
    url(r'assignment_display_for_user_ajax$', views.assignment_display_for_user, ),
    url(r'assignment_check_for_teacher_ajax$', views.assignment_check_for_teacher, ),
    url(r'assignment_check_ajax$', views.assignment_check, ),
    url(r'assignment_upload_ajax$', views.assignment_upload, ),
    url(r'assignment_remove_ajax$', views.assignment_remove, ),
    url(r'chat_save_ajax$', views.chat_save, ),
    url(r'chat_record_ajax$', views.chat_record, ),

    # team-related urls
    # url(r'get_team_name_list_ajax$', views.get_team_name_list_ajax),
    # url(r'register_team_ajax$', views.register_team_ajax),

]
urlpatterns += staticfiles_urlpatterns()
