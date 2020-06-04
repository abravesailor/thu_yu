<template>
    <div class="wrap">
        <div class="wrap-main">
            <div class="msg-list">
                <MsgList 
                :getUpperData="getUpperData"
                :getUnderData="getUnderData">
                </MsgList>
            </div>
            <div class="msg-input">
                <MsgWr/>
            </div>
        </div>
        <div class="wrap-left">
            <ul class="list-group" >
                <li class="list-group-item" v-for=" user in getUsers" >
                    {{user.name}}
                </li>
            </ul>
        </div>
    </div>
</template>
<script>
  import MsgList from './Message/MsgList'
  import MsgWr from './Message/MsgWriter'
  import { mapGetters } from 'vuex'
  import { Keys } from '../uitls'
  let getUsers = Keys.GETUSERS

  export default {
    name: 'HChat',
    components: {
      MsgList,
      MsgWr
    },
    computed: {
      ...mapGetters([getUsers])
    },
    methods:{
    //向上滚动加载数据
    getUpperData(){
      var me = this;
      
      // 这里为模拟异步加载数据
      // 实际上你可能要这么写:
      // return axios.get('xxx').then(function(result){
      //     return result;  //result的格式需要类似下面resolve里面的数组
      // })
      return new Promise(function(resolve){
        setTimeout(function(){
           //模拟加载完毕
          if(me.upperTimes>3){
            return resolve([]);
          }
          
          //加载数据
          resolve([{
              direction: 2,
              id: me.upperId-1,
              type: 1,
              content: '向上滚动加载第 ' + me.upperTimes +' 条！',
              ctime: new Date().toLocaleString()
            },
            {
              direction: 1,
              id: me.upperId-2,
              type: 1,
              content: '向上滚动加载第 ' + me.upperTimes +' 条！',
              ctime: new Date().toLocaleString()
            }]
      
          )
        }, 1000);
        me.upperId= me.upperId+2;
        me.upperTimes++;
      })
    },

    getUnderData(){
      var me = this;

      //意义同getUpperData()
      return new Promise(function(resolve){
        setTimeout(function(){
          //模拟加载完毕
          if(me.underTimes>3){
            return resolve([]);
          }
          
          //加载数据
          resolve(
            [{
              direction: 1,
              id: me.underId+1,
              type: 1,
              content: '向下滚动加载第 ' + me.underTimes +' 条！',
              ctime: new Date().toLocaleString()
            },
            {
              direction: 2,
              id: me.underId+2,
              type: 1,
              content: '向下滚动加载第 ' + me.underTimes +' 条！',
              ctime: new Date().toLocaleString()
            }]
          )
        }, 1000);

        me.underId = me.underId+2;
        me.underTimes++;
      })
    }
    }

  
  }
</script>
<style lang="scss" scoped >
    $left-width: 200px;
    $msg-list-height:80%;
    $msg-input-height:20%;
    $msg-border: 10px solid #58B7FF;
    $msg-radius:5px;

    .wrap{
        height:100%;
    }
    .wrap-left{ 
        width: $left-width; 
        float:left;
        height:100%;  
        margin-left: -100%;
        background: linear-gradient(#20A0FF,#58B7FF);
    }
    .wrap-main{ 
        float:left;
        padding-left: $left-width;
        height:100%;
        width:100%; /*因为float了，必须要有width，否则宽度为0px*/
        text-align:left;
    }
    .msg-list{
        height: $msg-list-height;
        border: $msg-border; 
    }
    .msg-input{
        height: $msg-input-height;
        border: $msg-border; 
    }
</style>