<template>
  <!-- 创建要控制的区域 -->
  <div id="app">
    <div class="panel panel-primary" v-if="isteacher">
      <div class="panel-heading">
        <h3 class="panel-title">{{classname}}-学生管理</h3>
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
      width="200">
    </el-table-column>
    <el-table-column
      prop="username"
      label="学生用户名"
      align = "center"
      width="150">
    </el-table-column>
    <el-table-column
      prop="realname"
      label="学生姓名"
      align = "center"
      width="150">
    </el-table-column>
    <el-table-column
      label="勾选分组"
      align = "center"
      type = "selection"
      width="150">
    </el-table-column>
    <el-table-column
      label="解散小组"
      align = "center"
      width="150">
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
        { id: "无组别", realname: "学生1", username: "user1", group_id: 0},
        { id: "组别1", realname: "学生2", username: "user2", group_id: 1},
        { id: "组别2", realname: "学生3", username: "user3", group_id: 2},
        { id: "组别2", realname: "学生4", username: "user4", group_id: 2}
      ],
      keywords: "",
      groupcount: 2,
      checked: [],
      isteacher: Boolean(Number(window.sessionStorage.isteacher)),
      classname: "课程1"
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
          if (tmp[i].group_id == 0)
          {
            tmp[i].realid = 0;
            continue;
          }
          tmp[i].realid = groupcnt;
          if ((i == tmp.length - 1) || (tmp[i].group_id != tmp[i + 1].group_id))
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
      if (a.group_id == b.group_id)
      {
        //("chucuo");
        return (a.realname > b.realname);
      }
      else
      {
        //console.log("chucuole");
        if (a.group_id == 0)
        {
          return true;
        }
        else
        {
           if (b.group_id == 0)
          {
            return false;
          }
        }
        return a.group_id > b.group_id;
      }
    },
    checkZero(val)
    {
      if (realData[val].group_id == 0)
      {
        return true;
      }
      else
      {
        return false;
      }
    },
    add() {
      var _this = this;
      console.log("checked:")
      console.log(_this.checked);
      if (_this.checked.length == 0)
      {
        return;
      }
      var i = 0
      var lst = []
      _this.groupcount++;
      _this.tableData.forEach(item => {
        if (_this.checked.indexOf(item) != -1)
        {
          //item.group_id = this.groupcount
          lst.push(item.username);
        }
      })

      $.ajax({
        type: 'post',
        url: '/api/group_add_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({'userlist': lst, 'group_id': _this.groupcount, 'classid': _this.$route.params.classid}),
        dataType: 'json',
        success: function (data) {
          _this.$message({
            type: 'success',
            message: '添加小组成功!'
          });
          window.location.reload();
          _this.checked = []
          _this.$refs.mulTable.clearSelection();
          //_this.tableData = data.tableData;
          //console.log("***");
          //console.log(data.tableData);
          //console.log("***");
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '网络链接失败！'
          })
        }
      })

      
    },

    delgroup(idxx) {

      var idx = this.realData[idxx].group_id;
      this.$confirm('确认解散该学生所在小组?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {

          var _this = this;
          $.ajax({
            type: 'post',
            url: '/api/group_dismiss_ajax',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({'group_id': idx}),
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

        
        if (row.group_id != 0)
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
      var _this = this;
      $.ajax({
        type: 'post',
        url: '/api/groups_in_lessons_ajax',
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
    this.groupcount = 0;
    for (var i = 0; i < this.tableData.length; i++)
      if (this.groupcount < this.tableData[i].group_id)
        this.groupcount = this.tableData[i].group_id
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
