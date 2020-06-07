<template>
  <div>
    <h1>{{ msg }}</h1>
    <input v-model="a">
    <input v-model="b">
    <br>
    {{gcd}}
  </div>
</template>

<script>
export default {
  data () {
    return {
      a: 5,
      b: 21,
      msg: 'test page'
    }
  },

  computed: {
    gcd () {
      function f (x, y) {
        if (!y) return x
        return f(y, x % y)
      }
      if (!/^([1-9]+\d*|0)$/.test(this.a) || !/^([1-9]+\d*|0)$/.test(this.b)) {
        return 'syntax error'
      }
      const a = parseInt(this.a)
      const b = parseInt(this.b)
      return f(a, b)
    }
  }
}
</script>
