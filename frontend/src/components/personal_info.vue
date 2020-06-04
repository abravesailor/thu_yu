<template id="parent">
    <div class="fuc">
      <div id='header'>
        <header-bar v-bind:msbm-seen='msbm' v-bind:fbms-seen='fbms' v-bind:tsxx-seen='tsxx' v-bind:msxxgl-seen='msxxgl' v-bind:qxgl-seen='qxgl'  v-bind:my-message='mess'></header-bar>
      </div>

      <div class="personal_information" id="personal">
          <div class="showing" id="showpage">
            <person v-if="type == 'person_seen'"></person>
            <changepw v-if="type == 'person_pw'"></changepw>
            <author v-if="type == 'author'"></author>
            <admi v-if="type == 'adi'"></admi>
            <lookup v-if="type == 'lookup'"></lookup>
          </div>

          <div class="toolbar">
            <el-menu default-active="1-1" class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
              <el-submenu index="1">
                <template slot="title">
                  <i class="el-icon-menu"></i>
                  <span>个人信息</span>
                </template>
                <el-menu-item-group>
                  <el-menu-item index="1-1" @click="per">个人信息</el-menu-item>
                  <el-menu-item index="1-2" @click="pw">修改密码</el-menu-item>
                  <el-menu-item index="1-3" @click="mpi">修改个人信息</el-menu-item>
                </el-menu-item-group>
              </el-submenu>
              <el-menu-item index="2" @click="ats" v-if="(auth == 'topAdministrator') || (start)">
                <i class="el-icon-setting"></i>
                <span slot="title">队伍管理员权限授予</span>
              </el-menu-item>
              <el-menu-item index="3" @click="ads" v-if="(auth == 'topAdministrator') || (start)">
                <i class="el-icon-document"></i>
                <span slot="title">录取表单</span>
              </el-menu-item>
              <el-menu-item index="4" @click="lop">
                <i class="el-icon-info"></i>
                <span slot="title">队伍成员管理</span>
              </el-menu-item>
            </el-menu>
          </div>
      </div>
    </div>
</template>

<script>
import headerBar from './HeaderBar.vue'
import person from './person.vue'
import passw from './changepassword.vue'
import at from './authority.vue'
import adm from './Admissions.vue'
import lop from './lookup.vue'
export default {
  name: 'personal',
  components: {
    'header-bar': headerBar,
    'person': person,
    'changepw': passw,
    'author': at,
    'admi': adm,
    'lookup': lop
  },
  data () {
    return {
      type: 'person_seen',
      start: false,
      auth: window.sessionStorage.auth
    }
  },
  created () {
    if (!window.sessionStorage.login) {
      this.$router.push('/')
    }
  },
  methods: {
    per: function () {
      this.type = 'person_seen'
    },
    pw: function () {
      this.type = 'person_pw'
    },
    mpi: function () {
      this.$router.push('/modify')
    },
    ats: function () {
      this.type = 'author'
    },
    ads: function () {
      this.type = 'adi'
    },
    lop: function () {
      this.type = 'lookup'
    }
  }
}
</script>

<style scoped>
label{
  font-size: 18px;
}
.fuc{
  height: 100%;
}
.personal_information{
  position: relative;
  height: 100%;
  width: 100%;
  background-color:#ffffff;
  display: inline-block;
}
.showing{
  position: relative;
  float: right;
  height: 100%;
  width: 85%;
  z-index: 100;
  background-color: #f5f5f5;
}
.showbox{
  float: left;
  margin-top: 5%;
  margin-left: 10%;
  height: 10%;
  width: 40%;
}
.toolbar{
  position: relative;
  display: inline-block;
  height: 100%;
  width: 15%;
  z-index: 992;
  background-color:#545c64;
  box-shadow: 1px 1px 1px #d4d4d4;
}
.toolele{
  position: relative;
  margin-top: 0%;
  margin-left:0%;
  height: 10%;
  width: 100%;
  z-index: 991;
}
.elename{
  position: relative;
  margin-top: 1%;
  height: 98%;
  width: 100%;
  border: none;
  background-color: #fafaf3;
  text-shadow: 1px 1px 1px rgba(0,0,0,.2);
}
</style>
