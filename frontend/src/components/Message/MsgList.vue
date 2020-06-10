<template> 
    <div>
        <div class="loading" v-if="getNewMsg.length==0 && dataArray.length==0">
                <div style="margin-top: 300px;text-align:center; font-size: 16px;">
                    <span>未查找到聊天记录</span>
                </div>
            </div>

        
        <ul class="msg-cont">
            <li v-for="item in dataArray"  v-bind:class="{ 'msg-cont-send' : item.direction == 'send' }" >
                <p class="time"> <span v-text="item.time"></span> </p>
                <span class="msg-cont-item" >{{item.userName}}: {{item.cont}}</span>
            </li>
            <li v-for="item in getNewMsg"  v-bind:class="{ 'msg-cont-send' : item.direction == 'send' }" >
                <p class="time"> <span v-text="item.time"></span> </p>
                <span class="msg-cont-item" >{{item.userName}}: {{item.cont}}</span>
            </li>
            
        </ul>
    </div>
</template>
<script>
  import { mapGetters } from 'vuex'
  import { Keys } from '../../uitls'
  let recKey = Keys.GETNEWMSG
  import { getCxt } from '../../services-client'
  import * as stores from '../../store'
  let getUsers = Keys.GETUSERS
  import { getBusCxt } from '../../store'
  let currRoom = Keys.GETROOMINFO
  let initRoomInfo = Keys.SETROOMINFO

  export default{
    name: 'MsgList',
    computed: {
      ...mapGetters([recKey]),
      msg() {
                console.log(this.getNewMsg);
                return this.getNewMsg.length;
            },
    },

    data() {
            return {
                isUpperLaoding: false,
                isUnderLaoding: false,

                isRefreshedAll: false,
                isLoadedAll: false,
                
                //minHeight: 700,
                dataArray: [],
                groupid: 0,
                username: window.sessionStorage.login
            }
        },

    methods: {

    goback ()
    {
      var url = this.$route.path;
      var px = url.lastIndexOf('/');
      var newurl = url.substr(0, px) + "/msglist";
      this.$router.push(newurl);
    },

            getInfo() {

                var self = this
                $.ajax({
                    type: 'post',
                    url: '/api/chat_record_ajax',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify({username: window.sessionStorage.login, lessonname: this.$route.params.classid}),
                    dataType: 'json',
                    success: function (data) {

                        self.dataArray = data.chatlist;
                        self.groupid = data.group_id;
                        window.sessionStorage.setItem('groupid', data.group_id);
                        let tmpid = data.group_id

                        console.log(tmpid);

                        if (typeof(tmpid) == "undefined")
                        {
                            console.log("entered");

                            self.$alert('该学生未被分组，无法进入小组讨论', '错误！', {
                                confirmButtonText: '确定',
                                callback: action => {
                            }
                            });
                    
                            self.goback();
                        }

                        getCxt().createIo(self, function (roomInfo) {
                            stores.busCxt.init() 
                            self.$store.dispatch(initRoomInfo, roomInfo)
                            getCxt().refUsers(function (users) {
                            stores.busCxt.userCxt.refUsers(users)
                            });
        
                            getBusCxt().userCxt.registerUser(self.username, self.username)
                        }, tmpid)


                    },
                    error: function (data) {
                    self.$notify({
                        title: '提示',
                        message: '网络链接失败！'
                    })
                    }
                })
                console.log("thisgroupid")
                console.log(self.groupid);

            }
    },
    created() {
        this.getInfo();


        
    }
  }
</script>
<style scoped >
    .msg-cont{
        list-style-type: none;
        margin: 0px;
        padding: 0px;
    }
    .msg-cont > li{
        margin: 0px;
        padding: 5px;
    }
    .msg-cont-item{
        /*background: #8492A6;
        padding: 5px 10px; 
        border-radius: 2px;*/
        display: inline-block;
        position: relative;
        padding: 0 10px;
        max-width: calc(100% - 75px);
        min-height: 35px;
        line-height: 2.1;
        font-size: 15px;
        padding: 6px 10px;
        text-align: left;
        word-break: break-all;
        background-color: #fff;
        color: #000;
        border-radius: 4px;
        box-shadow: 0px 1px 7px -5px #000;
    }
    .msg-cont-receive{
        text-align: left;
    }
    .msg-cont-send{
        text-align: right;
        
    }
    .msg-cont-send .msg-cont-item{
        background-color: #9EEA6A;
    }
    .time {
        margin: 10px 0;
        text-align: center;
    }
    .time>span {
        display: inline-block;
        padding: 0 5px;
        font-size: 12px;
        color: #fff;
        border-radius: 2px;
        background-color: #DADADA;
    }
</style>