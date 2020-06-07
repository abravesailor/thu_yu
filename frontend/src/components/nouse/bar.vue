<template>
<el-menu
  :default-active="activeIndex2"
  class="el-menu-demo"
  mode="horizontal"
  @select="handleSelect"
  background-color="#545c64"
  text-color="#fff"
  active-text-color="#ffd04b">
  <el-menu-item index="1">课程列表</el-menu-item>
  <el-menu-item index="2">个人信息</el-menu-item>
  <el-menu-item index="3" >修改密码</el-menu-item>
  <el-menu-item index="4">退出登录</el-menu-item>
</el-menu>
</template>

<script>
  export default {
    data() {
      return {
        activeIndex: '1',
      };
    },
    props: ['activeIndex2'],
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>