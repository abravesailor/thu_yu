<template>
  <el-container>
    <el-header><bar></bar></el-header>
    <el-container>
    <el-aside width="200px">Aside</el-aside>
    <el-main>
      <main></main>
    </el-main>
    </el-container>
  </el-container>
</template>


<script >
  import bar from './bar'
  import main from './signupbox'
export default {
  name: 'container',
  components: {
    bar,
    main
  }
}

</script>

<style>
  .el-header{
    background-color: #545c64;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  
  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }
  
</style>