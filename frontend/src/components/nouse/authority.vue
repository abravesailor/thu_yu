<template>
  <div class="body">
    <div class="search">
      <h3 class="title" >队伍管理员权限授予</h3>
      <div class="searchbar">
        <div class="inputbox">
          <label>用户名：</label>
          <input id="name" class="textbox" type="text"  placeholder="输入用户名">
        </div>
        <div class="inputbox">
          <label>学号：</label>
          <input id="StudentID" class="textbox" type="text"  placeholder="输入学号">
        </div>
      </div>
      <button class='sub' @click="searching">查询</button>
      <div class="show" v-if="seen">
        <label class="shol">查询成功！即将给{{  name  }}授予
          <el-select v-model="value" placeholder="请选择" :value="value" class="sees">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.label" @click.native='get'>
            </el-option>
          </el-select>
        管理员权限</label>
        <button class="give" @click="give">授予权限</button>
        <button class="giveup" @click="giveup">取消</button>
      </div>
    </div>
    <div class="namelist">
      <el-table :data="tableData" height="100%" border stripe style="width: 100%">
        <el-table-column prop="name" label="用户名" width="180"></el-table-column>
        <el-table-column prop="team" label="队伍" width="100"></el-table-column>
        <el-table-column prop="StudentID" label="学号" width="130"></el-table-column>
        <el-table-column prop="email" label="邮箱" width="500"></el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button @click="handleClick(scope.row, scope.$index, tableData)" type="text" size="small">撤销权限</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import $ from 'jquery/dist/jquery.min.js'
export default {
  name: 'author',
  data () {
    return {
      seen: false,
      tableData: [],
      options: [{
        value: '1',
        label: '军乐队'
      }, {
        value: '2',
        label: '民乐队'
      }, {
        value: '3',
        label: '合唱队'
      }, {
        value: '4',
        label: '交响队'
      }, {
        value: '5',
        label: '舞蹈队'
      }, {
        value: '6',
        label: '话剧队'
      }, {
        value: '7',
        label: '国标队'
      }, {
        value: '8',
        label: '曲艺队'
      }, {
        value: '9',
        label: '键盘队'
      }, {
        value: '10',
        label: '美术社'
      }, {
        value: '11',
        label: '摄影队'
      }, {
        value: '12',
        label: '京剧队'
      }],
      value: ''
    }
  },
  created () {
    this.gettable()
  },
  methods: {
    gettable: function () {
      var _this = this
      $.ajax({
        type: 'get',
        url: '/api/authorget_ajax',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            _this.tableData = data.tableData
          }
        }
      })
    },
    searching: function () {
      var _this = this
      var user = document.getElementById('name').value
      var ID = document.getElementById('StudentID').value
      function GetJsonData () {
        var json = {
          'search_name': user,
          'search_StudentID': ID
        }
        return json
      }
      if (user === '' || ID === '') {
        _this.seen = false
        _this.$message({
          message: '请输入完整信息',
          type: 'warning'
        })
      } else {
        $.ajax({
          type: 'post',
          url: '/api/authorsearch_ajax',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(GetJsonData()),
          dataType: 'json',
          success: function (data) {
            if (data.status === 'success') {
              _this.seen = true
              _this.name = user
            } else {
              _this.$message({
                message: '未查询到',
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
    },
    give () {
      var _this = this
      var user = document.getElementById('name').value
      var ID = document.getElementById('StudentID').value
      function GetJsonData () {
        var json = {
          'give_name': user,
          'give_StudentID': ID,
          'group': _this.value
        }
        return json
      }
      if (_this.value !== '') {
        $.ajax({
          type: 'post',
          url: '/api/authorgive_ajax',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(GetJsonData()),
          dataType: 'json',
          success: function (data) {
            if (data.status === 'success') {
              _this.seen = false
              _this.tableData = data.tableData
            } else {
              _this.seen = false
              _this.$message({
                message: '失败！',
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
      } else {
        _this.$message({
          message: '请选择一个队伍！',
          type: 'warning'
        })
      }
    },
    giveup () {
      this.seen = false
      this.$message({
        message: '已取消授权动作',
        type: 'warning'
      })
    },
    handleClick (row, index, table) {
      var _this = this
      var user = row.name
      var StudentID = row.StudentID
      function GetJsonData () {
        var json = {
          'delete_name': user,
          'delete_StudentID': StudentID
        }
        return json
      }
      $.ajax({
        type: 'post',
        url: '/api/authordelete_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(GetJsonData()),
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            table.splice(index, 1)
            _this.$message({
              message: '已撤销' + row.name + '的权限',
              type: 'warning'
            })
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

<style scoped>
label{
  height: 50%;
  width: 20%;
  font-weight: 200;
}
.body{
  height: 670px;
  width: 100%;
}
.title{
  border-left: 7px solid rgb(6, 171, 253);
  margin-left: 5%;
  padding: 2px 0 2px 15px;
}
.search{
  float: left;
  margin-left: 5%;
  margin-top: 13%;
  height: 40%;
  width:  40%;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 3px 3px 3px 3px #d4d4d4;
}
.searchbar{
  margin-top: 1%;
  height: 40%;
  width: 70%;
  display: inline-block;
}
.give{
  margin-top: 1.5%;
  margin-left: 27%;
  height: 45%;
  width: 20%;
  background-color: rgb(0, 110, 253);
  font-size: 20px;
  color: #FFF;
  font-weight: 300;
  border: none;
  border-radius: 5px;
  text-shadow: 1px 1px 1px rgba(0,0,0,.2);
}
.giveup{
  margin-left: 5%;
  height: 45%;
  width: 20%;
  background-color: rgb(0, 110, 253);
  font-size: 20px;
  color: #FFF;
  font-weight: 300;
  border: none;
  border-radius: 5px;
  text-shadow: 1px 1px 1px rgba(0,0,0,.2);
}
.sees{
  width: 20%;
}
.namelist{
  float: right;
  height: 100%;
  width:  50%;
  background-color: black;
}
.inputbox{
  margin-left: 6%;
  height: 50%;
  width: 85%;
}
.textbox{
  position: relative;
  height: 35px;
  width: 78%;
  border-radius: 3px;
  box-shadow: inset 0 1px 1px rgba(0,0,0,.075);
  background-color: #fff;
  border: 1px solid #aaaaaa;
}
.shol{
  height: 30%;
  width: 100%;
  font-size: 16px;
  font-weight: 300;
  text-align: center;
}
.sub{
  float: right;
  margin-top: 2.5%;
  margin-right: 6%;
  height: 20%;
  width: 20%;
  background-color: rgb(0, 110, 253);
  font-size: 20px;
  color: #FFF;
  font-weight: 300;
  border: none;
  border-radius: 5px;
  text-shadow: 1px 1px 1px rgba(0,0,0,.2);
}
.show{
  height: 36%;
  margin-top: 0%;
}
</style>
