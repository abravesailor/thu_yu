<template>
  <el-container>
    <el-header style="padding:0px;" height="50px">
      <header-bar style="margin:0px" v-bind:msbm-seen='msbm' v-bind:fbms-seen='fbms' v-bind:tsxx-seen='tsxx' v-bind:msxxgl-seen='msxxgl' v-bind:qxgl-seen='qxgl'  v-bind:my-message='mess'></header-bar>
    </el-header>
    <el-container>
      <el-main>
        <el-card style="height:100%;overflow-y:scroll;">
          <el-form ref="release" :model="release" :rules="inputrule">
            <el-form-item>
              <el-card>
                <div slot="header">
                  <span class="card-header">面试基本信息</span>
                </div>
                <el-form-item label="所属团体" prop="team">
                  <el-select v-model="release.team" placeholder="请选择面试所属队伍">
                    <el-option
                      v-for="item in options"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                      :disabled="item.disabled">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="选择日期" prop="date">
                  <el-date-picker
                    v-model="release.date"
                    type="date"
                    placeholder="请选择面试日期">
                  </el-date-picker>
                </el-form-item>
                <el-form-item label="起止时间">
                  <el-time-picker
                    is-range
                    v-model="release.timerange"
                    range-separator="To"
                    start-placeholder="开始时间"
                    end-placeholder="结束时间"
                    style="width: 400px">
                  </el-time-picker>
                </el-form-item>
                <el-form-item label="面试说明">
                  <el-col span="16">
                    <el-input
                      type="textarea"
                      :autosize="{ minRows: 2, maxRows: 4}"
                      placeholder="请输入面试地点等基本描述"
                      v-model="release.description">
                    </el-input>
                  </el-col>
                </el-form-item>
              </el-card>
            </el-form-item>
            <el-form-item>
              <el-card>
                <div slot="header">
                  <span class="card-header">指定现场评委</span>
                </div>
                <el-row gutter="20">
                  <el-col span="12">
                    <el-row>
                      <el-col span="20">
                        <el-input v-model="search" placeholder="输入姓名查找"></el-input>
                      </el-col>
                      <el-col span="4" style="padding-left:20px;">
                        <el-button type="primary" icon="el-icon-search" :loading="searchLoading" @click="searchIntver" circle></el-button>
                      </el-col>
                    </el-row>
                    <el-table :data="filterintver" style="width: 100%" empty-text="未查到匹配用户" stripe>
                      <el-table-column width="400" label="艺术团成员名" prop="name" show-overflow-tooltip></el-table-column>
                      <el-table-column align="right">
                        <template slot-scope="scope">
                          <el-button type="success" icon="el-icon-plus" @click="addIntver(scope.$index, scope.row)" circle></el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-col>
                  <el-col span="12">
                    <el-table :data="release.intver" style="width: 100%" empty-text="请添加评委" stripe>
                      <el-table-column width="400" label="当前评委名单" prop="name" show-overflow-tooltip></el-table-column>
                      <el-table-column align="right">
                        <template slot-scope="scope">
                          <el-button type="danger" icon="el-icon-delete" @click="deleteIntver(scope.$index, scope.row)" circle></el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-col>
                </el-row>
              </el-card>
            </el-form-item>
            <el-button style="display:block;margin:auto;width:43%" type="success" @click="submit" :loading="submitLoading" plain>Submit</el-button>
          </el-form>
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import headerBar from './HeaderBar.vue'
import $ from 'jquery/dist/jquery.min.js'
export default {
  name: 'PublishInterview',
  components: {
    'header-bar': headerBar
  },
  data: function () {
    var dateValidator = (rule, value, callback) => {
      if ((value.valueOf() < Date.now()) && (value.getDate() < new Date(Date.now()).getDate())) {
        callback(new Error('注意所设日期早于今天！'))
      } else {
        callback()
      }
    }
    return {
      release: {
        team: '',
        date: '',
        timerange: [new Date(2018, 9, 10, 0, 0, 0), new Date(2018, 9, 10, 23, 59, 59)],
        description: '',
        intver: []
      },
      inputrule: {
        team: [
          {required: true, message: '请选择面试所属队伍', trigger: 'change'}
        ],
        date: [
          {required: true, message: '请选择面试日期', trigger: 'change'},
          {validator: dateValidator, trigger: 'change'}
        ]
      },
      search: '',
      matchintver: [],
      options: [{
        value: '军乐团',
        label: '军乐团'
      }, {
        value: '舞蹈队',
        label: '舞蹈队',
        disabled: true
      }, {
        value: '国标队',
        label: '国标队'
      }],
      submitLoading: false,
      searchLoading: false
    }
  },
  created: function () {
    if (!window.sessionStorage.login) {
      this.$router.push('/')
    } else {
      this.fetchTeam()
    }
  },
  methods: {
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
            self.options = json
            for (let i of self.options) {
              i.value = i.name
              i.label = i.name
            }
          } else {
            self.$message({message: 'Oops... 服务器正忙，获取队伍列表失败', type: 'error'})
          }
        },
        error: function (data) {
          self.$message({message: '获取队伍列表失败，请检查您的连接', type: 'error'})
        }
      })
    },
    searchIntver: function () {
      let self = this
      self.searchLoading = true
      $.ajax({
        type: 'post',
        url: '/api/search_usr_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({keyword: self.search}),
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            self.matchintver = data.result
          } else {
            self.$message({message: 'Oops... 服务器正忙', type: 'error'})
          }
          self.searchLoading = false
        },
        error: function (data) {
          self.$message({message: '搜索用户失败失败，请检查您的连接', type: 'error'})
          self.searchLoading = false
        }
      })
    },
    addIntver: function (index, row) {
      this.release.intver.push({name: this.filterintver[index].name, username: this.filterintver[index].username})
    },
    deleteIntver: function (index, row) {
      this.release.intver.splice(index, 1)
    },
    submit: function () {
      this.$refs.release.validate((valid) => {
        if (valid) {
          if (this.release.intver.length === 0) {
            this.$message({message: '请指定现场评委！', type: 'warning'})
          } else if (this.timeNOTset()) {
            this.$message({message: '请设置面试时间！', type: 'warning'})
          } else {
            this.$confirm('确认修改吗？', '提示', {}).then(() => {
              this.submitLoading = true
              let self = this
              $.ajax({
                type: 'post',
                url: '/api/register_interview_ajax',
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify(self.getFormattedResult()),
                dataType: 'json',
                success: function (data) {
                  if (data.status === 'success') {
                    self.$message({message: '发布面试成功', type: 'success'})
                  } else {
                    self.$message({message: 'Oops... 发布面试接收失败', type: 'error'})
                  }
                  self.submitLoading = false
                },
                error: function (data) {
                  self.$message({message: '发布面试失败, 请检查网络连接', type: 'error'})
                  self.submitLoading = false
                }
              })
            })
          }
        } else {
          this.$message({message: '提交失败，请检查输入！', type: 'warning'})
        }
      })
    },
    toUTCTime: function (date) {
      return new Date(date.valueOf() - 60000 * date.getTimezoneOffset())
    },
    timeNOTset: function () {
      return (this.release.timerange[0].valueOf() === (new Date(2018, 9, 10, 0, 0, 0)).valueOf()) &&
      (this.release.timerange[1].valueOf() === (new Date(2018, 9, 10, 23, 59, 59)).valueOf())
    },
    getFormattedResult: function () { // get formatted result ready for submission
      let res = Object.assign({}, this.release)
      res.date = this.toUTCTime(res.date).toJSON().substring(0, 10)
      res.starttime = res.timerange[0].toTimeString().substring(0, 5)
      res.endtime = res.timerange[1].toTimeString().substring(0, 5)
      return res
    }
  },
  computed: {
    filterintver: function () {
      return this.matchintver.filter(data => {
        for (let a of this.release.intver) {
          if (a.name === data.name) {
            return false
          }
        }
        return true
      })
    }
  }
}
</script>

<style scoped>
.el-container, .el-tabs {
  height: 100%;
}
.el-tabs {
  width: 100%;
}
.el-main {
  padding: 0px;
}
.card-header {
  font-size: 20px;
}
.el-menu {
  height: 100%
}
.el-form-item .el-form-item {
  margin-bottom : 20px;
}
span.el-tab{
  padding: 10px;
}
</style>
