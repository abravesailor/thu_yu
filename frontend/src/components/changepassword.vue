<template>
  <div class="content">
    <div>
      <label class="alert1" v-if="fail">{{ detail }}</label>
      <label class="alert1" v-if="success">修改成功！</label>
    </div>

    <div class="box">
      <label>旧密码：</label>
      <input id="password" type="password">
    </div>
    <div class="box">
      <label>新密码：</label>
      <input id="newpassword" type="password">
    </div>
    <div class="box">
      <label>再输入一次新密码：</label>
      <input id="confirmpassword" type="password">
    </div>
    <button class="sub" @click="change">修改</button>
  </div>
</template>

<script>
import $ from 'jquery'
export default {
  name: 'changepassword',
  data () {
    return {
      success: false,
      fail: false
    }
  },
  methods: {
    change: function () {
      var _this = this
      var newpassword = document.getElementById('newpassword')
      var confirmpassword = document.getElementById('confirmpassword')
      var password = document.getElementById('password')
      var success = true
      // 判断密码合法性
      if (!(password.value.length >= 1 && password.value.length <= 16)) {
        success = false
        password.style.setProperty('border-color', 'red')
      } else {
        password.style.setProperty('border-color', '#ccc')
      }
      if (!(newpassword.value.length >= 1 && newpassword.value.length <= 16)) {
        success = false
        newpassword.style.setProperty('border-color', 'red')
      } else {
        newpassword.style.setProperty('border-color', '#ccc')
      }
      // 判断确认密码是否一致
      if (!(newpassword.value === confirmpassword.value)) {
        success = false
        confirmpassword.style.setProperty('border-color', 'red')
      } else {
        confirmpassword.style.setProperty('border-color', '#ccc')
      }
      function GetJsonData () {
        var json = {
          'password': password.value,
          'newpassword': newpassword.value
        }
        return json
      }
      if (success === true) {
        $.ajax({
          type: 'post',
          url: '/api/password_ajax',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(GetJsonData()),
          dataType: 'json',
          success: function (data) {
            if (data.status === 'success') {
              _this.$notify({
                title: '提示',
                message: '修改成功！'
              })
            } else {
              _this.$notify({
                title: '提示',
                message: '修改失败！'
              })
            }
          },
          error: function (data) {
            _this.$notify({
              title: '提示',
              message: '修改失败！请检查原始密码是否正确。'
            })
          }
        })
      } else {
        _this.$notify({
          title: '提示',
          message: '修改失败！请检查输入是否合法。'
        })
      }
    }
  }
}
</script>

<style scoped>
label{
  height: 40%;
  width: 100%;
}
input{
  height: 60%;
  width: 100%;
  border-radius: 3px;
  box-shadow: inset 0 1px 1px rgba(0,0,0,.075);
  background-color: #fff;
  border: 1px solid #ccc;
}
.alert1{
  margin-top: 10px;
  height: 30px;
  width: 40%;
  font-size: 21px;
  font-weight: 200;
  margin-left: 30%;
  text-align: center;
  background-color: rgba(0, 119, 255, 0.568);
}
.content{
  height: 100%;
  width: 100%;
  display: inline-block;
}
.box{
  height: 10%;
  margin-top: 4%;
  margin-left: 35%;
  width: 30%;
}
.sub{
  margin-top: 5%;
  height: 10%;
  width: 15%;
  margin-left: 42.5%;
  background-color: rgb(20, 155, 20);
  font-size: 20px;
  color: #FFF;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  text-shadow: 1px 1px 1px rgba(0,0,0,.2);
}
</style>
