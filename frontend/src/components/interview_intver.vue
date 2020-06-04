<template>
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
          <el-table-column fixed="right" align="right">
            <template slot-scope="scope">
              <el-button type="success" icon="el-icon-plus" @click="addIntver(scope.$index, scope.row)" circle></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col span="12">
        <el-table :data="intver" style="width: 100%" empty-text="请添加评委" stripe>
          <el-table-column width="400" label="当前评委名单" prop="name" show-overflow-tooltip></el-table-column>
          <el-table-column fixed="right" align="right">
            <template slot-scope="scope">
              <el-button type="danger" icon="el-icon-delete" @click="deleteIntver(scope.$index, scope.row)" circle></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <el-button
      style="display:block;margin:auto;width:43%"
      type="success"
      :loading="submitLoading"
      @click="submit"
      plain>
      提交
    </el-button>
  </el-card>
</template>

<script>
import $ from 'jquery/dist/jquery.min.js'
export default {
  name: 'intvIntver',
  props: {
    intver: Array
  },
  data: function () {
    return {
      search: '',
      matchintver: [],
      submitLoading: false,
      searchLoading: false
    }
  },
  methods: {
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
      this.intver.push({name: this.filterintver[index].name, username: this.filterintver[index].username})
    },
    deleteIntver: function (index, row) {
      this.intver.splice(index, 1)
    },
    submit: function () {
      this.$emit('submit')
    }
  },
  computed: {
    filterintver: function () {
      return this.matchintver.filter(data => {
        for (let a of this.intver) {
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
</style>
