<template>
  <div>
    <div id='header'>
      <header-bar v-bind:msbm-seen='msbm' v-bind:fbms-seen='fbms' v-bind:tsxx-seen='tsxx' v-bind:msxxgl-seen='msxxgl' v-bind:qxgl-seen='qxgl'  v-bind:my-message='mess'></header-bar>
    </div>

    <div class="info">
      <div class="content">
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
          <el-form-item label="学号：" prop="StudentID">
            <el-input v-model="ruleForm.StudentID" placeholder="请输入您的学号"></el-input>
          </el-form-item>
          <el-form-item label="邮箱：" prop="email">
            <el-input v-model="ruleForm.email" placeholder="请输入可用邮箱"></el-input>
          </el-form-item>
          <el-form-item label="手机号：" prop="phonenumber">
            <el-input v-model="ruleForm.phonenumber" placeholder="请输入可用手机号"></el-input>
          </el-form-item>
          <el-form-item label="院系：" prop="major">
            <el-input v-model="ruleForm.major" placeholder="请输入您所在的院系"></el-input>
          </el-form-item>
          <el-form-item label="用户简介：" prop="introduce">
            <el-input v-model="ruleForm.introduce" placeholder="介绍一下自己吧"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="uploadForm">立即修改</el-button>
            <el-button @click="returnp">返回</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import headerBar from './HeaderBar.vue'
import $ from 'jquery/dist/jquery.min.js'
export default {
  name: 'modify',
  data () {
    var emailPass = (rule, value, callback) => {
      var rex = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if ((!rex.test(value)) && value !== '') {
        callback(new Error('邮箱输入不正确!'))
      } else {
        callback()
      }
    }
    return {
      ruleForm: {
        email: '',
        phonenumber: '',
        StudentID: '',
        major: '',
        introduce: ''
      },
      rules: {
        email: [
          { validator: emailPass, trigger: 'blur' }
        ],
        phonenumber: [
          {min: 11, max: 11, message: '请检查输入是否为11位', trigger: 'blur'}
        ],
        StudentID: [
          {min: 10, max: 10, message: '请检查输入是否为10位', trigger: 'blur'}
        ]
      }
    }
  },
  components: {
    'header-bar': headerBar
  },
  created () {
    if (!window.sessionStorage.login) {
      this.$router.push('/')
    }
  },
  methods: {
    uploadForm: function () {
      var _this = this
      function GetJsonData () {
        var json = {
          'modify_major': _this.ruleForm.major,
          'modify_email': _this.ruleForm.email,
          'modify_phonenumber': _this.ruleForm.phonenumber,
          'modify_introduce': _this.ruleForm.introduce
        }
        return json
      }
      $.ajax({
        type: 'post',
        url: '/api/modify_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(GetJsonData()),
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            _this.$router.push('/person')
          } else {
            _this.$notify({
              title: '提示',
              message: '服务器未相应，请稍后重试！'
            })
          }
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '修改失败！'
          })
        }
      })
    },
    returnp: function () {
      this.$router.push('/person')
    }
  }
}
</script>

<style scoped>
label{
  height: 40%;
}
.info{
  height: 700px;
  width: 100%;
  display: inline-block;
  background-color: #f5f5f5;
}
.content{
  width: 40%;
  margin-left: 30%;
  margin-top: 5%;
}
</style>
