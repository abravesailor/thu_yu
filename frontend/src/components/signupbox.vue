<template>
<div id='signupbox'>
    <div id="signup" style="text-align: center; border-radius: 5px; position: relative; top: 15%; height: 60%; left:70%; width:15%;  background-color: rgb(255, 255, 255, 0.8)">
                <br>
                <div>
                    <p style="font-size: 20px">账号密码登录</p>
                </div>
                <div>
                    <input id="account" style="width: 80%;" type="text" placeholder="账号">
                </div>
                <br>
                <div>
                    <input id="password" style="width: 80%;" type="password" placeholder="密码">
                </div>
                <br>
                <div style="">
                    <button id="register" class="btn btn-info" @click="goregister">注册</button>
                    <button id="login" class="btn btn-success" @click="gosend">登录</button>
                </div>
                <label v-if="seen == 'registersuc'">注册成功！请登录</label>
                <label v-if="seen == 'loginfail'">登录失败！</label>
                <label v-if="seen == 'loginsuc'">登录成功！</label>
            </div>
        </div>
</template>

<script>
export default {
  data () {
    return {
      seen: ''
    }
  },
  methods: {
    goregister: function () {
      this.$router.push('/register')
    },
    gosend: function () {
      var _this = this
      var username = document.getElementById('account').value
      var password = document.getElementById('password').value
      var success = true
      // 判断用户名合法性
      if (!(username.length >= 4 && username.length <= 8)) {
        success = false
      }
      // 判断密码合法性
      if (!(password.length >= 1 && password.length <= 16)) {
        success = false
      }
      /*
      function GetJsonData () {
        var json = {
          'login_name': username,
          'login_password': password
        }
        return json
      }
      */
      if (success === true) {
        /*
        $.ajax({
          type: 'post',
          url: '/api/login_ajax',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(GetJsonData()),
          dataType: 'json',
          success: function (data) {
            if (data.status === 'success') {
              _this.seen = 'loginsuc'
              var ses = window.sessionStorage
              ses.setItem('login', username)
              ses.setItem('password', password)
              ses.setItem('auth', data.permission)
              if (window.sessionStorage.login === username) {
                _this.$router.push('/person')
              }
            } else {
              _this.seen = 'loginfail'
            }
          },
          error: function (data) {
            _this.seen = 'loginfail'
          }
        })
        */
      } else {
        _this.seen = 'loginfail'
      }
    }
  }
}

</script>

<style>
  #signupbox {
    width: 90%;
    height: 500px;
    /*background-color:aquamarine;*/
    left:20%;
    background-size: 100% 100%;
    border-radius: 5px;
    margin-left: 5%;
    margin-top: 20px;
  }
</style>
