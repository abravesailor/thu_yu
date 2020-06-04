<template>
  <ul class="nav nav-pills">
  <li class="active"><a href="#">导航1</a></li>
  <li><a href="#">导航2</a></li>
  <li><a href="#">导航3</a></li>
  <li><a href="#">导航4</a></li>
  <li><a href="#">导航5</a></li>
  <li><a href="#">导航6</a></li>
</ul>
</template>

<script>
export default {
  name: 'headerbar',
  data () {
    return {
    }
  }
}
</script>

<style scoped>
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
