<script setup>
import {getUser,getUsersFromGroup,getGroup,deleteGroup,updateGroup,addUserToGroup,removeUserFromGroup,getUserByEmail,fetchUserInfo} from "../../lib/requests"
import { ref,onMounted } from "vue";
import {useRoute} from "vue-router";
import Header from "../Header.vue";
import router from "@/lib/router.js";
import Gear from "@/components/Gear.vue";
const route = useRoute();
const groupId = route.params.id;

const group = ref({});   
const users = ref([]); 
const email = ref("");
const creatorEmail = ref("");
const parent = ref(null);

async function onFormSubmit() {
  let statusCode;
  let json;
  [json, statusCode] = await fetchUserInfo();
  if (statusCode !== 200) {
    alert(json.detail)
  }
  email.value = json.email;
  [json, statusCode] = await getGroup(groupId);
  if (statusCode !== 200) {
    alert(json.detail)
  }
  group.value = json;
  if (group.value.parent_id != null) {
    [json, statusCode] = await getGroup(group.value.parent_id);
    if (statusCode !== 200) {
      alert(json.detail)
    }
    parent.value = group.value.parent_id;
    group.value.parent_id = json.group_name;
  }
  [json, statusCode] = await getUser(group.value.creator_id);
  if (statusCode !== 200) {
    alert(json.detail)
  }
  group.value.name = json.name;
  group.value.surname = json.surname;
  creatorEmail.value = json.email;
  [json, statusCode] = await getUsersFromGroup(groupId);
  if (statusCode !== 200) {
    alert(json.detail)
  }
  users.value = json;
  for (let i = 0; i < users.value.length; i++) {
    [json, statusCode] = await getUser(users.value[i].id);
    if (statusCode !== 200) {
      alert(json.detail)
    }
    users.value[i].name = json.name;
    users.value[i].surname = json.surname;
  }
}


onMounted(async () => {
  await onFormSubmit();

});
async function confirmDelete() {
  const result = window.confirm("êtes vous sur de vouloir supprimer ce groupe?");
  if (result) {
    for (const user of users.value){
      await removeUserFromGroup(groupId,user.id)
    }
    await deleteGroup(groupId);
  }
}


let modifyGroupName = "";

function showModifyPopup() {
  modifyGroupName = group.group_name;
  const newGroupName = prompt("Entrez le nouveau nom du groupe:", modifyGroupName);
  if (newGroupName !== null) {
    modifyGroupName = newGroupName;
    updateGroup(groupId,modifyGroupName);
  }
  else {
    alert("Modification annulée");
  }

}

async function addUser() {
  const userEmail = prompt("Entrez l'email de l'utilisateur à ajouter:");
  const userId  = await getUserByEmail(userEmail).then((response) => {return response[0].id});
  if (userEmail !== null) {
    if(parent.value != null) {
      const usersFromParent = await getUsersFromGroup(parent.value)
      for (let i = 0; i < usersFromParent.length; i++) {
        if (usersFromParent[i].email === userEmail) {
          if (response[0].id !== null) {
            addUserToGroup(groupId,response[0].id);
          }
          return;
        } else {
          
          if (userId !== null) {
            addUserToGroup(groupId,userId);
            addUserToGroup(parent,usersFromParent[i].id);
          } 
              
        }
      }
    } else {
      if (userId !== null) {
        addUserToGroup(groupId,userId);
      }
    };

  }
  else {
    alert("Ajout annulé");
  }
  window.location.reload
}

function removeUser() {
  const userEmail = prompt("Entrez l'email de l'utilisateur à supprimer:");
  if (userEmail !== null) {
    getUserByEmail(userEmail).then((response) => {
      if (response[0].id !== null) {
        removeUserFromGroup(groupId,response[0].id);
      }
      else {
        alert("Utilisateur introuvable");
      }
    });


  }
  else {
    alert("Suppression annulée");
  }
}

function isCurrentUserCreator() {
  return email.value === creatorEmail.value;
}
</script>

<template>
  <Header />
  <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
  >
  <header />
  <div class="return">
    <button class="btnReturn">
      <img
        src="@/components/icons/return.svg"
        alt="return"
        @click="router.push('/groups')"
      >
    </button>
  </div>
  <div>
    <h1>
      {{ $t ("group.name") }}:
      <!-- Nom   -->
      {{ group.group_name }}
    </h1>
    <span v-if="isCurrentUserCreator()">
      <button @click="showModifyPopup()">
        {{ $t ("group.modify") }}
        <!-- Modifier ce groupe -->
      </button>
      <button class="delete"
              @click="confirmDelete()"
      >
        {{ $t ("group.delete") }}
      <!-- Supprimer ce groupe -->
      </button>
    </span>
    <hr>
    <div
      v-if="group.group_name"
      id="group-box"
    >
      <h3>
        {{ $t ("group.owner") }}:
        <!-- Propriétaire du groupe  -->
        <i>{{ group.name }} {{ group.surname }}</i>
      </h3>
      <h3 v-if="group.parent_id">
        {{ $t ("group.parent") }}:
        <!-- Groupe parent :  -->
        {{ group.parent_id }}
      </h3>
      <p>
        {{ $t ("group.members") }}:
        <!-- Membres: -->
      </p>
      <div v-if="users.length">
        <h4 v-for="user in users"
            :key="user.id"
        >
          {{ user.name }} {{ user.surname }}
        </h4>
      </div>
      <div v-else>
        <h4>
          {{ $t ("group.noMembers") }}
          <!-- Aucun membre -->
        </h4>
      </div>
      <span v-if="isCurrentUserCreator()"
            class="members"
      >
        <button @click="addUser()">
          {{ $t ("group.addMembers") }}
          <!-- Ajouter un membre -->
        </button>
        <button class="delete"
                @click="removeUser()"
        >
          {{ $t ("group.removeMembers") }}
        <!-- Supprimer des membres -->
        </button>
      </span>
    </div>
  </div>
  <Gear />
</template>
    

  <style scoped>
  * {
    font-family: "Sofia Sans", sans-serif;
    color: var(--text-color);
    overflow-wrap: break-word;
    word-wrap: break-word;
  }

  h1,h2,h3,p {
    max-width: 80%;
    align-self: center;
    align-items: center;

  }

  template {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
  }

  #group-box {
      border-radius: 10px;
      padding: 20px;
      text-align: center;
      width: 80%;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: right;
      
  }


  button {
    border-radius: 20px;
    background-color: var(--white);
    border: 2px solid var(--main-color);
    cursor: pointer;
    margin-left: 10px;
    margin-right: 10px;
    padding: 10px;
    margin-bottom: 10px;
  }

  button:hover {
    background-color: var(--CTA-color);
    color: var(--white);
    transition: linear 0.3s;
  }

  .delete {
    background-color: var(--CTA-2-color);
    border: 2px solid var(--CTA-2-color);
    color: white;
  }

  .delete:hover {
    background-color: var(--CTA-2-hover-color);
    border: var(--CTA-2-hover-color) 2px solid;
    color: white;
    transition: linear 0.3s;
  }

  span {
    display: inline-block;
    float: right;
    margin-top: 20px;
  }

  h1 {
    display: inline-block;
    padding-left: 20px;
  }

  .members {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      width: 100%;
  }

  .members button {
      margin: 8px 20px;
  }

  .btnReturn {
    background-color: transparent;
    border: none;
    border-radius: 100%;
    cursor: pointer;
    transition: 500ms;
  }

  .btnReturn:hover {
    background-color: #17273a23;
    border-radius: 10px;
    transition: 500ms;
  }

  </style>
