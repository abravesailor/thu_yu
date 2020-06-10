<template>
    <el-row>
    <el-col :span="24">
      <el-input type="textarea" :row="8" v-model="cont" clearable="true"></el-input>
    </el-col>
    <el-col :span="6">
          <el-button type="primary" v-on:click="add">添加</el-button>          
    </el-col>
  </el-row>
</template>
<script>
import { getBusCxt } from '../../store';
import { Keys } from '../../uitls';
import { mapGetters } from 'vuex';
let recKey = Keys.GETNEWMSG;
export default {
  name: 'MsgWriter',
  computed: {
            ...mapGetters([recKey])
        },
  data () {
    return {
      cont: ''
    }
  },
  methods: {
    add: function () {
      /* 组件 */
      let msg = {cont: this.cont}
      getBusCxt().msgCxt.sendMsg(msg);
      //console.log(this.getNewMsg);
      this.$emit("submit-add", msg)
      
      var _this = this
      $.ajax({
        type: 'post',
        url: '/api/chat_save_ajax',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({username: window.sessionStorage.login, groupid: window.sessionStorage.groupid, ctx: _this.cont}),
        dataType: 'json',
        success: function (data) {
        },
        error: function (data) {
          _this.$notify({
            title: '提示',
            message: '网络链接失败！'
          })
        }
      })
      _this.cont = '';
    }
  }
}

</script>
