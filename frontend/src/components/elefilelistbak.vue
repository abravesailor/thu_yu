<template>
  <!-- 创建要控制的区域 -->
  <div id="app">
    <div class="panel panel-primary">
      <div class="panel-heading">
        <h3 class="panel-title">文件列表</h3>
      </div>
      <div>
      <el-upload
        class="upload-demo"
        ref="upload"
        action="https://jsonplaceholder.typicode.com/posts/"
        :file-list="fileList"
        :limit="1"
        :on-exceed="handleExceed"
        :before-upload="beforeupload"
        >
      <el-button slot="trigger" size="small" type="primary" @click="clearUpload">选取文件</el-button>
      <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传</el-button>
      <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
      </el-upload>
      </div>
    </div>
    
    <el-table
    :data="tableData"
    border
    stripe
    style="width: 100%">
    <el-table-column
      prop="name"
      label="文件名称"
      align = "center"
      width="300">
    </el-table-column>
    <el-table-column
      prop="size"
      label="文件大小"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      prop="time"
      label="上传时间"
      align = "center"
      width="300">
    </el-table-column>
    <el-table-column
      label="下载文件"
      align = "center"
      width="200">
      <template slot-scope="scope">
        <el-button @click="handleClick(scope.row, scope.$index)" type="text" size="medium">下载</el-button>
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
        { name: "文件1", size: "大小1", time: "时间1", fileid: "1"},
        { name: "文件2", size: "大小2", time: "时间2", fileid: "2"},
        { name: "文件3", size: "大小3", time: "时间3", fileid: "3"},
        { name: "文件4", size: "大小4", time: "时间4", fileid: "4"}
      ],
      fileList: [],
      isteacher: Boolean(Number(window.sessionStorage.isteacher)),
      keywords: "",
      uploadForm: new FormData()
    };
  },
  methods: {
    add() {
      // vue中已经实现了数据的双向绑定，每当我们修改了data中的数据，Vue会默认监听到
      // 数据的改动，自动把最新的数据，应用到页面上
      this.list.push({ id: this.id, name: this.name, ctime: new Date() });
    },
    beforeupload(file){
      this.uploadForm.append('file', file);
      console.log("filetype:");
      console.log(typeof(file));
      console.log("file_name",this.uploadForm.get("file"));
      this.fileList.push(file);
      return false;
    }, 
    clearUpload(){
      //this.uploadForm = new FormData();
    },
    submitUpload()
    {
      var _this = this;
      console.log(this.fileList);
      console.log(this.uploadForm);
      console.log("file_name",_this.uploadForm.get("file"));
      let data = this.uploadForm;
      $.ajax({         
        url: '/api/upload_ajax',         
        type: "POST",
        data: data,
        processData: false,//必写
        contentType: false,//必写
        success: function(data)
        {
          _this.$notify({
            title: '提示',
            message: '上传成功'
          });
          //window.location.reload();
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '网络链接失败！'
          })
        }
      });
      
    },
    handleExceed(files, fileList) {
      this.$message.warning('每次仅限上传一个文件');
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
        url: '/api/filelist_ajax',
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

<style>

  .el-upload input[type="file"]
  {
    display:none;
  }

</style>