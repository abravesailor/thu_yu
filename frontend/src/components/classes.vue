<template>
  <!-- 创建要控制的区域 -->
  <div id="app">
    <div class="panel panel-primary">
      <div class="panel-heading">
        <h3 class="panel-title">课程列表</h3>
      </div>
      <div class="panel-body form-inline">
        <label>查找课程名:
          <input type="text" class="form-control" v-model="keywords">
        </label>
        
        <input type="button" value="Add" class="btn btn-primary" @click="查询">
      </div>
    </div>

    <table class="table table-hover table-bordered table-striped">
      <thead>
        <tr>
          <th>课程名</th>
          <th>主讲教师</th>
          <th>上课时间地点</th>
          <th>留空</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in search(keywords)" :key="item.id">
          <td>{{item.id}}</td>
          <td>{{item.name }}</td>
          <td>{{item.ctime}}</td>
          <td>
            <a href="#" @click.prevent="del(item.id)">留空操作</a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
export default {
  name: "classes",
  data() {
    return {
      list: [
        { id: "课程1", name: "老师1", ctime: "时间1" },
        { id: "课程2", name: "老师2", ctime: "时间2" },
        { id: "课程3", name: "老师3", ctime: "时间3" },
        { id: "课程4", name: "老师4", ctime: "时间4" }
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
