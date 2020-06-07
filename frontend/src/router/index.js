import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import TopNav from '@/components/final_topNav.vue'
import LeftNav from '@/components/final_leftNav.vue'
import Home from '@/views/home.vue'
import NotFound from '@/components/404.vue'
import classes from '@/components/eleclasses.vue'
import elemsglist from '@/components/elemsglist.vue'
import elepubmsg from '@/components/elepubmsg.vue'
import elepubhw from '@/components/elepubhw.vue'
import elefilelist from '@/components/elefilelist.vue'
import elegroup from '@/components/elegroup.vue'
import elehw from '@/components/elehw.vue'
import eleorder from '@/components/eleorder.vue'
import register from '@/components/register.vue'
import changepwd from '@/components/changepassword.vue'
import profile from '@/components/person.vue'
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
          stuname: '课程列表',
          components: {
            default: classes,
            top: TopNav,
            //aside: LeftNav
          },
          leaf: true, // 只有一个节点
          iconCls: 'iconfont icon-home', // 图标样式class
          menuShow: true
        },
        {
          path: 'profile',
          name: '个人信息',
          stuname: '个人信息',
          components: {
            default: profile,
            top: TopNav,
            //aside: LeftNav
          },
          leaf: true, // 只有一个节点
          iconCls: 'iconfont icon-home', // 图标样式class
          menuShow: false
        },
        {
          path: 'changepwd',
          name: '修改密码',
          stuname: '修改密码',
          components: {
            default: changepwd,
            top: TopNav,
            //aside: LeftNav
          },
          leaf: true, // 只有一个节点
          iconCls: 'iconfont icon-home', // 图标样式class
          menuShow: false
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
          stuname: '课程公告',
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
          path: 'pubmsg',
          name: '发布公告',
          stuname: '发布公告',
          components: {
            default: elepubmsg,
            top: TopNav,
            aside: LeftNav
          },
          leaf: true,
          iconCls: 'el-icon-menu',
          menuShow: false
        },
        {
          path: 'filelist',
          name: '课程文件',
          stuname: '课程文件',
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
          stuname: '小组成员',
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
          stuname: '作业检查',
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
          path: 'pubhw',
          name: '发布作业',
          stuname: '发布作业',
          components: {
            default: elepubhw,
            top: TopNav,
            aside: LeftNav
          },
          leaf: true,
          iconCls: 'el-icon-menu',
          menuShow: false
        },
        {
          path: ':hwid',
          name: '作业预约',
          stuname: '作业预约',
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
