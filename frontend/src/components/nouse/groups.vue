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

    <table class="table table-hover table-bordered table-striped">
      <thead>
        <tr>
          <th>所在组别</th>
          <th>学生姓名</th>
          <th>勾选分组</th>
          <th>取消分组</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in list" :key="item.name">
          <td>{{item.id}}</td>
          <td>{{item.name }}</td>
          <td>
            <input type="checkbox" :value = "item.name" :id = "item.name" v-model = "checked">
          </td>
          <td>
            <a href="#" @click.prevent="delgroup(item.name)">取消分组</a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
import bar from './bar'
export default {
  name: "classes",
  data() {
    return {
      list: [
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
      this.list.forEach(item => {
        if (this.checked.indexOf(item.name) != -1)
        {
          this.delgroup(item.name)
        }
      })
      this.groupcount++;
      this.list.forEach(item => {
        if (this.checked.indexOf(item.name) != -1)
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
      this.msg = "没了"
    },

    delgroup(name) {
      var idx = 0
      for (var i = 0; i < this.list.length; i++)
      {
        if (this.list[i].name == name)
        {
          idx = i
          break
        }
      }
      console.log(i)
      var gid = this.list[idx].groupid
      var flag = false
      for (var i = 0; i < this.list.length; i++)
      {
        if (i != idx && this.list[i].groupid == gid)
        {
          flag = true
          break
        }
      }
      if (flag == false)
      {
        for (var i = 0; i < this.list.length; i++)
        {
           if (this.list[i].groupid > gid)
           {
             this.list[i].groupid--
             this.list[i].id = "组别"+this.list[i].groupid.toString()
           }
        }
        this.groupcount--
      }

      this.list[idx].groupid = 0
      this.list[idx].id = "无组别"
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
      
      let index = this.list.findIndex(item => {
        if (item.id == id) {
          return true;
        }
      });

      this.list.splice(index, 1);
      
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
  list-style-type: none;
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
