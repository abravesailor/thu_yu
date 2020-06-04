<template>
  <div>
    <div class="header-content">
      <div class="logo-part">
        <img src="../assets/logo.png" width="30" height="30">
        <span>小组讨论系统</span>
      </div>
    </div>
    <el-form ref="AccountForm" :model="account" :rules="rules" label-position="left" label-width="0px"
             class="demo-ruleForm login-container">
      <h3 class="title">欢迎登录</h3>
      <el-form-item prop="username">
        <el-input type="text" v-model="account.username" auto-complete="off" placeholder="请输入账号"></el-input>
      </el-form-item>
      <el-form-item prop="pwd">
        <el-input type="password" v-model="account.pwd" :autofocus="pwdFocus" auto-complete="off" placeholder="请输入登录密码"></el-input>
      </el-form-item>
      <!--<el-checkbox v-model="checked" checked class="remember">记住密码</el-checkbox>-->
      <el-form-item class="extra-text">
        <a href="javascript:;" class="forget-pwd" title="找回密码">忘记密码?</a>
        <router-link :to="{path: '/register'}" class="reg-text" title="立即注册">立即注册</router-link>
      </el-form-item>
      <el-form-item style="width:100%;">
        <el-button type="primary" style="width:100%;" @click.native.prevent="handleLogin" :disabled="allowLogin" :loading="loading">登录</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
  //import API from '../api/api_user'
  export default {
    data() {
      var validateAccount = (rules, value, callback) => {
        if (value === '') {
          callback(new Error('请输入账号'));
        } else {
          if (this.account.username !== '') {
            this.account.username = value;
			this.validateCorrect();
          }
          callback();
        }
      };
	  var validatePwd = (rules, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.account.pwd !== '') {
            this.account.pwd = value;
            this.validateCorrect();
          }
          callback();
        }
      };
      return {
        loading: false,
        account: {
          username: '',
          pwd: ''
        },
        rules: {
          username: [
            { required: true, validator: validateAccount, trigger: 'change' }

          ],
          pwd: [
            {required: true, validator: validatePwd, trigger: 'change'}
          ]
        },
        pwdFocus: false,
		allowLogin: true,
        checked: true
      };
    },
    created() {
      let reg_user = JSON.parse(window.sessionStorage.getItem('register-user'));
      if (reg_user) {
        this.account.username = reg_user.username;
        this.account.pwd = '';
        this.pwdFocus = true;
      }
    },
    methods: {
      handleLogin(){
        let that = this;
        let result = {
          id: '1',
          username: 'admin',
          nickname: this.account.username,
          name: 'administrator',
          email: '888888@163.com'
        };
        console.log(this.account.username);



      var _this = this
      var username = this.account.username;
      var password = this.account.pwd;
      var success = true
      // 判断用户名合法性
      if (!(username.length >= 4 && username.length <= 8)) {
        success = false
      }
      // 判断密码合法性
      if (!(password.length >= 1 && password.length <= 16)) {
        success = false
      }
      
      function GetJsonData () {
        var json = {
          'login_name': username,
          'login_password': password
        }
        return json
      }
      var isdebug = false;
      if (isdebug)
      {
        var ses = window.sessionStorage
        ses.setItem('login', username)
        ses.setItem('password', password)
        //ses.setItem('auth', data.permission)
        if (window.sessionStorage.login === username) {
          _this.$router.push('/classes')
        }
      }
      else
      {
      if (success === true) {
        $.ajax({
          type: 'post',
          url: '/api/login_ajax',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(GetJsonData()),
          dataType: 'json',
          success: function (data) {
            if (data.status === 'success') {
              console.log(username)
              var ses = window.sessionStorage
              ses.setItem('login', username)
              ses.setItem('password', password)
              ses.setItem('auth', data.permission)
              if (window.sessionStorage.login === username) {
                _this.$router.push('/classes')
              }
            } else {
              _this.seen = 'loginfail';
              _this.$notify({
              title: '提示',
              message: data.failed_reason
            })
            }
          },
          error: function (data) {
            _this.seen = 'loginfail';
            _this.$notify({
              title: '提示',
              message: '网络链接失败！'
            })
          }
        })
        
      } else {
        _this.seen = 'loginfail'
      }
      }
      },
      validateCorrect(){
        if(this.account.pwd.trim().length > 0 && this.account.username.trim().length > 0){
          this.allowLogin = false;
        } else {
          this.allowLogin = true;
        }
      }
    }
  }
</script>
<style scoped>
  body {
    background: #DFE9FB;
  }
  .header-content {
    position: fixed;
    top: 0;
    width: 100%;
    height: 50px;
    padding: 6px 0;
    border-bottom: 1px solid #ddd;
    box-shadow: 0 0 2px #ddd;
  }
  .header-content .logo-part {
    margin-left: 10px;
    font-size: 18px;
    color: #999;
  }
  .header-content .logo-part img {
    vertical-align: middle;
  }
  .login-container {
    /*box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);*/
    -webkit-border-radius: 5px;
    border-radius: 5px;
    -moz-border-radius: 5px;
    background-clip: padding-box;
    margin: 160px auto;
    width: 350px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;

    background: -ms-linear-gradient(top, #ace, #00C1DE); /* IE 10 */
    background: -moz-linear-gradient(top, #ace, #00C1DE); /*火狐*/
    background: -webkit-gradient(linear, 0% 0%, 0% 100%, from(#ace), to(#00C1DE)); /*谷歌*/
    background: -webkit-linear-gradient(top, #ace, #00C1DE); /*Safari5.1 Chrome 10+*/
    background: -o-linear-gradient(top,#ace, #00C1DE); /*Opera 11.10+*/

  }
  .login-container .title {
    margin: 0px auto 40px auto;
    text-align: center;
    color: #505458;
  }
  .login-container .remember {
    margin: 0px 0px 35px 0px;
  }
  .extra-text {
    position: relative;
    margin-bottom: 0;
    padding-left: 2px;
  }
  .extra-text a {
    font-size: 12px;
    color: #aaa;
  }
  .extra-text a:hover {
    color: #29e;
  }
  .extra-text .reg-text {
    position: absolute;
    top: 4px;
    right: 2px;
  }
</style>
