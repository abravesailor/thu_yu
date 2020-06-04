<template>
  <el-card style="height:100%;overflow-y:scroll">
    <div slot="header">
       <span class="card-header">面试打分</span>
    </div>
    <el-row class="toolbar" style="padding: 10px;">
      <el-col :span="12" style="float:left;">
        <el-form :inline="true">
          <el-form-item>
            <el-input v-model="search" placeholder="输入姓名查找"></el-input>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="12">
        <el-pagination
          layout="prev, pager, next"
          :page-size="pageSize"
          :total="inSearchTotal"
          style="float:right;"
          :current-page="currentPage"
          @current-change="handleCurrentChange"
          background>
        </el-pagination>
      </el-col>
    </el-row>

    <!-- interviewee table -->
    <el-row>
    <el-table :data="inPageIntvees" style="width: 100%" stripe>
      <el-table-column width="150" label="姓名" prop="name" show-overflow-tooltip fixed></el-table-column>
      <el-table-column width="150" label="班级" prop="class" show-overflow-tooltip></el-table-column>
      <el-table-column width="300" label="个人简介" prop="bref" show-overflow-tooltip></el-table-column>
      <el-table-column min-width="300" label="当前评分">
        <template slot-scope="scope">
          <el-rate
            :value="scope.row.value.score"
            :max=10
            low-threshold="5"
            high-threshold="8"
            :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
            disabled>
          </el-rate>
        </template>
      </el-table-column>
      <el-table-column width="260" align="right" fixed="right">
        <template slot-scope="scope">
          <el-button-group>
            <el-button type="primary" @click="fetchInfo(scope.$index, scope.row)"><i class="el-icon-info"></i> 查看报名信息</el-button>
            <el-button type="success" @click="handleEdit(scope.$index, scope.row)"><i class="el-icon-edit-outline"></i> 打分</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    </el-row>

    <!-- Dialog to give evaluation -->
    <el-dialog title="面试评价" :visible="valueFormVisible" :show-close="false">
      <el-form :model="valueForm" ref="valueForm">
        <el-form-item prop="score">
          <div class="block">
            <span class="demonstration">综合评分</span>
            <el-rate
              v-model="valueForm.value.score"
              :max=10
              low-threshold="5"
              high-threshold="8"
              :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
              show-score>
            </el-rate>
          </div>
        </el-form-item>
        <el-form-item label="评语" prop="comment">
          <el-input type="textarea" :autosize="{minRows: 2, maxRows: 4}" v-model="valueForm.value.comment" placeholder="可突出该同学的亮点或点评不足"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="danger" @click="valueFormVisible = false" plain>Cancel</el-button>
          <el-button type="primary" @click="valueSubmit" :loading="valueLoading" plain>Submit</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <!-- Dialog to show apply form info -->
    <el-dialog title="报名表信息" :visible="formVisible" :show-close="false">
      <el-table :data="formInfo" style="width: 100%" stripe>
        <el-table-column width="200" label="表项" prop="name" show-overflow-tooltip></el-table-column>
        <el-table-column width="" label="填写信息" prop="value" show-overflow-tooltip></el-table-column>
      </el-table>
      <el-button type="danger" @click="formVisible = false" plain>Cancel</el-button>
    </el-dialog>
  </el-card>
</template>

<script>
import $ from 'jquery/dist/jquery.min.js'
export default {
  name: 'intvTable',
  props: {
    intv: String
  },
  data () {
    return {
      currentPage: 20,
      pageSize: 11,
      search: '',
      valueFormVisible: false, // 编辑界面是否显示
      valueLoading: false,
      // 编辑界面数据
      valueForm: {
        index: -1,
        value: {
          score: 0,
          comment: ''
        }
      },
      intvees: [
        {index: 0, name: '马冬梅', class: '计算机系', bref: '这个人很懒，什么都没有留下这个人很懒，什么都没有留下这个人很懒，什么都没有留下这个人很懒，什么都没有留下', value: {score: 0, comment: 'mdm'}},
        {index: 1, name: '冬梅', class: '计算机系', bref: '这个人很懒，什么都没有留下', value: {score: 1, comment: 'dm'}},
        {index: 2, name: '马梅', class: '计算机系', bref: '这个人很懒，什么都没有留下', value: {score: 2, comment: 'mm'}},
        {index: 3, name: '马冬', class: '计算机系', bref: '这个人很懒，什么都没有留下', value: {score: 3, comment: 'md'}}
      ],
      formVisible: false,
      formInfo: [
        {name: '姓名', value: '某某'},
        {name: '年龄', value: 'xx'}
      ]
    }
  },
  watch: {
    intv: function (newId, oldId) {
      this.fetchIntvees(newId)
      this.handleCurrentChange(1)
    }
  },
  created: function () {
    // this.fetchIntvees(this.intv)
  },
  methods: {
    handleCurrentChange: function (val) {
      this.currentPage = val
    },
    handleEdit: function (index, row) {
      this.valueForm.value = Object.assign({}, row.value)
      this.valueForm.index = row.index
      this.valueFormVisible = true
    },
    valueSubmit: function () {
      this.$refs.valueForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认修改吗？', '提示', {}).then(() => {
            this.valueLoading = true
            let self = this
            $.ajax({
              type: 'post',
              url: '/api/submit_judge_ajax',
              contentType: 'application/json; charset=utf-8',
              data: JSON.stringify(self.getFormattedRes()),
              dataType: 'json',
              success: function (data) {
                if (data.status === 'success') {
                  self.$message({message: '提交成功', type: 'success'})
                  self.intvees[self.valueForm.index].value = self.valueForm.value
                } else {
                  self.$message({message: 'Oops... 发布面试接收失败', type: 'error'})
                }
                self.valueLoading = false
                self.valueFormVisible = false
              },
              error: function (data) {
                self.$message({message: 'Oops, 提交失败', type: 'error'})
                self.valueLoading = false
                self.valueFormVisible = false
              }
            })
          })
        }
      })
    },
    getFormattedRes: function () {
      let res = Object.assign({}, this.valueForm.value)
      res.intv = this.intv
      res.intvee = this.intvees[this.valueForm.index].name
      return res
    },
    fetchIntvees: function (intvid) {
      let self = this
      self.s
      $.ajax({
        type: 'post',
        url: '/api/intvees_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({id: intvid}),
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            self.intvees = data.intvees
          } else {
            self.$message({message: 'Oops...获取面试数据失败', type: 'error'})
          }
        },
        error: function (data) {
          self.$message({message: '获取面试数据失败', type: 'error'})
        }
      })
      this.handleCurrentChange(1)
    },
    fetchInfo: function (index, row) {
      let self = this
      self.formVisible = true
      $.ajax({
        type: 'post',
        url: '/api/fetch_form_info_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({id: intv, username: self.intvees[index].name}),
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            self.formInfo = data.content
            self.formVisible = true
          } else {
            self.$message({message: 'Oops...获取报名数据失败', type: 'error'})
          }
        },
        error: function (data) {
          self.$message({message: '获取报名数据失败', type: 'error'})
        }
      })
    }
  },
  computed: {
    inSearchIntvees: function () {
      return this.intvees.filter(data => !this.search || data.name.toLowerCase().includes(this.search.toLowerCase()))
    },
    inSearchTotal: function () {
      return this.inSearchIntvees.length
    },
    inPageIntvees: function () {
      return this.inSearchIntvees.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
    }
  }
}
</script>

<style scoped>
.el-menu {
  height: 100%;
}
.card-header {
  font-size: 20px;
}
</style>
