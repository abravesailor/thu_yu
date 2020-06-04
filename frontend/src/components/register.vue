<template>
    <div>
        <div class="register-container" id="register-form">
            <h1 class="title" >用户注册</h1>
              <el-form :model="ruleForm" :rules="rules" label-position="left" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                <div class="leftbox">
                  <el-form-item label="用户名：" prop="username">
                    <el-input v-model="ruleForm.username" placeholder="4~8 个字符，作为登陆使用"></el-input>
                  </el-form-item>
                  <el-form-item label="性别：" prop="sex">
                    <el-select v-model="ruleForm.sex" placeholder="请选择您的性别">
                      <el-option label="男" value="男"></el-option>
                      <el-option label="女" value="女"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="真实姓名：" prop="realname">
                    <el-input v-model="ruleForm.realname" placeholder="请输入您的真实姓名"></el-input>
                  </el-form-item>
                  <el-form-item label="学号：" prop="StudentID">
                    <el-input v-model="ruleForm.StudentID" placeholder="请输入您的学号"></el-input>
                  </el-form-item>
                  <el-form-item label="邮箱：" prop="email">
                    <el-input v-model="ruleForm.email" placeholder="请输入可用邮箱"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
                    <el-button @click="resetForm('ruleForm')">重置</el-button>
                  </el-form-item>
                </div>
                <div class="rightbox">
                  <el-form-item label="手机号：" prop="phonenumber">
                    <el-input v-model="ruleForm.phonenumber" placeholder="请输入可用手机号"></el-input>
                  </el-form-item>
                  <el-form-item label="密码：" prop="password">
                    <el-input type="password" v-model="ruleForm.password" placeholder="8~16个字符"></el-input>
                  </el-form-item>
                  <el-form-item label="确认密码：" prop="confirmpassword">
                    <el-input type="password" v-model="ruleForm.confirmpassword" placeholder="请再次输入您的密码"></el-input>
                  </el-form-item>
                  <el-form-item label="院系：" prop="major">
                    <el-input v-model="ruleForm.major" placeholder="请输入您所在的院系"></el-input>
                  </el-form-item>
                  <el-form-item label="验证码：" prop="confirmcode">
                    <div class="confirmimg"  @click="refresh">
                      <ide :identifyCode="identifyCode"></ide>
                    </div>
                    <el-input v-model="ruleForm.confirmcode" placeholder="请输入验证码"></el-input>
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
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.ruleForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    var confirmPass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入验证码'))
      } else if (value.toUpperCase() !== this.identifyCode) {
        callback(new Error('验证码输入错误!'))
      } else {
        callback()
      }
    }
    var emailPass = (rule, value, callback) => {
      var rex = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (value === '') {
        callback(new Error('请输入您的邮箱'))
      } else if (!rex.test(value)) {
        callback(new Error('邮箱输入不正确!'))
      } else {
        callback()
      }
    }
    return {
      seen: '',
      identifyCode: '',
      ruleForm: {
        username: '',
        sex: '',
        realname: '',
        email: '',
        phonenumber: '',
        StudentID: '',
        password: '',
        confirmpassword: '',
        major: '',
        confirmcode: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          {min: 4, max: 8, message: '长度在 4 到 8 个字符', trigger: 'blur'}
        ],
        sex: [
          { required: true, message: '请选择您的性别', trigger: 'change' }
        ],
        realname: [
          {required: true, message: '请输入您的真实姓名', trigger: 'blur'}
        ],
        email: [
          { required: true, validator: emailPass, trigger: 'blur' }
        ],
        phonenumber: [
          {required: true, message: '请输入11位手机号', trigger: 'blur'},
          {min: 11, max: 11, message: '请检查输入是否为11位', trigger: 'blur'}
        ],
        StudentID: [
          {required: true, message: '您还没有输入您的学号', trigger: 'blur'},
          {min: 10, max: 10, message: '请检查输入是否为10位', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请您输入密码', trigger: 'blur'},
          {min: 8, max: 16, message: '8~16 个字符!', trigger: 'blur'}
        ],
        confirmpassword: [
          { required: true, validator: validatePass, trigger: 'blur' }
        ],
        confirmcode: [
          { required: true, validator: confirmPass, trigger: 'blur' }
        ]
      }
    }
  },
  created () {
    this.refresh()
  },
  methods: {
    red (min, max) {
      return Math.floor(Math.random() * (max - min) + min)
    },
    refresh () {
      this.identifyCode = ''
      this.make(4)
    },
    make (num) {
      this.record = 0
      for (let i = 0; i < num; i++) {
        var xr = this.red(0, 9 + 26)
        if (xr > 9) {
          xr = String.fromCharCode(65 + xr - 9)
        }
        this.identifyCode += xr
      }
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    submitForm: function (formName) {
      var _this = this
      function GetJsonData () {
        var json = {
          'register_name': _this.ruleForm.username,
          'register_realname': _this.ruleForm.realname,
          'register_StudentID': _this.ruleForm.StudentID,
          'register_sex': _this.ruleForm.sex,
          'register_email': _this.ruleForm.email,
          'register_phonenumber': _this.ruleForm.phonenumber,
          'register_password': _this.ruleForm.password,
          'register_major': _this.ruleForm.major
        }
        return json
      }
      var gks = 0
      this.$refs[formName].validate((valid) => {
        if (valid) {
          gks = 1
        } else {
          _this.$notify({
            title: '提示',
            message: '请填写全部信息'
          })
        }
      })
      if (gks === 1) {
        $.ajax({
          type: 'post',
          url: '/api/register_ajax',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(GetJsonData()),
          dataType: 'json',
          success: function (data) {
            if (data.status === 'success') {
              var ses = window.sessionStorage
              ses.setItem('register', 'success')
              console.log("regsuccess");
              _this.$router.push('/');
            } else {
              if (data.username === 'error') {
                _this.$notify({
                  title: '提示',
                  message: '注册失败！请检查用户名！'
                })
              } else if (data.StudentID === 'error') {
                _this.$notify({
                  title: '提示',
                  message: '注册失败！请检查学号！'
                })
              } else {
                _this.$notify({
                  title: '提示',
                  message: '后台错误！'
                })
              }
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
  width: 38.5%;
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
