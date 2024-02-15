<script setup>
import Gear from "@/components/Gear.vue";
import head from "@/components/Header.vue";
import timer from "@/components/Timer.vue";
const components = {
  Gear,
  head,
  timer,
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
        <tr v-for="i in 50"
            :key="i"
        >
          <td>student name {{ i }}</td>
          <td>
            porro tenetur provident consequatur, vero temporibus! Sapiente
            libero fugit delectus ad expedita explicabo, quis recusandae
            corporis saepe rerum numquam dignissimos exercitationem aperiam rem.
          </td>
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
  margin: 10px auto;
}

tbody {
  padding: 50px;
}

td {
  padding: 10px;
}

td:first-child {
  border-right: 1px solid black;
}

tr:nth-child(even){
  background-color: rgba(168, 175, 190, 0.74);
}
</style>
