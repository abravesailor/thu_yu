import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import TopNav from '@/components/final_topNav.vue'
import LeftNav from '@/components/final_leftNav.vue'
import Home from '@/views/home.vue'
import Dashboard from '@/views/workbench/dashboard.vue'
import MySettings from '@/views/workbench/mySettings.vue'
import Mission from '@/views/workbench/mission/mission.vue'
import Plan from '@/views/workbench/plan/plan.vue'
import Maillist from '@/views/workbench/maillist.vue'
import EnterpriseList from '@/views/enterprise/index.vue'
import EnterpriseAdd from '@/views/enterprise/add.vue'
import EnterpriseDetail from '@/views/enterprise/detail.vue'
import EnterpriseValidate from '@/views/enterprise/validate.vue'
import VehicleManage from '@/views/vehicle/index.vue'
import DeptManager from '@/views/dept/index.vue'
import NotFound from '@/components/404.vue'
import classes from '@/components/eleclasses.vue'
import elemsglist from '@/components/elemsglist.vue'
import elefilelist from '@/components/elefilelist.vue'
import elegroup from '@/components/elegroup.vue'
import elehw from '@/components/elehw.vue'
import eleorder from '@/components/eleorder.vue'
import register from '@/components/register.vue'
Vue.use(Router)
const Login = resolve => require(['@/views/login'], resolve)



let router = new Router({
  routes: [
    {
      path: '/register',
      type: 'register',
      component: register
    },
    {
      path: '/login',
      type: 'login',
      component: Login
    },
    {
      path: '*',
      component: NotFound
    },
    {
      path: '/',
      type: 'home',
      name: 'home',
      redirect: '/classes',
      component: Home,
      children: [
        {
          path: 'classes',
          name: '课程列表',
          components: {
            default: classes,
            top: TopNav,
            //aside: LeftNav
          },
          leaf: true, // 只有一个节点
          iconCls: 'iconfont icon-home', // 图标样式class
          menuShow: true
        }
      ]
    },
    {
      path: '/classlist/:classid',
      type: 'classlist',
      name: 'classlist',
      component: Home,
      redirect: '/classlist/:classid/msglist',
      menuShow: true,
      children: [
        {
          path: 'msglist',
          name: '课程公告',
          components: {
            default: elemsglist,
            top: TopNav,
            aside: LeftNav
          },
          leaf: true,
          iconCls: 'el-icon-menu',
          menuShow: true
        },
        {
          path: 'filelist',
          name: '课程文件',
          components: {
            default: elefilelist,
            top: TopNav,
            aside: LeftNav
          },
          leaf: true,
          iconCls: 'el-icon-folder',
          menuShow: true
        },
        {
          path: 'group',
          name: '课程成员',
          components: {
            default: elegroup,
            top: TopNav,
            aside: LeftNav
          },
          leaf: true,
          iconCls: 'el-icon-user',
          menuShow: true
        },
        {
          path: 'hw',
          name: '作业检查',
          components: {
            default: elehw,
            top: TopNav,
            aside: LeftNav
          },
          leaf: true,
          iconCls: 'el-icon-s-flag',
          menuShow: true,
        },
        {
          path: 'hw/:hwid',
          name: '作业预约',
          components: {
            default: eleorder,
            top: TopNav,
            aside: LeftNav
          },
          leaf: true,
          iconCls: 'el-icon-s-flag',
          menuShow: false,
        },

      ]
    }
  ],
  mode: "history"
});


router.beforeEach((to, from, next) => {


  console.log('to:' + to.path)
  if (to.path.startsWith('/login') || to.path.startsWith('/register')) {
    window.sessionStorage.removeItem('login');
    window.sessionStorage.removeItem('password');
    window.sessionStorage.removeItem('auth');
    next()
  } else {
    let user = window.sessionStorage.getItem('login')
    console.log(user);
    if (!user) {
      next({path: '/login'})
    } else {
      next()
    }
  }
  /*
 console.log('to:' + to.path)
 if (!(to.path.startsWith('/test')))
 {
  next({path: '/test'})
 }
 */
});


export default router
