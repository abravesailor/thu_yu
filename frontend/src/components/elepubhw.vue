<template>
    <div>
        <div class="register-container" id="register-form">
            <h3 class="title" >发布作业</h3>
              <el-form :model="ruleForm" :rules="rules" label-position="right" ref="ruleForm" label-width="150px" class="demo-ruleForm">
                <div class="leftbox">
                  <el-form-item label="作业标题" prop="title">
                    <el-input v-model="ruleForm.title"></el-input>
                  </el-form-item>
                  <el-form-item label="作业描述" prop="txt">
                    <el-input type="textarea" :rows="5" v-model="ruleForm.txt" placeholder="请输入作业描述"></el-input>
                  </el-form-item>

                  <el-form-item label="作业截止日期" required prop="ddl">
                <el-date-picker
                    size="small"
                    v-model="ruleForm.ddl"
                    type="date"
                    value-format="yyyy-MM-dd"
                ></el-date-picker>
                </el-form-item>

                <el-form-item label="是否允许同时检查" prop="sep">
                <el-switch v-model="ruleForm.sep"></el-switch>
                </el-form-item>
                
                <div v-for="(domain, index) in ruleForm.domains" :key="index">
                <el-form-item
                  :label="'时间段' + (index+1) + '选择日期'"
                  :prop="'domains.'+index+'.date'"
                  :rules="rules.date"
                  >
                    <el-date-picker
                      size="medium"
                      v-model="domain.date"
                      type="date"
                      placeholder="选择日期"
                      value-format="yyyy-MM-dd"
                      :picker-options="pickerOptions">
                    </el-date-picker>
                  </el-form-item>
                  <el-form-item
                    :label="'时间段' + (index+1) + '选择时间'"
                    :prop="'domains.'+index+'.time'"
                    :rules="rules.time"
                    >
                    <el-time-picker
                      size="medium"
                      is-range
                      align="left"
                      v-model="domain.time"
                      range-separator="至"
                      start-placeholder="选择起始时间"
                      end-placeholder="结束时间"
                      value-format="HH:mm"
                      format="HH:mm"
                      placeholder="选择时间范围">

                    </el-time-picker>
                  </el-form-item>
                  <el-form-item
                  :label="'时间段' + (index+1) + '限选人数'"
                  :prop="'domains.'+index+'.cnt'"
                  :rules="rules.cnt"
                  >
                    <el-input v-model.number="domain.cnt" placeholder="输入该时段最大限选人数"></el-input>
                  </el-form-item>
                  <el-form-item>
                  <el-button @click.prevent="removeDomain(domain)" :disabled="onlyone">删除时间段{{index+1}}</el-button>
                </el-form-item>

                </div class="lastpart">
                  <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')">发布作业</el-button>
                    <el-button @click="addDomain">新增时间段</el-button>
                    <el-button @click="resetForm('ruleForm')">重置</el-button>
                    <el-button @click="goback()">返回</el-button>
                  </el-form-item>
                </div>
              </el-form>
        </div>
    </div>
</template>

