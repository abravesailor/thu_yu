<template>
  <el-container>
    <el-header style="padding:0px;" height="50px">
      <header-bar style="margin:0px" v-bind:msbm-seen='msbm' v-bind:fbms-seen='fbms' v-bind:tsxx-seen='tsxx' v-bind:msxxgl-seen='msxxgl' v-bind:qxgl-seen='qxgl'  v-bind:my-message='mess'></header-bar>
    </el-header>
    <el-container>
      <el-aside height="100%" style="background:#fefefe">
        <el-menu class="el-menu-vertical-demo" @select="handleSelect" unique-opened>
          <el-submenu index="form">
            <template slot="title"><i class="el-icon-document"></i>修改报名表</template>
            <el-menu-item key="0" index="all" :disabled="!isTopAdmin" style="padding-right:10px;">
              <span class="nav_intvteam"><i class="el-icon-edit"></i>基本报名表</span>
            </el-menu-item>
            <el-menu-item v-for="(item, index) in accessable" :key="index+1" :index="item.name" :disabled="item.disabled" style="padding-right:10px;">
              <span class="nav_intvteam"><i class="el-icon-edit"></i>{{item.name}}</span>
            </el-menu-item>
          </el-submenu>
          <el-submenu index="12">
            <template slot="title"><i class="el-icon-view"></i>当前面试</template>
            <el-menu-item v-for="(item, index) in activeIntvs" :key="index" :index="index+''" style="padding-right:10px;">
              <span class="nav_intvteam"><i class="el-icon-time"></i>{{item.team}}</span>
              <span class="nav_intvtime">{{item.time}}</span>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main style="width:100%">
        <intvform :form="form" :submitLoading="submitLoading" v-if="editForm" @submit="submit"></intvform>
        <div v-if="editIntv" style="height:100%;overflow-y:scroll">
          <intvqrcode :intv="currentIntv"></intvqrcode>
          <intvintver :intver="intver" @submit="submitIntver"></intvintver>
          <intvtable :intv="currentIntv"></intvtable>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import headerBar from './HeaderBar.vue'
import intvForm from './interview_form.vue'
import intvTable from './interview_table.vue'
import intvIntver from './interview_intver.vue'
import intvQRCode from './interview_qrcode.vue'
import $ from 'jquery/dist/jquery.min.js'
export default {
  name: 'intvManage',
  components: {
    'header-bar': headerBar,
    'intvform': intvForm,
    'intvtable': intvTable,
    'intvintver': intvIntver,
    'intvqrcode': intvQRCode
  },
  data: function () {
    return {
      activeIntvs: [
        {team: '军乐团', time: '15:00 Mon. Nov 1, 2018', id: '1'},
        {team: '国标队', time: '15:00 Mon. Nov 1, 2018', id: '2'}
      ],
      form: {
        team: '',
        bmxx: [],
        bmwt: []
      },
      accessable: [
        {name: '军乐团', disabled: true},
        {name: '军乐团2', disabled: false}
      ],
      submitLoading: false,
      editForm: true,
      editIntv: false,
      currentIntv: '',
      intver: []
    }
  },
  created: function () {
    if (!window.sessionStorage.login) {
      this.$router.push('/')
    } else {
      this.fetchTeam()
      this.fetchIntv()
    }
  },
  methods: {
    handleSelect: function (index, path) {
      if (path[0] === 'form') {
        this.form.team = path[1]
        this.fetchForm()
        this.editForm = true
        this.editIntv = false
      } else {
        this.currentIntv = this.activeIntvs[index].id
        this.fetchIntver()
        this.editIntv = true
        this.editForm = false
      }
    },
    submit: function () {
      this.$confirm('确认修改吗？', '提示', {}).then(() => {
        let self = this
        this.submitLoading = true
        $.ajax({
          type: 'post',
          url: '/api/set_interview_form_ajax',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(self.form),
          dataType: 'json',
          success: function (data) {
            if (data.status === 'success') {
              self.$message({
                message: '提交修改成功',
                type: 'success'
              })
            } else {
              self.$message({
                message: 'Oops... 修改生效失败',
                type: 'error'
              })
            }
            self.submitLoading = false
          },
          error: function (data) {
            self.$message({
              message: '提交失败, 请检查网络连接',
              type: 'error'
            })
            self.submitLoading = false
          }
        })
      })
    },
    fetchForm: function () {
      let self = this
      $.ajax({
        type: 'post',
        url: '/api/get_interview_form_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({team: self.form.team}),
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            self.form.bmxx = data.bmxx
            self.form.bmwt = data.bmwt
          } else {
            self.$message({
              message: 'Oops... 获取服务器报名表信息失败',
              type: 'error'
            })
          }
        },
        error: function (data) {
          self.$message({
            message: '获取队伍报名表信息失败, 请检查网络连接',
            type: 'error'
          })
        }
      })
    },
    fetchIntv: function () {
      let self = this
      $.ajax({
        type: 'post',
        url: '/api/activeintv_ajax',
        contentType: 'application/json; charset=utf-8',
        data: '',
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            self.activeIntvs = data.activeIntvs
          } else {
            self.$message({message: 'Oops...获取面试失败', type: 'error'})
          }
        },
        error: function (data) {
          self.$message({message: '获取面试失败', type: 'error'})
        }
      })
    },
    fetchTeam: function () {
      let self = this
      $.ajax({
        type: 'get',
        url: '/api/get_team_name_list_ajax',
        contentType: 'application/json; charset=utf-8',
        data: '',
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            var json = JSON.parse(data.team_name_list)
            self.accessable = Object.assign({}, json)
          } else {
            self.$message({message: 'Oops... 服务器正忙，获取队伍列表失败', type: 'error'})
          }
        },
        error: function (data) {
          self.$message({message: '获取队伍列表失败，请检查您的连接', type: 'error'})
        }
      })
    },
    submitIntver: function () {
      let self = this
      $.ajax({
        type: 'post',
        url: 'api/set_intver_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({id: self.currentIntv, intver: self.intver}),
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            self.$message({message: '提交成功', type: 'success'})
          } else {
            self.$message({message: 'Oops... 服务器正忙，提交失败', type: 'error'})
          }
        },
        error: function (data) {
          self.$message({message: '提交失败，请检查您的连接', type: 'error'})
        }
      })
    },
    fetchIntver: function () {
      let self = this
      $.ajax({
        type: 'post',
        url: 'api/get_intver_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({id: self.currentIntv}),
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            self.intver = data.intver
          } else {
            self.$message({message: 'Oops... 服务器正忙，获取评委名单失败', type: 'error'})
          }
        },
        error: function (data) {
          self.$message({message: '获取评委名单失败，请检查您的连接', type: 'error'})
        }
      })
    }
  },
  computed: {
    isTopAdmin: function () {
      return window.sessionStorage.auth == 'topAdministrator'
    }
  }
}
</script>

<style scoped>
.el-container, .el-menu{
  height: 100%;
}
.el-main {
  padding: 0px;
}
.card-header {
  font-size: 20px;
}
.el-form-item .el-form-item {
  margin-bottom : 20px;
}
.nav_intvteam {
  float: left;
}
.nav_intvtime {
  color:darkgray;
  float: right;
}
</style>
