<template>
	<el-container>
  	<el-header><bar></bar></el-header>
  	<el-container>
    <el-aside width="200px"><asidebar></asidebar></el-aside>
    <el-main>
      <mainpage></mainpage>
    </el-main>
  	</el-container>
	</el-container>
</template>


<script >
  import bar from './bar'
  import mainpage from './eleclasses'
  import asidebar from './asidebar'
export default {
  name: 'container',
  components: {
    bar,
    mainpage,
    asidebar
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
    background-color: #545c64;
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 50px;
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }
  
  
</style>