<script>
// import headerBar from './HeaderBar.vue'
import ident from './ident.vue'
import $ from 'jquery'
export default {
  name: 'Home',
  components: {
    //'header-bar': headerBar,
    'ide': ident
  },
  data () {
    return {
      seen: '',
      identifyCode: '',
      ruleForm: {
        title: '',
        txt: '',
        ddl: '',
        sep: true,
        domains: [{
            date: '',
            starttime: '',
            endtime: '',
            time: '',
            cnt: ''
          }],
      },
      pickerOptions: {
          disabledDate(time) {
            return time.getTime() <= Date.now();
          },
        },
      rules: {
        title: [
          { required: true, message: '请输入公告标题', trigger: 'blur' },
          {max: 15, message: '长度不超过 15 个字符', trigger: 'blur'}
        ],
        txt: [
          { required: true, message: '请输入公告内容', trigger: 'blur' },
          {max: 300, message: '长度不超过 300 个字符', trigger: 'blur'}
        ],
        ddl: [
          {required: true, message: '请选择作业截止时间', trigger: "blur"}
        ],
        date: [
          {required: true, message: '请选择时间段日期', trigger: "blur"}
        ],
        time: [
          {required: true, message: '请选择时间段时间', trigger: "blur"}
        ],
        cnt: [
          { required: true, message: '最大限选人数不能为空'},
          { pattern: /^([1-9]\d{0,3}|1000)$/, message: '请输入1-10000内的正整数' }
        ]
      }
    }
  },
  computed:{
    onlyone: function()
    {
      if (this.ruleForm.domains.length == 1) return true;
      else return false;
    }
  },
  created () {
    //this.refresh()
  },
  methods: {
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    goback ()
    {
      var url = this.$route.path;
      var px = url.lastIndexOf('/');
      var newurl = url.substr(0, px) + "/hw";
      this.$router.push(newurl);
    },
    removeDomain(item) {
        var index = this.ruleForm.domains.indexOf(item)
        if (index !== -1) {
          this.ruleForm.domains.splice(index, 1)
        }
      },
      addDomain() {
        this.ruleForm.domains.push({
          value: '',
          key: Date.now()
        });
      },
    submitForm: function (formName) {

      var _this = this
      function GetJsonData () {
        var json = {
          'title': _this.ruleForm.title,
          'context': _this.ruleForm.txt,
          'username': window.sessionStorage.login,
          'classid': _this.$route.params.classid,
          'permission': '',
          'ddl': String(_this.ruleForm.ddl),
          'list': []

        }
        if (_this.ruleForm.sep) json.permission = 'yes';
        else  json.permission = 'no';
        for (var i  = 0; i < _this.ruleForm.domains.length; i++)
        {
          var js = {
            'starttime': String(_this.ruleForm.domains[i].date) + ' ' + String(_this.ruleForm.domains[i].time[0]),
            'endtime': String(_this.ruleForm.domains[i].date) + ' ' + String(_this.ruleForm.domains[i].time[1]),
            'cnt': _this.ruleForm.domains[i].cnt
          }
          json.list.push(js);
        }
        json.list = JSON.stringify(json.list);
        console.log(json);
        return json
      }
      var gks = 0
      this.$refs[formName].validate((valid) => {
        if (valid) {
          gks = 1
        } else {
          _this.$notify({
            title: '提示',
            message: '请正确填写内容'
          })
        }
      })
      if (gks === 1) {
        $.ajax({
          type: 'post',
          url: '/api/assignment_distribute_ajax',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(GetJsonData()),
          dataType: 'json',
          success: function (data) {
            if (data.status === 'success') {
              var ses = window.sessionStorage
              
              //console.log("regsuccess");
              _this.$alert('作业发布成功！', '发布成功', {
                  confirmButtonText: '确定',
                  callback: action => {
                 }
                });
              _this.goback();
            } else {
                _this.$notify({
                  title: '提示',
                  message: '后台错误！'
                })
              }
          },
          error: function (data) {
            _this.$notify({
              title: '提示',
              message: '网络链接失败！'
            })
          }
        })
      }
    }
  }
}
</script>

<style scoped>
label{
  font-weight: 500;
}
.register-container{
  width:100%;
  position: relative;
  z-index: 99;
  background:#f4f4f4;
  display: inline-block;
}
.title{
  position: relative;
  margin-left: 13.6%;
  margin-top: 2%;
  text-align: left;
  color: #444;
  height: 9%;
  width: 80%;
  padding: 2px 0 3px 20px;
  border-left: 7px solid #08c;
}
.leftbox{
  position: relative;
  float: left;
  height: 400px;
  margin-left: 10%;
  width: 70%;
}
.rightbox{
  position: relative;
  float: right;
  height: 400px;
  width: 38.5%;
  margin-right: 10%;
}
.confirmimg{
  position: absolute;
  height: 100%;
  width: 18%;
  float: left;
  z-index: 999;
  margin-left: 80%;
}
.sepp{
  margin-left: 30px;
}
.submit{
  background-color: #08d;
  margin-left:55.7%;
  height: 9%;
  width: 10%;
  font-size: 18px;
  color: #fff;
  border: none;
  border-radius: 3px;
  overflow: hidden;
}
.lastpart{
  margin-bottom: 20px;
}
</style>
