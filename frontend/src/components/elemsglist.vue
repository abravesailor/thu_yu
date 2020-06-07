<template>
  <!-- 创建要控制的区域 -->
    <div id="app">
    <div class="panel panel-primary">
      <div class="panel-heading">
        <h3 class="panel-title">公告列表</h3>
      </div>
      <div class="panel-body form-inline" v-if="isteacher">
        <input type="button" value="发布公告" class="btn btn-primary" @click="add">
      </div>
    </div>
    <el-table
    :data="tableData"
    border
    stripe
    style="width: 100%">
    <el-table-column
      prop="msg_title"
      label="公告标题"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      prop="teachers"
      label="发布者"
      align = "center"
      width="150">
    </el-table-column>
    <el-table-column
      prop="create_time"
      label="发布时间"
      align = "center"
      width="150">
    </el-table-column>
    <el-table-column
      label="查看详情"
      align = "center"
      width="150">
      <template slot-scope="scope">
        <el-button @click="handleClick(scope.row, scope.$index)" type="text" size="medium">点击查看</el-button>
      </template>
    </el-table-column>
    <el-table-column
      v-if="isteacher"
      label="删除公告"
      align = "center"
      width="150">
      <template slot-scope="scope">
        <el-button @click="del(scope.$index)" type="text" size="medium">删除</el-button>
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
      tableData: [
        { msg_title: "标题1", teachers: "老师1", create_time: "时间1", msgid: "1", context: "公告1的内容是XXXX"},
        { msg_title: "标题2", teachers: "老师2", create_time: "时间2", msgid: "2", context: "公告2的内容是XXXX"},
        { msg_title: "标题3", teachers: "老师3", create_time: "时间3", msgid: "3", context: "公告3的内容是XXXX"},
        { msg_title: "标题4", teachers: "老师4", create_time: "时间4", msgid: "4", context: "公告4的内容是XXXX"}
      ],
      keywords: "",
      isteacher: window.sessionStorage.isteacher
    };
  },
  methods: {
    add() {
      var url = this.$route.path;
      var px = url.lastIndexOf('/');
      var newurl = url.substr(0, px) + "/pubmsg";
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
      console.log(row);
      console.log(idx);



      this.$alert(this.tableData[idx].context, this.tableData[idx].msg_title, {
          confirmButtonText: '确定',
          callback: action => {
          }
        });
    },

    search(keywords) {
      var newList = [];
      // this.list.forEach(item => {
      //     if (item.name.indexOf(keywords) != -1) {
      //         newList.push(item)
      //     }
      // });
      // return newList;

      // forEach some fliter findIndex 这些都属于数组的新方法，
      // 都会对数组的每一项，进行遍历，执行相关的操作
      return this.list.filter(item => {
        //注意:在ES6中，为字符串提供了一个新方法，叫做 String.prototype.includes("要包含的字符串")
        // 如果包含，返回true，反之false
        if (item.name.includes(keywords)) {
          return item;
        }
      });
    },
    getinfo: function () {
      var _this = this;
      console.log(this.$route.params.classid);
      console.log(window.sessionStorage.login);
      $.ajax({
        type: 'post',
        url: '/api/msglist_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({'username': window.sessionStorage.login, 'classid': this.$route.params.classid}),
        dataType: 'json',
        success: function (data) {
          _this.tableData = data.tableData;
          console.log("***");
          console.log(data.tableData);
          console.log("***");
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
    console.log(this.tableData);
  }
};
</script>