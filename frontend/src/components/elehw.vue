<template>
  <!-- 创建要控制的区域 -->
  <div id="app">
    <div class="panel panel-primary" >
      <div class="panel-heading">
        <h3 class="panel-title">{{classname}}-作业列表</h3>
      </div>
      <div class="panel-body form-inline" v-if="isteacher">
        <input type="button" value="发布作业" class="btn btn-primary" @click="add">
      </div>
    </div>

    <el-table
    v-if="isteacher"
    :data="tableData"
    border
    stripe
    style="width: 100%">
    <el-table-column
      prop="title"
      label="作业标题"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      prop="distributor"
      label="发布者"
      align = "center"
      width="120">
    </el-table-column>
    <el-table-column
      prop="ddl"
      label="提交截止时间"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      label="查看详情"
      align = "center"
      width="120">
      <template slot-scope="scope">
        <el-button @click="handleClickTeacher(scope.row, scope.$index)" type="text" size="medium">点击查看</el-button>
      </template>
    </el-table-column>
    <el-table-column
      label="删除作业"
      align = "center"
      width="120">
      <template slot-scope="scope">
        <el-button @click="handleClickDelete(scope.row, scope.$index)" type="text" size="medium">点击删除</el-button>
      </template>
    </el-table-column>
  </el-table>

    <el-table
    v-else-if="!isteacher"
    :data="tableData"
    border
    stripe
    style="width: 100%">
    <el-table-column
      prop="title"
      label="作业标题"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      prop="distributor"
      label="发布者"
      align = "center"
      width="120">
    </el-table-column>
    <el-table-column
      prop="ddl"
      label="提交截止时间"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      prop="submitted"
      label="提交状态"
      align = "center"
      width="120">
    </el-table-column>
    <el-table-column
      label="提交作业"
      align = "center"
      width="120">
      <template slot-scope="scope">
        <el-button @click="handleClick(scope.row, scope.$index)" type="text" size="medium" :disabled="tableData[scope.$index].passddl">点击查看</el-button>
      </template>
    </el-table-column>
  </el-table>
  </div>
</template>



<script>
export default {
  name: "classes",
  data() {
    return {
      tmpData: [],
      keywords: "",
      isteacher: Boolean(Number(window.sessionStorage.isteacher)),
      classname: "课程1"
    };
  },
  computed: {
    tableData()
    {
      var ret = []
      for (var i = 0; i < this.tmpData.length; i++)
      {
        ret.push(this.tmpData[i]);
        if (this.tmpData[i].upload_status == "False")
          ret[i].submitted = "未提交";
        else
          ret[i].submitted = "已提交";
      }
      return ret;
    }
  },
  methods: {
    add() {
      // vue中已经实现了数据的双向绑定，每当我们修改了data中的数据，Vue会默认监听到
      // 数据的改动，自动把最新的数据，应用到页面上
      var url = this.$route.path;
      var px = url.lastIndexOf('/');
      var newurl = url.substr(0, px) + "/pubhw";
      this.$router.push(newurl);
    },

    del(id) {
      // 根据Id删除数据
      // this.list.some((item, i) => {
      //     if (item.id == id) {
      //         this.list.splice(i, 1)
      //         // 在数组的 some 方法中，如果return true ，就会立即终止这个数组的后续循环
      //         return true
      //     }
      // })
      /*
      let index = this.list.findIndex(item => {
        if (item.id == id) {
          return true;
        }
      });

      this.list.splice(index, 1);
      */
    },

    handleClick(row, idx) {
      console.log(row)
      console.log(idx)
      var url = this.$route.path+this.tableData[idx].hwid;
      this.$router.push(url);
    },



    handleClickTeacher(row, idx) {
      console.log(row)
      console.log(idx)
    },



    handleClickDelete(row, idx) {
      this.$confirm('确认删除该作业?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          var _this = this
          var dat = _this.tableData[idx];
          $.ajax({
            type: 'post',
            url: '/api/assignment_display_for_user_ajax',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({lessonname: this.$route.params.classid, username: dat.distributor, title: dat.title}),
            dataType: 'json',
            success: function (data) {
              window.location.reload();
            },
            error: function (data) {
              _this.$notify({
                title: '提示',
                message: '网络链接失败！'
              })
            }
          })
          
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });          
        });
      
    },
    getinfo: function () {
      var _this = this
      $.ajax({
        type: 'post',
        url: '/api/assignment_display_for_user_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({classid: this.$route.params.classid, username: window.sessionStorage.login}),
        dataType: 'json',
        success: function (data) {
          _this.tmpData = data.result;
          console.log(data.result);
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
    //this.isteacher = false;
  }
};
</script>