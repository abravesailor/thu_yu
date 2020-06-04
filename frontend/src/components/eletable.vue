<template>
  <el-table
    :data="tableData"
    border
    stripe
    style="width: 100%">
    <el-table-column
      prop="date"
      label="日期"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      prop="name"
      label="姓名"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      prop="province"
      label="省份"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      prop="city"
      label="市区"
      align = "center"
      width="200">
    </el-table-column>
    <el-table-column
      prop="address"
      label="地址"
      align = "center"
      width="300">
    </el-table-column>
    <el-table-column
      prop="zip"
      label="邮编"
      align = "center"
      width="120">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作"
      width="100">
      <template slot-scope="scope">
        <el-button @click="handleClick(scope.row)" type="text" size="medium">{{tableData[scope.$index].date}}</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
  export default {
    methods: {
      handleClick(row) {
        console.log(row);
      }
    },

    data() {
      return {
        tableData: [{
          date: '2016-05-02',
          name: '王小虎',
          province: '上海',
          city: '普陀区',
          address: '上海市普陀区金沙江路 1518 弄',
          zip: 200333
        }, {
          date: '2016-05-04',
          name: '王小虎',
          province: '上海',
          city: '普陀区',
          address: '上海市普陀区金沙江路 1517 弄',
          zip: 200333
        }, {
          date: '2016-05-01',
          name: '王小虎',
          province: '上海',
          city: '普陀区',
          address: '上海市普陀区金沙江路 1519 弄',
          zip: 200333
        }, {
          date: '2016-05-03',
          name: '王小虎',
          province: '上海',
          city: '普陀区',
          address: '上海市普陀区金沙江路 1516 弄',
          zip: 200333
        }]
      }
    }
  }
</script>