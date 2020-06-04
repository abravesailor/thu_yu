<template>
  <div>
    <div id='header'>
      <header-bar v-bind:msbm-seen='msbm' v-bind:fbms-seen='fbms' v-bind:tsxx-seen='tsxx'
      v-bind:msxxgl-seen='msxxgl' v-bind:qxgl-seen='qxgl'  v-bind:my-message='mess'></header-bar>
    </div>

    <table class='table' style='margin:1% 5% 1% 5%; width:90%'>
      <caption>志愿信息</caption>
      <thead>
        <tr>
          <th>团体</th>
          <th>日期</th>
          <th>开始时间</th>
          <th>结束时间</th>
          <th>志愿等级</th>
          <th>详情信息</th>
        </tr>
      </thead>
      <tbody id='info'>
        <tr v-for="(wish, index) in wishes" v-dragging="{ item: wish, list: wishes}"
          :key="wish.name">
           <td>{{wish.interview_team_name}}</td>
          <td>{{wish.interview_date}}</td>
          <td>{{wish.interview_start_time}}</td>
          <td>{{wish.interview_end_time}}</td>
          <td>{{index === 0 ? '第一志愿' : (3 > index ? '第二志愿' : '第三志愿')}}</td>
          <td><button class='btn btn-default' @click="showDetails(0, index)">查看详情</button></td>
          <td><button class='btn btn-danger' @click="deleteWish(index)">删除</button></td>
        </tr>
        <div></div>
      </tbody>
    </table>

    <div style='text-align:center'>
      <button class='btn btn-success' @click="uploadWishes()">保存</button>
    </div>

    <div style='margin:0 5% 0 5%; float: right'>
      <select id='classify' class='selectpicker'>
        <option>all</option>
      </select>
      <button id='search' class='btn btn-primary' @click="showAll">查询</button>
    </div>

    <table class='table' style='margin:1% 5% 1% 5%; width:90%'>
      <caption>面试信息</caption>
      <thead>
        <tr>
          <th>团体</th>
          <th>日期</th>
          <th>开始时间</th>
          <th>结束时间</th>
          <th>报名状态</th>
          <th>详情信息</th>
        </tr>
      </thead>
      <tbody id='info'>
        <tr v-for="(item, index) in selectedInfo" :key="item.id">
          <td>{{item.interview_team_name}}</td>
          <td>{{item.interview_date}}</td>
          <td>{{item.interview_start_time}}</td>
          <td>{{item.interview_end_time}}</td>
          <td>
            <button v-if='item.status == false' class='btn btn-success' @click="addWish(index)">报名</button>
            <button v-if='item.status == true' class='btn btn-success'>已报名</button>
          </td>
          <td><button class='btn btn-default' @click="showDetails(1, index)">查看详情</button></td>
        </tr>
      </tbody>
    </table>
    <v-dialog/>

    <el-container>
      <el-main>
        <el-dialog title="填写报名信息" :visible="signupInfo" :show-close="false">
          <h2>基本信息</h2>
          <div v-for="(item, index) in basicinfo" :key="item.name">
            <p>{{item.name}}<input v-model="basicinfoAns[index]"></p>
          </div>
          <h2>队伍信息</h2>
          <div v-for="(item, index) in teaminfo" :key="item.name">
            <p>{{item.name}}<input v-model="teaminfoAns[index]"></p>
          </div>
          <div>
            <button class='btn btn-success' @click='signupUpload(index)'>确认</button>
            <button class='btn btn-default' @click='signupClose()'>取消</button>
          </div>
        </el-dialog>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import headerBar from './HeaderBar.vue'
import $ from 'jquery/dist/jquery.min.js'

