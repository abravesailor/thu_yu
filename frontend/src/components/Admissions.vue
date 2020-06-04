<template>
  <div class="content">

    <div class="toolbar">
      <div class="opt">
        <el-input v-model="search" placeholder="请输入您的搜索内容" class="textbox"></el-input>
        <el-input v-model="searcher" placeholder="请输入您的搜索内容" class="textbox"></el-input>
      </div>
      <el-button type="primary" round size="small" @click="send" class="sender">确定录取名单并推送</el-button>
    </div>

    <div class="admislist">
      <el-table :data="YDatas" height="100%" border style="width: 100%">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="姓名：">
                <span>{{ props.row.username }}</span>
              </el-form-item>
              <el-form-item label="性别：">
                <span>{{ props.row.sex }}</span>
              </el-form-item>
              <el-form-item label="学号：">
                <span>{{ props.row.StudentID }}</span>
              </el-form-item>
              <el-form-item label="院系：">
                <span>{{ props.row.major }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column label="预录取人员" width="150">
          <template slot-scope="scope">
            <span v-bind:class="{active: (scope.row.conflict === 'Yes')}">{{ scope.row.username }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="group" label="录取队伍" width="100"></el-table-column>
        <el-table-column prop="email" label="邮箱" width="250"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button @click="handleClick(scope.row, scope.$index, YData)" type="text" size="small">移除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="unadmislist">
      <el-table :data="NDatas" height="100%" border style="width: 100%">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="姓名：">
                <span>{{ props.row.username }}</span>
              </el-form-item>
              <el-form-item label="性别：">
                <span>{{ props.row.sex }}</span>
              </el-form-item>
              <el-form-item label="学号：">
                <span>{{ props.row.StudentID }}</span>
              </el-form-item>
              <el-form-item label="院系：">
                <span>{{ props.row.major }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="没有被录取人员" width="150"></el-table-column>
		<el-table-column prop="group" label="填报队伍" width="100"></el-table-column>
		<el-table-column prop="email" label="邮箱" width="250"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button @click="admitClick(scope.row, scope.$index, NData)" type="text" size="small">录取</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import $ from 'jquery/dist/jquery.min.js'
export default {
  name: 'admission',
  data () {
    return {
      YData: [],
      NData: [],
      type: '',
      text: '',
      search: '',
      searcher: ''
    }
  },
  computed: {
    YDatas () {
      const search = this.search
      if (search) {
        return this.YData.filter(data => {
          return Object.keys(data).some(key => {
            return String(data[key]).indexOf(search) > -1
          })
        })
      }
      return this.YData
    },
    NDatas () {
      const searcher = this.searcher
      if (searcher) {
        return this.NData.filter(data => {
          return Object.keys(data).some(key => {
            return String(data[key]).indexOf(searcher) > -1
          })
        })
      }
      return this.NData
    }
  },
  methods: {
    flit () {
      var YData = this.YData
      for (var i = 0; i < this.YData.length; i++) {
        for (var j = 0; j < this.YData.length; j++) {
          if ((i !== j) && (YData[i].username === YData[j].username)) {
            YData[i]['conflict'] = 'Yes'
          } else {
		    if (YData[i]['conflict'] !== 'Yes') {
			YData[i]['conflict'] = 'No'
			}
          }
        }
      }
    },
    handleClick (row, index, table) {
      var _this = this
      var user = row.username
      var StudentID = row.StudentID
      var conflict = row.conflict
	  var team = row.group
      function GetJsonData () {
        var json = {
          'username': user,
          'StudentID': StudentID,
          'team': team,
          'conflict': conflict
        }
        return json
      }
      $.ajax({
        type: 'post',
        url: '/api/admit_delete_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(GetJsonData()),
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            _this.YData = data.admitdata
            _this.NData = data.notadmit
            _this.flit()
            _this.$notify({
              title: '提示',
              message: '移除成功！'
            })
          } else {
            _this.$notify({
              title: '提示',
              message: '修改失败！'
            })
          }
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '网路连接失败！'
          })
        }
      })
    },
    admitClick (row, index, table) {
      var _this = this
      var user = row.username
      var StudentID = row.StudentID
      var json = {
        'username': user,
        'StudentID': StudentID,
        'team': row.group
      }
      $.ajax({
        type: 'post',
        url: '/api/admit_add_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(json),
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            _this.YData = data.admitdata
            _this.NData = data.notadmit
            _this.flit()
            _this.$notify({
              title: '提示',
              message: '录取成功！'
           })
          } else {
            _this.$notify({
              title: '提示',
              message: '修改失败！'
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
    },
    getinfo () {
      var _this = this
      $.ajax({
        type: 'get',
        url: '/api/admit_get_ajax',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            _this.YData = data.admitdata
            _this.NData = data.notadmit
			if (data.admitdata !== undefined) {
              _this.flit()
			}
          }
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '网络链接失败！'
          })
        }
      })
    },
    send () {
      var _this = this
      var YData = this.YData
      for (var i = 0; i < this.YData.length; i++) {
        if (YData[i].conflict === 'Yes') {
          _this.$notify({
            title: '提示',
            message: '还有冲突没有处理！'
          })
          return
        }
      }
      $.ajax({
        type: 'get',
        url: '/api/admin_send_ajax',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            _this.$notify({
              title: '提示',
              message: '系统推送已经发布！'
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
    }
  },
  created () {
    this.getinfo()
  }
}
</script>

<style scoped>
.content{
  height: 100%;
  width: 100%;
  margin-top: 0%;
  display: inline-block;
}
.admislist{
  float: left;
  height: 90%;
  width: 49.5%;
}
.unadmislist{
  float: right;
  height: 90%;
  width: 49.5%;
}
.toolbar{
  position: relative;
  height: 10%;
  width: 100%;
  display: inline-block;
  background-color: beige;
}
.opt{
  position: relative;
  margin-top: 1.5%;
  margin-left: 15%;
  width: 70%;
  display: inline-block;
}
.sender{
  display: inline-block;
}
.poss{
  margin-top: 5%;
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
  width: 49.5%;
  display: inline-block;
}
.dd{
  display: inline-block;
}
.button1{
  width: 10%;
  margin-left: 10%;
  display: inline-block;
}
.active {
  color: red;
}
</style>
