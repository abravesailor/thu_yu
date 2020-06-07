<template>
  <div class="header">
    <div class="contain">
      <div class="poss">
        <el-input v-model="search" placeholder="请输入您要查询的内容" class="textbox"></el-input>
      </div>
    </div>

    <div class="namelist">
      <el-table :data="tableDatas" height="100%" border stripe style="width: 100%">
        <el-table-column prop="username" label="用户名" width="180"></el-table-column>
        <el-table-column prop="sex" label="性别" width="100"></el-table-column>
        <el-table-column prop="studentID" label="学号" width="180"></el-table-column>
        <el-table-column prop="team" label="队伍" width="120"></el-table-column>
        <el-table-column prop="email" label="邮箱" width="300"></el-table-column>
        <el-table-column prop="major" label="系别" width="130"></el-table-column>
        <el-table-column prop="introduction" label="用户简介" width="500"></el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button type="primary" round size="small" @click="handleClick(scope.row, scope.$index)">发送消息</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import $ from 'jquery/dist/jquery.min.js'
export default {
  data () {
    return {
      username: '',
      StudentID: '',
      tableData: [],
      search: ''
    }
  },
  created () {
    this.getinfol()
  },
  computed: {
    tableDatas () {
      const search = this.search
      if (search) {
        return this.tableData.filter(data => {
          return Object.keys(data).some(key => {
            return String(data[key]).indexOf(search) > -1
          })
        })
      }
      return this.tableData
    }
  },
  methods: {
    getinfol: function () {
      var _this = this
      function GetJsonData () {
        var json = {
          'username': window.sessionStorage.login,
          'password': window.sessionStorage.password
        }
        return json
      }
      $.ajax({
        type: 'post',
        url: '/api/lookupget_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(GetJsonData()),
        dataType: 'json',
        success: function (data) {
          _this.tableData = data.tableData
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '网络链接失败！'
          })
        }
      })
    },
    handleClick: function (raw, index) {
      var conpass = (value) => {
        if (value.length > 50) {
          return '字符数目超过50个！'
        } else if (value === '') {
          return '请填写发送内容！'
        } else {
          return true
        }
      }
      var _this = this
      var tmp = raw.username
      this.$prompt('请输入内容', '发送消息', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValidator: conpass
      }).then(({ value }) => {
        var json = {
          'to_user': tmp,
          'from_user': window.sessionStorage.login,
          'message': value
        }
        $.ajax({
          type: 'post',
          url: '/api/add_insite_mail_ajax',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(json),
          dataType: 'json',
          success: function (data) {
            if (data.status === 'success') {
              _this.$message({
                type: 'success',
                message: '发送成功'
              })
            } else {
              _this.$notify({
                title: '提示',
                message: '网络链接失败！'
              })
            }
          },
          error: function (data) {
            _this.$notify({
              title: '提示',
              message: '网络链接失败！'
            })
          }
        })
      }).catch(() => {
        _this.$message({
          type: 'info',
          message: '取消输入'
        })
      })
    }
  }
}
</script>

<style scoped>
label{
  width: 7%;
  text-align: right;
}
.header{
  height: 100%;
  width: 100%;
  background-color: beige;
  display: inline-block;
}
.namelist{
  height: 90%;
  width: 100%;
}
.dd{
  display: inline-block;
}
.button1{
  width: 10%;
  margin-left: 15%;
  display: inline-block;
}
.contain{
  height: 10%;
  width: 70%;
  margin-left: 2%;
  display: inline-block;
}
.poss{
  margin-top: 2%;
  width: 100%;
  display: inline-block;
}
.leftbox{
  width: 40%;
  display: inline-block;
}
.rightbox{
  width: 40%;
  margin-left: 13%;
  display: inline-block;
}
.textbox{
  width: 40%;
}
.sendbox{
  margin-top: 2%;
  margin-left: 90%;
}
</style>
