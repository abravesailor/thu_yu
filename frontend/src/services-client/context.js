
class Context {
  constructor (url, keys, io) {
    this.url = url
    this.io = io
    this.keys = keys
    this.vm = null
    this.socket = null
    this.userId = 1
    this.name = '客户端注册'
    this.roomInfo = null
    this.groupid = 5
  }
  createIo (vm, callback, groupid) {
    this.vm = vm
    
    let socket = this.io.connect(this.url)
    let self = this;
    this.socket = socket
    var tmpgroupid = groupid;
    console.log("yijinglianjie")
    console.log(this.keys)
    socket.on("sendSuccess", function() {
      console.log("shoudaosuccess")
      console.log(tmpgroupid)
      socket.emit("getGroupid", tmpgroupid)
      console.log(self.keys.emit);
      socket.on(self.keys.emit.sendRooms, function (roomInfo) {
        self.roomInfo = roomInfo
        callback(roomInfo)
      })

    })
    
    
  }
  registerUser (id, name) {
    console.log("aaaaa")
    console.log(id)
    console.log(name)
    console.log(this.keys)

    this.userId = id
    this.name = name
    this.socket.emit(this.keys.client.registerUser, this.userId, this.name)
  }
  newUser (callback) {
    this.socket.on(this.keys.emit.newUser, callback)
  }
  sendMsg (msg) {
    console.log("sendsth")
    this.socket.emit(this.keys.client.newMsg, msg)
  }
  reciveMsg (callback) {
    this.socket.on(this.keys.emit.notifyMsg, function (msg) {
      console.log("receivesth")
      callback(msg)
    })
  }
  closeConn () {
    this.socket.emit(this.keys.client.closeConn)
  }
  refUsers (callback) {
    this.socket.on(this.keys.emit.refUsers, function (users) {
      callback(users)
    })
  }
}
export default Context
