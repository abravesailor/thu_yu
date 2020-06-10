<template>
    <div class="wrap">
        <div class="wrap-main">
            <div class="msg-list" id="scrolltest" style="overflow: auto">
                <MsgList>
                </MsgList>
            </div>
            <div class="msg-input">
                <MsgWr @submit-add="newadd">
                </MsgWr>
            </div>
        </div>
    </div>
</template>
<script>
  import MsgList from './Message/MsgList'
  import MsgWr from './Message/MsgWriter'
  import { mapGetters } from 'vuex'
  import { Keys } from '../uitls'
  import { getCxt } from '../services-client'
  import * as stores from '../store'
  let getUsers = Keys.GETUSERS
  import { getBusCxt } from '../store'
  let currRoom = Keys.GETROOMINFO
  let initRoomInfo = Keys.SETROOMINFO
  let recKey = Keys.GETNEWMSG

  export default {
    name: 'HChat',
    components: {
      MsgList,
      MsgWr
    },
    data() {
      return {
        username: window.sessionStorage.login
      }
    },
    computed: {
      ...mapGetters([getUsers]),
      ...mapGetters([currRoom]),
      ...mapGetters([recKey]),
      msg() {
            console.log("GNMchange");
            this.$nextTick(function(){
                var div = document.getElementById('scrolltest');
                div.scrollTop = div.scrollHeight;
                
            });
            return this.getNewMsg.length;
      }
    },
    methods:{
      newadd: function(val)
      {
        console.log("shoudaole");
        //$("div").scrollTop(10000);
        //var div = docck();ument.getElementById('msg_end');
        //div.cli
        //div.scrollTop = 1000000;
        this.$nextTick(function(){
        var div = document.getElementById('scrolltest');
        div.scrollTop = div.scrollHeight;
        })
      },

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
    },

    created() {
      
      
    },

    destroyed()
    {
      console.log("logout");
      //getBusCxt().userCxt.closeConn();
    }

  
  }
</script>
<style lang="scss" scoped >
    $left-width: 20px;
    $msg-list-height:450px;
    $msg-input-height:120px;
    $msg-border: 10px solid #58B7FF;
    $msg-radius:5px;

    .wrap{
        height:100%;
    }
    .wrap-main{ 
        float:left;
        padding-left: $left-width;
        height:100%;
        width:750px; /*因为float了，必须要有width，否则宽度为0px*/
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