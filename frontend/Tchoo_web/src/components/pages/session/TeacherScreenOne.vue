<script setup>
import Gear from "@/components/Gear.vue";
import head from "@/components/Header.vue";
import timer from "@/components/Timer.vue";
const components = {
  Gear,
  head,
  timer
};
</script>

<template>
  <hr >
  <div class="title">
    <h1>Session 1</h1>
  </div>
  <hr >

  <div class="container">
    <table>
      <tbody>
        <!-- Table 1 -->
        <tr v-for="i in 20"
            :key="i"
        >
          <td>student name {{ i }}</td>
          <td>answers</td>
        </tr>
      </tbody>
    </table>

    <table>
      <tbody>
        <!-- Table 2 -->
        <tr v-for="i in 20"
            :key="i"
        >
          <td>student name {{ i + 20 }}</td>
          <td>answers</td>
        </tr>
      </tbody>
    </table>

    <table>
      <tbody>
        <!-- Table 3 -->
        <tr v-for="i in 20"
            :key="i"
        >
          <td>student name {{ i + 40 }}</td>
          <td>answers</td>
        </tr>
      </tbody>
    </table>

    <table>
      <tbody>
        <!-- Table 4 -->
        <tr v-for="i in 20"
            :key="i"
        >
          <td>student name {{ i + 60 }}</td>
          <td>answers</td>
        </tr>
      </tbody>
    </table>
  </div>
  <timer />

  <Gear />
</template>

<style scoped>
.title {
  display: flex;
  flex-direction: initial;
  justify-content: center;
  align-items: center;
  text-align: center;
  font-size: smaller;
}

hr {
  width: 100%;
  margin: 0 auto;
}

.container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  text-align: center;
}

table {
  border-collapse: collapse;
  border-right: 1px solid black;
  margin: 10px auto;
}

tbody {
  padding: 50px;
}

td {
  padding: 10px;
}

td:last-child {
  background-color: #ffffff9d;
  /* padding-right: 50px; */
}


</style>
