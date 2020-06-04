<template>
  <div class="info">
    <div class="inputbox">
        <label>用户名：</label>
        <label class="shower">{{ username }}</label>
    </div>
    <div class="inputbox">
        <label>真实姓名：</label>
        <label class="shower">{{ realname }}</label>
    </div>
    <div class="inputbox">
        <label>性别：</label>
        <label class="shower">{{ sex }}</label>
    </div>
    <div class="inputbox">
        <label>EMAIL：</label>
        <label class="shower">{{ email }}</label>
    </div>
    <div class="inputbox">
        <label>院系：</label>
        <label class="shower">{{ major }}</label>
    </div>
    <div class="inputbox">
        <label>手机号：</label>
        <label class="shower">{{ phonenumber }}</label>
    </div>
    <div class="inputbox" v-if="seen">
        <label>录取结果：</label>
        <label class="shower">您已经被{{ hav }}录取！</label>
    </div>
    <div class="inputbox">
        <label>用户简介：</label>
        <label class="tes">{{ intro }}</label>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
export default {
  name: 'person',
  data () {
    return {
      seen: false,
      username: '',
      email: '',
      major: '',
      phonenumber: '',
      intro: '',
      realname: '',
      sex: ''
    }
  },
  methods: {
    getinfo: function () {
      var _this = this
      $.ajax({
        type: 'get',
        url: '/api/person_info_ajax',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function (data) {
          _this.username = data.username
          _this.email = data.email
          _this.major = data.major
          _this.phonenumber = data.telephone
          _this.intro = data.introduction
          _this.realname = data.realname
          _this.sex = data.sex
          if (data.introduction === '') {
            _this.intro = '这个人什么都没写'
          }
          if (data.result === 'Yes') {
            _this.seen = true
            _this.hav = data.group
          } else {
            _this.seen = false
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
  },
  created () {
    this.getinfo()
  }
}
</script>

<style scoped>
label{
  height: 60%;
  width: 23%;
  font-size: 21px;
  font-weight: 200;
}
.tes{
  float: right;
  height: 100px;
  width: 75%;
  word-wrap: break-word;
  word-break: normal;
}
.shower{
  width: 75%;
}
.info{
  margin-top: 5%;
  height: 90%;
  width: 100%;
  display: inline-block;
}
.inputbox{
  margin-left: 25%;
  margin-top: 1%;
  height: 10%;
  width: 40%;
}
.textbox{
  height: 60%;
  width: 10%;
  border-radius: 5px;
}
</style>
