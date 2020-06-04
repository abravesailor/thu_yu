<template>
  <div>
    <div id='header'>
      <header-bar v-bind:msbm-seen='msbm' v-bind:fbms-seen='fbms' v-bind:tsxx-seen='tsxx'
      v-bind:msxxgl-seen='msxxgl' v-bind:qxgl-seen='qxgl'  v-bind:my-message='mess'></header-bar>
    </div>
    <table class='table' style='margin:1% 5% 1% 5%; width:90%'>
      <caption>人员名单</caption>
      <thead>
        <tr>
          <th>用户名</th>
          <th>姓名</th>
          <th>性别</th>
          <th>分数</th>
          <th>志愿等级</th>
          <th>录取状态</th>
          <th>信息</th>
        </tr>
      </thead>
      <tbody id='info'>
        <tr v-for="(item, index) in userList" :key="item.id">
          <td>{{item.username}}</td>
          <td>{{item.name}}</td>
          <td>{{item.sex}}</td>
          <td>{{item.score}}</td>
          <td>{{item.wish}}</td>
          <td>
            <button v-if='item.status == false' class='btn btn-success' @click="enroll(index)">录取</button>
            <button v-if='item.status == true' class='btn btn-success' @click="unenroll(index)">已录取</button>
          </td>
          <td><button class='btn btn-default' @click="showDetails(index)">用户信息</button></td>
        </tr>
      </tbody>
    </table>
    <modal name='showUserDetails'>
      <h3>Email: </h3><p>{{userInfo.email}}</p>
      <h3>联系方式: </h3><p>{{userInfo.telephone}}</p>
      <h3>介绍: </h3><p>{{userInfo.introduction}}</p>
      <h3>系别: </h3><p>{{userInfo.major}}</p>
    </modal>
  </div>
</template>

<script>
import headerBar from './HeaderBar.vue'
import $ from 'jquery/dist/jquery.min.js'
export default {
  name: 'teamEnroll',
  components: {
    'header-bar': headerBar
  },
  data: function () {
    return {
      userInfo: {
      },
      userList: []
    }
  },
  mounted: function () {
    if (!window.sessionStorage.login) {
      this.$router.push('/')
    } else {
      this.getPersonList()
    }
  },
  methods: {
    getPersonList: function () {
      this.userList.splice(0, this.userList.length)
      var _this = this
      var json = {
        'username': window.sessionStorage.login
      }
      $.ajax({
        type: 'post',
        url: '/api/get_name_score_list_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function (data) {
          // alert(JSON.stringify(data.res))
          if (data.status === 'success') {
            // _this.userList = data.userList
            for (var i = 0; i < data.res.length; i++) {
              // alert(typeof data.res[i])
              // alert(JSON.parse(data.res[i]).username)
              // alert(data.res[i].name)
              // alert(data.res[i].score)
              _this.userList.push(JSON.parse(data.res[i]))
            }
          } else {
            _this.$notify({
              title: '提示',
              message: '后台错误！'
            })
          }
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '操作失败！'
          })
        }
      })
    },
    enroll: function (index) {
      var _this = this
      var json = {
        'username': _this.userList[index].username
      }
      $.ajax({
        type: 'post',
        url: '/api/enroll_Yes_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function (data) {
          if (data.status !== 'success') {
            _this.$notify({
              title: '提示',
              message: '后台错误！'
            })
          }
          else
            _this.userList[index].status = true
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '操作失败！'
          })
        }
      })
    },
    unenroll: function (index) {
      var _this = this
      var json = {
        'username': _this.userList[index].username
      }
      $.ajax({
        type: 'post',
        url: '/api/enroll_No_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function (data) {
          if (data.status !== 'success') {
            _this.$notify({
              title: '提示',
              message: '后台错误！'
            })
          }
          else
            _this.userList[index].status = false
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '操作失败！'
          })
        }
      })
    },
    showDetails: function (index) {
      this.$modal.show('showUserDetails')
      var _this = this
      var json = {'username': this.userList[index].username}
      $.ajax({
        type: 'post',
        url: '/api/get_person_info_by_username_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function (data) {
          _this.userInfo = data
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '网络错误！'
          })
        }
      })
    }
  }
}
</script>
