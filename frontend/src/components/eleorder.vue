<template>
  <!-- 创建要控制的区域 -->
  <div id="app">
    <div class="panel panel-primary">
      <div class="panel-heading">
        <h3 class="panel-title">预约检查时间</h3>
      </div>
      <div class="panel-body form-inline">
        <el-row>
          <el-col :span="12"><input type="button" value="预约时间" class="btn btn-primary" @click="add"></el-col>
          <el-col :span="30">已预约时间： {{dated}} </el-col>
          <el-col :span="30"><el-button @click="handleClick()">点击返回</el-button></el-col>
        
      </el-row>
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
      prop="date"
      label="日期"
      align = "center"
      width="300">
    </el-table-column>
    <el-table-column
      prop="time"
      label="时间"
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
export default {
  name: "classes",
  data() {
    return {
      tableData: [
        { date: "2020.6.1", time: "15:00-15:30", number: 1},
        { date: "2020.6.1", time: "15:30-16:00", number: 1},
        { date: "2020.6.1", time: "16:00-16:30", number: 1},
        { date: "2020.6.1", time: "16:30-17:00", number: 1}
      ],
      checked: -1,
      ordered: -1,
    };
  },
  computed: {
    dated: function() {
      if (this.ordered == -1){
        return "无预约时间"
      }
      else
      {
        return this.ordered.date + ' ' + this.ordered.time
      }
    }
  },
  methods: {
    add() {
      if (this.checked == -1)
      {
        this.$notify({
              title: '提示',
              message: '请选择一个时间段！'
            });
      }
      else
      {
        this.ordered = this.checked;
        console.log(this.ordered);
        this.$refs.mulTable.toggleRowSelection(this.checked);
        this.checked = -1;
        this.$notify({
              title: '提示',
              message: '预约成功！'
            });
      }
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
        if (val.length == 0)
        {
          this.checked = -1;
          return;
        }
        if (val.length == 1)
        {
          this.checked = val[0];
          return;
        }

        var prev = this.checked;
        var now = val[0];
        if (prev == now)
        {
          now = val[1];
        }

        this.$refs.mulTable.toggleRowSelection(prev);
        this.checked = now;
      },
      handleClick()
      {
        var url = this.$route.path;
        var px = url.lastIndexOf('/');
        var newurl = url.substr(0, px) + "/hw";

        this.$router.push(newurl);
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
