<template>
  <nav class="navbar-default" role="navigation">
    <div class="container-fluid">
      <div class="navbar-header">
        <a class="navbar-brand" href="javascript:;">
          艺术团招新
        </a>
      </div>
      <div>
        <ul class="nav navbar-nav">
          <li v-if="(msbmSeen && login != '未登录' && ((auth != 'teamAdministrator') && (auth != 'topAdministrator'))) || (start)" class="header-item">
            <router-link to="registerInterview">面试报名</router-link>
          </li>
          <li v-if="(fbmsSeen && login != '未登录' && ((auth == 'teamAdministrator') || (auth == 'topAdministrator'))) || (start)" class="header-item">
            <router-link to="publishinterview">发布面试</router-link>
          </li>
          <li class="header-item" v-if="(login != '未登录' && (auth == 'teamAdministrator')) || (start)">
            <router-link to="teamEnroll">队伍录取</router-link>
          </li>
          <li v-if="(msxxglSeen && login != '未登录' &&((auth == 'teamAdministrator') || (auth == 'topAdministrator'))) || (start)" class="header-item">
            <router-link to="interviewmanage">面试管理</router-link>
          </li>
          <li v-if="(msdfSeen && login != '未登录' && ((auth == 'teamAdministrator') || (auth == 'topAdministrator') || (auth == 'interviewer'))) || (start)" class="header-item">
            <router-link to="interviewvaluation">面试打分</router-link>
          </li>
        </ul>
        <ul class="nav navbar-nav navbar-right">
          <li class="header-item" v-if="login != '未登录'">
            <a @click="showTS">消息</a>
          </li>
          <li class="header-item">
            <a href="#" v-if="login == '未登录'">{{ login }}</a>
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" v-if="login != '未登录'">{{ login }}<b class="caret"></b></a>
            <ul class="dropdown-menu">
              <li><a href="#" @click="info">个人信息</a></li>
              <li><a href="#" @click="logout">退出登陆</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
    <modal name='tsxx'>
      <div style='padding: 5%; height: 70%'>
        <h3>来自：{{tsxx[tscnt].from_user}}</h3>
        <h4>内容: <h4 v-html="tsxx[tscnt].content"></h4></h4>
      </div>
      <p style='float:left; padding: 5%'>{{tscnt + 1}} / {{tsxx.length}}</p>
      <div style='float:right; padding: 5%'>
        <button class='btn btn-default' @click="preTS">上一条</button>
        <button class='btn btn-default' @click="nextTS">下一条</button>
      </div>
    </modal>
  </nav>
</template>

<style scoped>
.navbar-default{
  z-index: 999;
}
</style>

<script>
import $ from 'jquery/dist/jquery.min.js'
export default {
  name: 'headerBar',
  created () {
    if (window.sessionStorage.login) {
      this.login = window.sessionStorage.login
      this.getTsxx()
    } else {
      this.login = '未登录'
    }
  },
  mounted: function () {

  },
  data () {
    return {
      msbmSeen: true,
      fbmsSeen: true,
      tsxxSeen: true,
      msxxglSeen: true,
      qxglSeen: true,
      msdfSeen: true,
      start: false,
      myMessage: '{2}',
      tsxx: [{'from_user':'', 'content':''}],
      tscnt: 0,
      flag: false,
      auth: window.sessionStorage.auth
    }
  },
  methods: {
    getTsxx: function () {
      var _this = this
       $.ajax({
        type: 'post',
        url: '/api/ask_for_insite_mail_by_user_received_ajax',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
          _this.tsxx.splice(0, _this.tsxx.length)
          for (var i = data.result.length - 1; i >= 0; i--) {
            _this.tsxx.push(data.result[i].fields)
          }
        },
        error: function (data) {
        }
      })
    },
    preTS: function () {
      this.tscnt = this.tscnt > 0 ? this.tscnt - 1 : 0
    },
    nextTS: function () {
      this.tscnt = this.tscnt < this.tsxx.length - 1  ? this.tscnt + 1 : this.tscnt
    },
    showTS: function () {
      this.tscnt = 0
      this.$modal.show('tsxx')
    },
    home: function () {
      this.$router.push('/')
    },
    info: function () {
      this.$router.push('/person')
    },
    logout: function () {
      var _this = this
      $.ajax({
        type: 'get',
        url: '/api/logout_ajax',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            window.sessionStorage.clear()
            window.location.reload()
          } else {
            _this.$message({
              message: '访问服务器出错',
              type: 'warning'
            })
          }
        },
        error: function (data) {
          _this.$message({
            message: '访问服务器出错',
            type: 'warning'
          })
        }
      })
    }
  }
}
</script>
