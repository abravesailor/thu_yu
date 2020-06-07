<template>
  <el-card>
    <div slot="header">
      <span class="card-header">签到二维码</span>
      <el-button type="primary" @click="showQRCode" circle><i class="el-icon-view"></i></el-button>
    </div>
    <el-dialog :visible.sync="show" :show-close="false">
      <el-tooltip content="请右键点击二维码下载打印">
        <img width="100%" height="100%" :src="path"/>
      </el-tooltip>
    </el-dialog>
  </el-card>
</template>

<script>
export default {
  name: 'intvQRCode',
  props: {
    intv: String
  },
  data: function () {
    return {
      show: false
    }
  },
  methods: {
    showQRCode: function () {
      this.show = true
    }
  },
  computed: {
    path: function () {
      return '/static/qrcodes/qr' + this.intv + '.png'
    }
  }
}
</script>

<style scoped>
.card-header {
  font-size: 20px;
  margin-right: 10px;
}
.el-tooltip__popper {
  padding: 20px 20px;
  font-size: 55px;
}
</style>
