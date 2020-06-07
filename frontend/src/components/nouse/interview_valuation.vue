<template>
  <el-container>
    <el-header style="padding:0px;" height="50px">
      <header-bar style="margin:0px" v-bind:msbm-seen='msbm' v-bind:fbms-seen='fbms' v-bind:tsxx-seen='tsxx' v-bind:msxxgl-seen='msxxgl' v-bind:qxgl-seen='qxgl'  v-bind:my-message='mess'></header-bar>
    </el-header>
    <el-container style="background:#fcfcfc">
      <el-aside height="100%" style="background:#fefefe">
        <el-menu class="el-menu-vertical-demo" unique-opened>
          <el-submenu index="1">
            <template slot="title"><i class="el-icon-view"></i>当前面试</template>
            <el-menu-item v-for="(item, index) in activeIntvs" :key="index" :index="index+''" style="padding-right:10px;" @click="switchIntv(item.id)">
              <span class="nav_intvteam"><i class="el-icon-time"></i>{{item.team}}</span>
              <span class="nav_intvtime">{{item.time}}</span>
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main style="padding:0px">
        <intvtable :intv="currentIntv"></intvtable>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import headerBar from './HeaderBar.vue'
import intvTable from './interview_table.vue'
import $ from 'jquery/dist/jquery.min.js'
export default {
  name: 'intvValuation',
  components: {
    'header-bar': headerBar,
    'intvtable': intvTable
  },
  data () {
    return {
      activeIntvs: [
        {team: '军乐团', time: '15:00 Mon. Nov 1, 2018', id: 'intv1'},
        {team: '国标队', time: '15:00 Mon. Nov 1, 2018', id: 'intv2'}
      ],
      currentIntv: ''
    }
  },
  created: function () {
    if (!window.sessionStorage.login) {
      this.$router.push('/')
    } else {
      this.fetchIntv()
    }
  },
  methods: {
    switchIntv: function (newid) {
      this.currentIntv = newid
      console.log(this.currentIntv)
    },
    fetchIntv: function () {
      let self = this
      $.ajax({
        type: 'post',
        url: '/api/activeintv_ajax',
        contentType: 'application/json; charset=utf-8',
        data: '',
        dataType: 'json',
        success: function (data) {
          if (data.status === 'success') {
            self.activeIntvs = data.activeIntvs
          } else {
            self.$message({message: 'Oops...获取面试失败', type: 'error'})
          }
        },
        error: function (data) {
          self.$message({message: '获取面试失败', type: 'error'})
        }
      })
    }
  }
}
</script>

<style scoped>
.nav_intvteam {
  float: left;
}
.nav_intvtime {
  color:darkgray;
  float: right;
}
.el-container, .el-menu {
  height: 100%;
}
.el-menu {
  height: 100%;
}
</style>
