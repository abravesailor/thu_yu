<template>
    <div>
        <div class="register-container" id="register-form">
            <h3 class="title" >发布公告</h3>
              <el-form :model="ruleForm" :rules="rules" label-position="left" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                <div class="leftbox">
                  <el-form-item label="公告标题" prop="title">
                    <el-input v-model="ruleForm.title"></el-input>
                  </el-form-item>
                  <el-form-item label="公告内容" prop="txt">
                    <el-input type="textarea" :rows="10" v-model="ruleForm.txt"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')">发布公告</el-button>
                    <el-button @click="resetForm('ruleForm')">重置</el-button>
                    <el-button @click="goback()">返回</el-button>
                  </el-form-item>
                </div>
              </el-form>
        </div>
    </div>
</template>

<script>
// import headerBar from './HeaderBar.vue'
import ident from './ident.vue'
import $ from 'jquery'
export default {
  name: 'Home',
  components: {
    //'header-bar': headerBar,
    'ide': ident
  },
  data () {
    return {
      seen: '',
      identifyCode: '',
      ruleForm: {
        title: '',
        txt: ''
      },
      rules: {
        title: [
          { required: true, message: '请输入公告标题', trigger: 'blur' },
          {max: 15, message: '长度不超过 15 个字符', trigger: 'blur'}
        ],
        txt: [
          { required: true, message: '请输入公告内容', trigger: 'blur' },
          {max: 300, message: '长度不超过 300 个字符', trigger: 'blur'}
        ],
      }
    }
  },
  created () {
    //this.refresh()
  },
  methods: {
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    goback ()
    {
      var url = this.$route.path;
      var px = url.lastIndexOf('/');
      var newurl = url.substr(0, px) + "/msglist";
      this.$router.push(newurl);
    },
    submitForm: function (formName) {
      var _this = this
      function GetJsonData () {
        var json = {
          'classid': _this.$route.params.classid,
          'msg_title': _this.ruleForm.title,
          'context': _this.ruleForm.txt,
          'username': window.sessionStorage.login
        }
        console.log(json);
        return json
      }
      var gks = 0
      _this.$refs[formName].validate((valid) => {
        if (valid) {
          gks = 1
        } else {
          _this.$notify({
            title: '提示',
            message: '请正确填写内容'
          })
        }
      })
      console.log(gks);
      console.log(this.$route.params)
      //console.log(GetJsonData());
      if (gks === 1) {
        $.ajax({
          type: 'post',
          url: '/api/add_notice_ajax',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(GetJsonData()),
          dataType: 'json',
          success: function (data) {
            if (data.status === 'success') {
              var ses = window.sessionStorage
              
              //console.log("regsuccess");
              _this.$alert('公告发布成功！', '发布成功', {
                  confirmButtonText: '确定',
                  callback: action => {
                 }
                });
              _this.goback();
            } else {
                _this.$notify({
                  title: '提示',
                  message: '后台错误！'
                })
              }
          },
          error: function (data) {
            _this.$notify({
              title: '提示',
              message: '网络链接失败！'
            })
          }
        })
      }
    }
  }
}
</script>

<style scoped>
label{
  font-weight: 500;
}
.register-container{
  width:100%;
  position: relative;
  height: 670px;
  z-index: 99;
  background:#f4f4f4;
  display: inline-block;
}
.title{
  position: relative;
  margin-left: 13.6%;
  margin-top: 2%;
  text-align: left;
  color: #444;
  height: 9%;
  width: 80%;
  padding: 2px 0 3px 20px;
  border-left: 7px solid #08c;
}
.leftbox{
  position: relative;
  float: left;
  height: 400px;
  margin-left: 10%;
  width: 70%;
}
.rightbox{
  position: relative;
  float: right;
  height: 400px;
  width: 38.5%;
  margin-right: 10%;
}
.confirmimg{
  position: absolute;
  height: 100%;
  width: 18%;
  float: left;
  z-index: 999;
  margin-left: 80%;
}
.submit{
  background-color: #08d;
  margin-left:55.7%;
  height: 9%;
  width: 10%;
  font-size: 18px;
  color: #fff;
  border: none;
  border-radius: 3px;
  overflow: hidden;
}
</style>
