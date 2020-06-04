<template>
    <div class = "tst">
      <span v-html="msg"></span>
      <br />
      <input v-model="msg" />
      <br /><br /><br />
      <span v-if="see" v-on:click="tap">现在你能看到我了</span>
    </div>
</template>

<script>
export default {
  name: 'hello',
  data () {
    return {
      msg: '<h1>Hello World</h1>',
      see: true
    }
  },
  methods: {
    tap: function () {
      alert('csdjsj')
    }
  }
}
</script>
