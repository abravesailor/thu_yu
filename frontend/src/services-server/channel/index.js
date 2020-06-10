class Channel {
  constructor (id, socket, cxt) {
    this.socket = socket
    this.id = id
    this.user = null
    this.cxt = cxt
    this.room = null,
    this.groupid = 0
  }
  static createChannel (id, socket, cxt) {
    return new Channel(id, socket, cxt)
  }
  setUser (user) {
    console.log(user)
    this.user = user
    this.socket.emit(this.cxt.eventKeys.emit.newUser, user)
    this.socket.to('roomId' + this.roomInfo.id).emit(this.cxt.eventKeys.emit.newUser, user)
  }
  init () {
    let tmproomInfo = this.cxt.room.collections[0];
    this.roomInfo = tmproomInfo;

    this.socket.emit("sendSuccess");
    console.log("fasongsuccess")
    let self = this
    this.socket.on("getGroupid", function(groupid){
      this.groupid = groupid
      console.log(groupid)
      let roomInfo = self.cxt.room.collections[groupid]
      self.roomInfo = roomInfo
      console.log("roomInfo")
      console.log(self.roomInfo)
      self.socket.join('roomId' + roomInfo.id)
      self.socket.emit(self.cxt.eventKeys.emit.sendRooms, roomInfo)
      self.socket.on(self.cxt.eventKeys.client.registerUser, function (id, name) {
        console.log(id + '-' + name + '--' + self.id)
        self.cxt.createUserById(id, name, self.id)
      }) /** 新用户注册 */
      self.socket.on(self.cxt.eventKeys.client.newMsg, function (msg) { /** 发送消息 */
        self.notifyMsg(msg)
        console.log(msg)
        self.cxt.addMsg(msg)
      })
      self.socket.on(self.cxt.eventKeys.client.closeConn, function () {
        console.log(self.id + '--关闭连接')
        self.cxt.remove(self)
      })
      self.sendUsers()
    })

    
  }
  notifyMsg (msg) {
    msg.direction = 'notify'
    msg.type = 1
    this.socket.to('roomId' + this.roomInfo.id).emit(this.cxt.eventKeys.emit.notifyMsg, msg)
    console.log(this.roomInfo.id + "aaa")
  }
  sendUsers () {
    this.socket.emit(this.cxt.eventKeys.emit.refUsers, this.cxt.users)
    this.socket.to('roomId' + this.roomInfo.id).emit(this.cxt.eventKeys.emit.refUsers, this.cxt.users)
  }
}
module.exports = Channel
