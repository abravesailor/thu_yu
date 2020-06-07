<template>
  <!-- 创建要控制的区域 -->
  <div id="app">
    <div class="panel panel-primary" v-if="isteacher">
      <div class="panel-heading">
        <h3 class="panel-title">学生管理</h3>
      </div>
      <div class="panel-body form-inline">
        <input type="button" value="添加分组" class="btn btn-primary" @click="add">
      </div>
    </div>

    <el-table
    v-if="isteacher"
    :data="realData"
    border
    stripe
    ref = "mulTable"
    @select="handleSelect"
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
      label="解散小组"
      align = "center"
      width="200">
      <template slot-scope="scope">
        <el-button @click="delgroup(scope.$index)" type="text" size="medium" :disabled="realData[scope.$index].isZero">解散小组</el-button>
      </template>
    </el-table-column>
  </el-table>

    <el-table
    v-else-if="!isteacher"
    :data="tableData"
    border
    stripe
    ref = "mulTable"
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
  </el-table>

  </div>
</template>


<script>
export default {
  name: "classes",
  data() {
    return {
      tableData: [
        { id: "无组别", name: "学生1", groupid: 0},
        { id: "组别1", name: "学生2", groupid: 1},
        { id: "组别2", name: "学生3", groupid: 2},
        { id: "组别2", name: "学生4", groupid: 2}
      ],
      keywords: "",
      groupcount: 2,
      msg: "还没",
      checked: [],
      isteacher: window.sessionStorage.isteacher
    };
  },
  computed:
  {
      realData: function()
      {
        var ret = []
        var tmp = this.tableData.sort(this.sortNumber);
        //console.log(tmp);
        var groupcnt = 1;
        for (var i = 0; i < tmp.length; i++)
        {
          if (tmp[i].groupid == 0)
          {
            tmp[i].realid = 0;
            continue;
          }
          tmp[i].realid = groupcnt;
          if ((i == tmp.length - 1) || (tmp[i].groupid != tmp[i + 1].groupid))
          {
            groupcnt++;
          }
        }
        for (var i = 0; i < tmp.length; i++)
        {
          if (tmp[i].realid == 0)
          {
            tmp[i].id = "无组别";
            tmp[i].isZero = true;
          }
          else
          {
            tmp[i].id = "组别" + tmp[i].realid.toString();
            tmp[i].isZero = false;
          }
        }
        return tmp;
      }
  },
  methods: {
    sortNumber(a, b)
    {
      if (a.groupid == b.groupid)
      {
        //("chucuo");
        return (a.name > b.name);
      }
      else
      {
        //console.log("chucuole");
        if (a.groupid == 0)
        {
          return true;
        }
        else
        {
           if (b.groupid == 0)
          {
            return false;
          }
        }
        return a.groupid > b.groupid;
      }
    },
    checkZero(val)
    {
      if (realData[val].groupid == 0)
      {
        return true;
      }
      else
      {
        return false;
      }
    },
    add() {
      if (this.checked.length == 0)
      {
        return;
      }
      var i = 0

      this.groupcount++;
      this.tableData.forEach(item => {
        if (this.checked.indexOf(item) != -1)
        {
          item.groupid = this.groupcount
        }
      })
        this.checked = []
        this.$refs.mulTable.clearSelection();
    },

    delgroup(idxx) {

      var idx = idxx
      this.$confirm('确认解散该学生所在小组?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          var gid = this.tableData[idx].groupid
      
          for (var i = 0; i < this.tableData.length; i++)
          {
          if (this.tableData[i].groupid == gid)
          {
            this.tableData[i].groupid = 0;
          }
          }
          this.$message({
            type: 'success',
            message: '解散成功!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });          
        });
      //console.log(idx)
      var gid = this.tableData[idx].groupid
      
      for (var i = 0; i < this.tableData.length; i++)
      {
        if (this.tableData[i].groupid == gid)
        {
          this.tableData[i].groupid = 0;
        }
      }
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
    handleSelect(val, row) {

        
        if (row.groupid != 0)
        {
          this.$alert('无法选择该成员，因为该成员已被分组', '错误选择', {
          confirmButtonText: '确定',
          callback: action => {
            this.$refs.mulTable.toggleRowSelection(row);
          }
          });
        }
        else
        {
          this.checked = val;
        }
      },


    getInfo()
    {
      //
      //ajax
      //
      //console.log(this.realData);
      //console.log("isteacher?:"+this.$store.state.isteacher);

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
  },
  created()
  {
    //console.log(this.$store.state.isteacher);
    console.log(this.$store.state.collapsed);
    console.log("&&&")
    this.getInfo();
  },
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
