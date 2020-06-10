import Vuex from 'vuex'
import Vue from 'vue'

import RoomViewCxt from './room/roomViewCxt'
import UserViexCxt from './userViewCxt'
import MsgViewCxt from './msg/msgViewCxt'
import BusCxt from './indexForBus'



let _busCxt = new BusCxt()

let _rvCxt = new RoomViewCxt()
let _uvCxt = new UserViexCxt(_busCxt.userCxt)
let _mvCxt = new MsgViewCxt()

console.log("laiguozhelizhihou")


let opt = {
  state: {collapsed: false, topNavState: 'home', leftNavState: 'home', isteacher: false},
  getters: null,
  mutations: null,
  actions: null
}

/*
const date = 'Mon Mar 24 2018 00:00:00 GMT+0800 (中国标准时间)'
const data = [
  {
    id: '1111',
    name: 'Allen',
    type: '员工',
    status: '已离职'
  },{
    id: '2222',
    name: 'Thomas',
    type: '司机',
    status: '在职'
  }
]

for(var item in opt) {
  localStorage.getItem(item)? opt[item] = JSON.parse(localStorage.getItem(item)): false;
}
*/
_rvCxt.use(opt)
_uvCxt.use(opt)
_mvCxt.use(opt)

Vue.use(Vuex)

let store = new Vuex.Store(opt)
console.log(_busCxt)
export default store
export const busCxt = _busCxt /** 业务处理上下文 */
export function getBusCxt () {
  return _busCxt
}
