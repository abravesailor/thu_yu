<template>
  <!-- 创建要控制的区域 -->
  <div id="app">
    <h3>公告列表</h3>

    <el-table
    :data="tableData"
    border
    stripe
    style="width: 100%">
    <el-table-column
      prop="title"
      label="作业标题"
      align = "center"
      width="300">
    </el-table-column>
    <el-table-column
      prop="teacher"
      label="发布者"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      prop="time"
      label="发布时间"
      align = "center"
      width="300">
    </el-table-column>
    <el-table-column
      label="预约时间"
      align = "center"
      width="200">
      <template slot-scope="scope">
        <el-button @click="handleClick(scope.row, scope.$index)" type="text" size="medium">点击查看</el-button>
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
        { title: "标题1", teacher: "老师1", time: "时间1", msgid: "1"},
        { title: "标题2", teacher: "老师2", time: "时间2", msgid: "2"},
        { title: "标题3", teacher: "老师3", time: "时间3", msgid: "3"},
        { title: "标题4", teacher: "老师4", time: "时间4", msgid: "4"}
      ],
      keywords: ""
    };
  },
  methods: {
    add() {
      // vue中已经实现了数据的双向绑定，每当我们修改了data中的数据，Vue会默认监听到
      // 数据的改动，自动把最新的数据，应用到页面上
      this.list.push({ id: this.id, name: this.name, ctime: new Date() });
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
      var url = this.$route.path+'/'+this.tableData[idx].msgid;
      this.$router.push(url);
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
      var _this = this
      $.ajax({
        type: 'get',
        url: '/api/hwlist_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({classid: this.$route.params.classid}),
        dataType: 'json',
        success: function (data) {
          _this.tableData = data.tableData;
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
    //this.getinfo()
  }
};
</script>