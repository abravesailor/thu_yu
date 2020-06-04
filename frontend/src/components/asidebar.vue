<template>
<el-menu
      default-active="activeIndex2"
      class="el-menu-vertical-demo"
      @select="handleSelect"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b">
      <el-menu-item index="1">
        <i class="el-icon-menu"></i>
        <span slot="title">课程公告</span>
      </el-menu-item>
      <el-menu-item index="2">
        <i class="el-icon-folder"></i>
        <span slot="title">课程文件</span>
      </el-menu-item>
      <el-menu-item index="3">
        <i class="el-icon-user"></i>
        <span slot="title">课程成员</span>
      </el-menu-item>
      <el-menu-item index="4">
        <i class="el-icon-user-solid"></i>
        <span slot="title">小组讨论</span>
      </el-menu-item>
      <el-menu-item index="5">
        <i class="el-icon-folder-opened"></i>
        <span slot="title">小组文件</span>
      </el-menu-item>
    </el-menu>
</template>

<script>
  export default {
    data() {
      return {
        activeIndex: '1',
        activeIndex2: '1'
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>