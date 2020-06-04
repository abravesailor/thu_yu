<template>
  <!-- 创建要控制的区域 -->
  <div id="app">
    <div class="panel panel-primary">
      <div class="panel-heading">
        <h3 class="panel-title">学生管理</h3>
      </div>
      <div class="panel-body form-inline">
        <input type="button" value="添加分组" class="btn btn-primary" @click="add">
      </div>
    </div>

    <el-table
    :data="tableData"
    border
    stripe
    ref = "mulTable"
    @selection-change="handleSelectionChange"
    style="width: 100%">
    <el-table-column
      prop="id"
      label="所在组别"
      align = "center"
      width="300">
    </el-table-column>
    <el-table-column
      prop="name"
      label="学生姓名"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      label="勾选分组"
      align = "center"
      type = "selection"
      width="200">
    </el-table-column>
    <el-table-column
      label="取消分组"
      align = "center"
      width="200">
      <template slot-scope="scope">
        <el-button @click="delgroup(scope.$index)" type="text" size="medium">取消分组</el-button>
      </template>
    </el-table-column>
  </el-table>

  </div>
</template>


<script>
import bar from './bar'
export default {
  name: "classes",
  data() {
    return {
      tableData: [
        { id: "无组别", name: "学生1", groupid: 0 },
        { id: "无组别", name: "学生2", groupid: 0 },
        { id: "无组别", name: "学生3", groupid: 0 },
        { id: "无组别", name: "学生4", groupid: 0 }
      ],
      keywords: "",
      groupcount: 0,
      msg: "还没",
      checked: []
    };
  },
  methods: {
    add() {
      if (this.checked.length == 0)
      {
        return
      }
      var i = 0
      this.tableData.forEach(item => {

        if (this.checked.indexOf(item) != -1)
        {
          this.delgroup(i)
        }
        i = i + 1
      })
      this.groupcount++;
      this.tableData.forEach(item => {
        if (this.checked.indexOf(item) != -1)
        {
          item.groupid = this.groupcount
          item.id = "组别" + item.groupid.toString()
        }
      })
      console.log("tmp")
      console.log(this.checked)
      var ele = document.getElementsByTagName("input")
        for (var i = 0; i < ele.length; i++)
        {
          ele[i].checked = false;
        }
        this.checked = []
        this.$refs.mulTable.clearSelection();
      this.msg = "没了"
    },

    delgroup(idxx) {
      var idx = idxx
      console.log(idx)
      var gid = this.tableData[idx].groupid
      var flag = false
      for (var i = 0; i < this.tableData.length; i++)
      {
        if (i != idx && this.tableData[i].groupid == gid)
        {
          flag = true
          break
        }
      }
      if (flag == false)
      {
        for (var i = 0; i < this.tableData.length; i++)
        {
           if (this.tableData[i].groupid > gid)
           {
             this.tableData[i].groupid--
             this.tableData[i].id = "组别"+this.tableData[i].groupid.toString()
           }
        }
        this.groupcount--
      }

      this.tableData[idx].groupid = 0
      this.tableData[idx].id = "无组别"
    },

    del(id) {
      // 根据Id删除数据
      // this.tableData.some((item, i) => {
      //     if (item.id == id) {
      //         this.tableData.splice(i, 1)
      //         // 在数组的 some 方法中，如果return true ，就会立即终止这个数组的后续循环
      //         return true
      //     }
      // })
      
      let index = this.tableData.findIndex(item => {
        if (item.id == id) {
          return true;
        }
      });

      this.tableData.splice(index, 1);
      
    },
    handleSelectionChange(val) {
        this.checked = val;
      },

    search(keywords) {
      var newtableData = [];
      // this.tableData.forEach(item => {
      //     if (item.name.indexOf(keywords) != -1) {
      //         newtableData.push(item)
      //     }
      // });
      // return newtableData;

      // forEach some fliter findIndex 这些都属于数组的新方法，
      // 都会对数组的每一项，进行遍历，执行相关的操作
      return this.tableData.filter(item => {
        //注意:在ES6中，为字符串提供了一个新方法，叫做 String.prototype.includes("要包含的字符串")
        // 如果包含，返回true，反之false
        if (item.id.includes(keywords)) {
          return item;
        }
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}
ul {
  tableData-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
