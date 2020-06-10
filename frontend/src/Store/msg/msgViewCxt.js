import * as uitls from '../../uitls'
class MsgViewCxt {
  use (store) {
    this.initStore(store)
  }
  initStore (store) {
    let state = {
      msgs: []
    }
    let getters = {
      [uitls.Keys.GETNEWMSG]: function (argState) {
        return argState.msgs
      }
    }
    let mutations = {
      [uitls.Keys.ADDMSG]: function (argState, msg) {
        console.log("addmsg")
        argState.msgs.push(msg)
      }
    }
    let actions = {
      [uitls.Keys.ADDMSG]: function (dis, msg) {
        var date=new Date();   
        var year=String(date.getFullYear()); //获取当前年份   
        var month=String(date.getMonth()+1); //获取当前月份   
        var dat=date.getDate(); //获取当前日   
        var hour=String(date.getHours()); //获取小时   
        var minutes=String(date.getMinutes()); //获取分钟   
        var tme = year + '-';
        if (month.length != 2) tme = tme + '0';
        tme = tme + month + '-' + dat + ' ';
        if (hour.length != 2) tme = tme + '0';
        tme = tme + hour + ':';
        if (minutes.length != 2) tme = tme + '0';
        tme = tme + minutes;
        var newmsg = msg;
        msg.time = tme;

        dis.commit(uitls.Keys.ADDMSG, newmsg)
      }
    }
    store.state = uitls.merge(store.state, state)
    store.getters = uitls.merge(store.getters, getters)
    store.mutations = uitls.merge(store.mutations, mutations)
    store.actions = uitls.merge(store.actions, actions)
  }
}

export default MsgViewCxt
