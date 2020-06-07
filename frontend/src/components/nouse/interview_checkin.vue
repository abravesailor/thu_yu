<template>
  <el-container>
    <el-card v-if="!succeeded" style="margin:auto;margin-top:100px;padding: 10px 100px;">
      <el-form ref="submit" :model="submit" :rules="checkinRules">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="submit.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="submit.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
      </el-form>
      <el-button
        :type="button.type"
        style="width:80%;margin-left:10%;margin-top:50px;"
        @click="checkin">
        {{button.note}}
        <i :class="button.class"></i>
      </el-button>
    </el-card>
  </el-container>
</template>

<script>
import $ from 'jquery/dist/jquery.min.js'
export default {
  name: 'checkin',
  data: function () {
    return {
      submit: {
        id: '',
        username: '',
        password: ''
      },
      checkinRules: {
        username: [{required: true, message: '请输入用户名', trigger: 'blur'}],
        password: [{required: true, message: '请输入密码', trigger: 'blur'}]
      },
      button: {
        type: 'primary',
        class: '',
        note: '签到'
      }
    }
  },
  created: function () {
    this.submit.id = this.$route.params.id
  },
  methods: {
    checkin: function () {
      if (this.button.type !== 'success') {
        this.$refs.submit.validate((valid) => {
          if (valid) {
            let self = this
            console.log('hah')
            $.ajax({
              type: 'post',
              url: '/api/qrcode_checkin_ajax',
              contentType: 'application/json; charset=utf-8',
              data: JSON.stringify(self.submit),
              dataType: 'json',
              success: function (data) {
                if (data.status === 'success') {
                  if (data.pass) {
                    self.button.type = 'success'
                    self.button.class = 'el-icon-success'
                    self.button.note = '签到成功'
                  } else {
                    self.$message({message: data.errorMsg, type: 'error'})
                  }
                } else {
                  self.$message({message: '服务器忙，请稍后重试', type: 'error'})
                }
              },
              error: function (data) {
                  self.$message({message: '签到失败，请检查连接', type: 'error'})
              }
            })
          }
        })
      }
    }
  }
}
</script>
