<template>
  <el-card style="height:100%;overflow-y:scroll;">
    <el-form ref="form" :model="form">
      <el-form-item>
        <el-card>
          <div slot="header">
            <span class="card-header">{{cardHeader}}</span>
          </div>
          <el-row gutter="20">
            <el-col span="12">
              <el-row>
                <el-col span="20">
                  <el-input v-model="newentry" placeholder="请输入表项名称，如“获奖记录”、“特长”等"></el-input>
                </el-col>
                <el-col span="4" style="padding-left:20px;">
                  <el-button type="success" icon="el-icon-plus" @click="addEntry" circle></el-button>
                </el-col>
              </el-row>
              <el-table :data="form.bmxx" style="width: 100%" empty-text="请添加须填写的表项" stripe>
                <el-table-column width="400" label="表项名称" prop="name" show-overflow-tooltip></el-table-column>
                <el-table-column align="right" fixed="right">
                  <template slot-scope="scope">
                    <el-button type="danger" icon="el-icon-delete" @click="deleteEntry(scope.$index, scope.row)" circle></el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-col>
            <el-col span="12">
              <el-row>
                <el-col span="20">
                  <el-input v-model="newupload" placeholder="请输入上传文件入口名称，如“简历”、“证书”等"></el-input>
                </el-col>
                <el-col span="4" style="padding-left:20px;">
                  <el-button type="success" icon="el-icon-plus" @click="addUpload" circle></el-button>
                </el-col>
              </el-row>
              <el-table :data="form.bmwt" style="width: 100%" empty-text="请添报名表附件上传入口名称" stripe>
                <el-table-column width="400" label="附件上传入口名称" prop="name" show-overflow-tooltip></el-table-column>
                <el-table-column align="right" fixed="right">
                  <template slot-scope="scope">
                    <el-button type="danger" icon="el-icon-delete" @click="deleteUpload(scope.$index, scope.row)"
                      circle></el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-col>
          </el-row>
        </el-card>
      </el-form-item>
      <el-button style="display:block;margin:auto;width:43%" type="success" @click="submit" :loading="submitLoading"
        plain>Submit</el-button>
    </el-form>
  </el-card>
</template>

<script>
export default {
  name: 'intvForm',
  props: {
    form: Object,
    submitLoading: Boolean
  },
  data: function () {
    return {
      newentry: '',
      newupload: ''
    }
  },
  methods: {
    addEntry: function () {
      this.form.bmxx.push({
        name: this.newentry
      })
      this.newentry = ''
    },
    deleteEntry: function (index, row) {
      this.form.bmxx.splice(index, 1)
    },
    addUpload: function () {
      this.form.bmwt.push({
        name: this.newupload
      })
      this.newupload = ''
    },
    deleteUpload: function (index, row) {
      this.form.bmwt.splice(index, 1)
    },
    submit: function () {
      if (this.form.team === '') {
        this.$message({message: '请先选择报名表对应的队伍', type: 'warning'})
      } else {
        this.$emit('submit')
      }
    }
  },
  computed: {
    cardHeader: function () {
      if (this.form.team === '') {
        return '请先选择报名表对应的队伍!'
      } else if (this.form.team === 'all') {
        return '基本报名表'
      } else {
        return this.form.team
      }
    }
  }
}
</script>

<style scoped>
  .el-container {
    height: 100%;
  }

  .el-main {
    padding: 0px;
  }

  .card-header {
    font-size: 20px;
  }

  .el-form-item .el-form-item {
    margin-bottom: 20px;
  }
</style>