export default {
  name: 'registerInterview',
  components: {
    'header-bar': headerBar
  },
  data: function () {
    return {
      info: [],
      selectedInfo: [],
      wishes: [],
      cnt: 0,
      signupInfo: false,
      selectedWish: 0,
      signupInfoData: [],
      signupInfoQue: [],
      basicinfo: ['姓名', '性别', '年龄'],
      teaminfo: ['兴趣爱好', '为什么选择我'],
      basicinfoAns: [],
      teaminfoAns: [],
      sendSignupInfo: {'content': '', 'id': ''}
    }
  },
  mounted: function () {
    if (!window.sessionStorage.login) {
      this.$router.push('/')
    } else {
      this.addTeam()
      // this.testaddWish()

      this.getWishes()
      this.getInfo()
      this.getBasicInfo()
      // alert(typeof this.wishes)
      // alert(this.wishes.length)
    }
  },
  methods: {
    getBasicInfo: function () {
      var _this = this
      var json = {
        'team': 'all'
      }
      $.ajax({
        type: 'post',
        url: '/api/get_interview_form_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function (data) {
          // alert(JSON.stringify(data))
          _this.basicinfo = data.bmxx
        },
        error: function (data) {
          // alert('fail')
          // alert(data)
          _this.$notify({
            title: '提示',
            message: '操作失败！'
          })
        }
      })
    },
    signupUpload: function () {
      this.confirmAddWish(this.selectedWish)
      this.signupClose()
    },
    signupClose: function () {
      this.signupInfo = false
    },
    showDetails: function (type, index) {
      this.$modal.show('dialog', {
        title: '详情信息',
        text: type === 0 ? this.wishes[index].interview_description : this.selectedInfo[index].interview_description,
        buttons: [
          {
            title: '关闭'
          }
        ]
      })
    },
    deleteWish: function (index) {
      for (var i = 0; i < this.info.length; i++) {
        if (this.info[i].id === this.wishes[index].id) {
          this.info[i].status = false
          break
        }
      }
      for (var j = 0; j < this.selectedInfo.length; j++) {
        if (this.selectedInfo[j].id === this.wishes[index].id) {
          this.selectedInfo[j].status = false
          break
        }
      }
      this.wishes.splice(index, 1)
    },
    uploadWishes: function () {
      var _this = this
      var json = {
        'content': this.wishes
      }
      $.ajax({
        type: 'post',
        url: '/api/modify_personal_priority_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function (data) {
          // alert('success')
          _this.$message({message: '保存成功', type: 'success'})
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '操作失败！'
          })
        }
      })
    },
    getWishes: function () {
      var _this = this
      this.wishes = []
      $.ajax({
        type: 'post',
        url: '/api/get_personal_priority_ajax',
        contentType: 'application/json; charset=utf-8',
        data: '',
        dataType: 'json',
        success: function (data) {
          // alert(JSON.stringify(data))
          // alert(JSON.stringify(data.priority))
          // alert('0getwishes' + _this.wishes)
          // alert('0getwishes' + _this.wishes.length)
          // _this.wishes = data.priority
          for (var k = 0; k < data.priority.length; k++) {
            _this.wishes.push(data.priority[k])
          }
          // alert('1getwishes' + _this.wishes.length)
          // alert('1getwishes' + _this.wishes)
          for (var i = 0; i < _this.wishes.length; i++) {
            for (var j = 0; j < _this.info.length; j++) {
              if (_this.wishes[i].id === _this.info[j].id) {
                _this.info[j].status = true
              }
            }
          }
          // alert('2getwishes' + _this.wishes.length)
          // alert('2getwishes' + _this.wishes)
        },
        error: function (data) {
          // alert('fail')
          // alert(JSON.stringify(data))

        }
      })
    },
    testaddWish: function () {
      this.wishes.push({
        group: '少先队',
        date: '2018-10-31',
        starttime: '12:00',
        endtime: '14:00',
        id: -1
      })
      this.wishes.push({
        group: '共青团',
        date: '2018-10-31',
        starttime: '15:00',
        endtime: '17:00',
        id: -1
      })
      this.wishes.push({
        group: '群众',
        date: '2018-10-31',
        starttime: '08:00',
        endtime: '10:00',
        id: -1
      })
    },
    addTeam: function () {
      var _this = this
      $.ajax({
        type: 'post',
        url: '/api/get_team_name_list_ajax',
        contentType: 'application/json; charset=utf-8',
        data: '',
        dataType: 'json',
        success: function (data) {
          // alert(JSON.stringify(data))
          // alert('addteam' + _this.wishes.length)
          // alert('addteam' + _this.wishes)
          var json = JSON.parse(data.team_name_list)
          // alert(JSON.stringify(json))
          for (var index in json) {
            document.getElementById('classify').options.add(new Option(json[index].name, index))
          }
          _this.showAll()
          // alert('addteam' + _this.wishes.length)
          // alert('addteam' + _this.wishes)
        },
        error: function (data) {
          // alert('fail')
          // alert(data)
          _this.$notify({
            title: '提示',
            message: '操作失败！'
          })
        }
      })
    },
    addWish: function (index) {
      this.selectedWish = index
      for (var i = 0; i < this.wishes.length; i++) {
        if (this.selectedInfo[index].interview_team_name === this.wishes[i].interview_team_name) {
          this.$modal.show('dialog', {
            title: '冲突!',
            text: '最多只能报名每个队伍发布的其中一场面试<br>冲突队伍名称: ' + this.selectedInfo[index].interview_team_name,
            buttons: [
              {
                title: '关闭'
              }
            ]
          })
          return
        }
      }
      // this.signupInfoQue = this.selectedInfo[index].interview_bmxx
      // alert(this.signupInfoQue)
      var _this = this
      var json = {
        'team': this.selectedInfo[index].interview_team_name
      }
      $.ajax({
        type: 'post',
        url: '/api/get_interview_form_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function (data) {
          // alert(JSON.stringify(data))
          _this.teaminfo = data.bmxx
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '操作失败！'
          })
        }
      })
      this.signupInfo = true
    },
    confirmAddWish: function (index) {
      this.selectedInfo[index].status = true
      for (var i = 0; i < this.info.length; i++) {
        if (this.selectedInfo[index].id === this.info[i].id) {
          this.info[i].status = true
          break
        }
      }
      // this.sendSignupInfo.splice(0, this.sendSignupInfo.length)
      var i = 0;
      var content = []
      for (i = 0; i < this.basicinfo.length; i++) {
        if (this.basicinfoAns[i] === '') {
          this.$notify({
            title: '提示',
            message: '报名表某项不能为空'
          })
          return
        }
        content.push({
          'name': this.basicinfo[i],
          'value': this.basicinfoAns[i]
        })
      }
      for (i = 0; i < this.teaminfo.length; i++) {
        if (this.teaminfoAns[i] === '') {
          this.$notify({
            title: '提示',
            message: '报名表某项不能为空'
          })
          return
        }
        content.push({
          'name': this.teaminfo[i].name,
          'value': this.teaminfoAns[i]
        })
      }
      this.sendSignupInfo.content = content
      this.sendSignupInfo.id = this.selectedInfo[index].id
      var _this = this
      // alert(JSON.stringify(this.sendSignupInfo))
      $.ajax({
        type: 'post',
        url: '/api/sign_up_interview_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(_this.sendSignupInfo),
        dataType: 'json',
        success: function (data) {
          // alert(JSON.stringify(data))
          _this.$notify({
            title: '提示',
            message: '操作成功！'
          })
        },
        error: function (data) {
          // alert('send failed')
          _this.$notify({
            title: '提示',
            message: '操作失败！'
          })
        }
      })
      // alert(this.wishes.length)
      // alert(this.info.length)
      this.wishes.push(this.selectedInfo[index])
    },
    addItem: function () {
      this.info.push({
        group: 'test',
        date: 'test',
        starttime: 'test',
        endtime: 'test',
        status: false,
        more: 'test',
        id: this.cnt++
      })
    },
    showAll: function () {
      this.selectedInfo.splice(0, this.selectedInfo.length)
      for (var i = 0; i < this.info.length; i++) {
        if (this.info[i].interview_team_name === document.getElementById('classify')[document.getElementById('classify').selectedIndex].text || document.getElementById('classify')[document.getElementById('classify').selectedIndex].text === 'all') {
          this.selectedInfo.push(this.info[i])
          for (var j = 0; j < this.wishes.length; j++) {
            if (this.wishes[j].id === this.selectedInfo[this.selectedInfo.length - 1].id) {
              this.selectedInfo[this.selectedInfo.length - 1].status = true
            }
          }
        }
      }
    },
    getInfo: function () {
      var _this = this
      // alert(document.getElementById('classify')[document.getElementById('classify').selectedIndex].text)
      var json = {
        'team': 'all'
      }
      $.ajax({
        type: 'post',
        url: '/api/get_interview_list_by_teamname_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function (data) {
          // lert(JSON.stringify(data))
          // var test = JSON.parse(data.interview_list)
          // alert('bbb')
          // alert(data.interview_list.length)
          // alert('geilist' + _this.wishes.length)
          // alert('geilist' + _this.wishes)
          for (var i = 0; i < data.interview_list.length; i++) {
            var tmp = data.interview_list[i].fields
            tmp.id = data.interview_list[i].pk
            tmp.status = false
            tmp.interview_date = tmp.interview_date.substring(0, 10)
            var arr = []
            if (tmp.interview_bmxx !== '') {
              // alert(typeof tmp.interview_bmxx)
              var reg = new RegExp('\'', 'g')
              var newstr = tmp.interview_bmxx.replace(reg, '"')
              // alert(newstr)
              // alert(JSON.parse(newstr))
              var jj = JSON.parse(newstr)
              for (var j = 0; j < jj.length; j++) {
                arr.push(jj[j])
              }
              tmp.interview_bmxx = arr
            }
            _this.info.push(tmp)
          }
          // alert('geilist' + _this.wishes.length)
          // alert('geilist' + _this.wishes)
          // alert(JSON.stringify(test))
          // alert('aaa')
        },
        error: function (data) {

        }
      })
    },
    showRegistered: function () {

    },
    showUnregistered: function () {

    },
    search: function () {

    }
  }
}
</script>
