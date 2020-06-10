<template>
  <!-- 创建要控制的区域 -->
  <div id="app">
    <div class="panel panel-primary">
      <div class="panel-heading">
        <h3 class="panel-title">预约检查时间</h3>
      </div>
      <div class="panel-body form-inline">
        <el-row>
          <el-col :span="8"><input type="button" value="预约时间" class="btn btn-primary" @click="add"></el-col>
          <el-col :span="8"><el-button @click="handleClick()">点击返回</el-button></el-col>
          <el-col :span="15">
          已预约时间： {{dated}} 
          <br>
          作业标题： {{title}}
          <br>
          详细信息： {{ctx}}
        </el-col>
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
      label="时间段"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      label="选择时间段"
      align = "center"
      type = "selection"
      width="200">
    </el-table-column>
    <el-table-column
      label="时间段剩余人数"
      align = "center"
      prop="number"
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
      tmpData: [],
      checked: -1,
      ordered: -1,
      tmpStatus: [],
      username: window.sessionStorage.login
    };
  },
  computed: {
    dated: function() {
      if (this.ordered == -1){
        return "无预约时间"
      }
      else
      {
        return this.tableData[this.ordered].date + ' ' + this.tableData[this.ordered].time
      }
    },
    tableData: function()
    {
      var ret = []
      for (var i = 0; i < this.tmpData.length; i++)
      {
        ret.push(this.tmpData[i]);
        console.log(this.tmpData[i]);
        ret[i].date = this.tmpData[i].starttime.substr(0, 10);
        ret[i].time = this.tmpData[i].starttime.substr(11, 5) + '-' + this.tmpData[i].endtime.substr(11, 5);
        ret[i].number = this.tmpData[i].cnt - this.tmpData[i].curcnt;
      }
      console.log(ret)
      return ret;

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
        var _this = this;
        var hwstr = this.$route.params.hwid;
        var tmphwid = Number(hwstr.substr(2));
        console.log(_this.checked);
        var idx = -1;
        for (var i = 0; i < _this.tableData.length; i++)
        {
          if (_this.checked === _this.tableData[i])
          {
            idx = i;
            break;
          }
        }
        $.ajax({
          type: 'post',
          url: '/api/assignment_upload_ajax',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify({'username': _this.username, 'hwid': tmphwid, 'lessonname': _this.$route.params.classid, 'index': idx}),
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
      getInfo()
      {
        var _this = this
        var hwstr = this.$route.params.hwid;
        var tmphwid = Number(hwstr.substr(2));
        console.log("hwid:" + hwstr);
        $.ajax({
        type: 'post',
        url: '/api/assignment_check_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({classid: this.$route.params.classid, hwid: tmphwid}),
        dataType: 'json',
        success: function (data) {
          
          console.log("success");
          console.log(data.userstatus);
          _this.tmpData = data.checking_list;
          _this.tmpStatus = JSON.parse(data.userstatus);
          _this.ordered = _this.tmpStatus[_this.username];
          _this.title = data.title;
          _this.ctx = data.context
          console.log(data.checking_list);
          console.log(data.userstatus);
          console.log(_this.ordered);
          console.log(_this.tmpData);
          console.log(_this.tmpData[0]);

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
    this.getInfo();
    //this.isteacher = false;
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
