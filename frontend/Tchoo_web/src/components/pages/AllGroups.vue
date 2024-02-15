<script setup>
import {getAllGroups,getUser,getUsersFromGroup,getGroup,createGroup,fetchUserInfo, getUserByEmail, register, addUserToGroup} from "../../lib/requests"
import { ref,onMounted } from "vue";
import Header from "../Header.vue";
import router from "@/lib/router.js";
const email = ref("");
const groups = ref([]);
const fileInputRef = ref(null);
import Gear from "@/components/Gear.vue";

function login(a, b) {
  throw new Error("Not imlemented")
}

async function onFormSubmit() {
  let statusCode;
  let json;
  [json, statusCode] = await fetchUserInfo();
  if (statusCode !== 200) {
    alert(json.detail)
  }
  email.value = json.email;
  [json, statusCode] = await getAllGroups();
  if (statusCode !== 200) {
    alert(json.detail)
  }
  groups.value = json;
  for (let i = 0; i < groups.value.length; i++) {
    [json, statusCode] = await getUser(groups.value[i].creator_id);
    if (statusCode !== 200) {
      alert(json.detail)
    }

    groups.value[i].creator_id = json.name;
  }
  for (let i = 0; i < groups.value.length; i++) {
    [json, statusCode] = await getUsersFromGroup(groups.value[i].id);
    if (statusCode !== 200) {
      alert(json.detail)
    }
    groups.value[i].count = json.length;
  }
  for (let i = 0; i < groups.value.length; i++) {
    if (groups.value[i].parent_id != null) {
      [json, statusCode] = await getGroup(groups.value[i].parent_id);
      if (statusCode !== 200) {
        alert(json.detail)
      }
      groups.value[i].parent_id = json.group_name;
    }
  }
  
}

function handleFileChange(event) {
  fileInputRef.value = event.target;
  importGroup();
}

function createGroupPopUp() {
  const name = prompt("Entrez le nom du groupe");
  const parent = prompt("Entrez le nom du groupe parent (optionnel)");
  let parent_id = null;
  let isDuplicate = false;
  groups.value.forEach(element => {
    if (element.group_name == parent) {
      parent_id = element.id;
    } else if (element.group_name == name) {
      alert("Ce nom de groupe est déjà utilisé");
      isDuplicate = true;
    }
  });
  if (name == null) {
    return;
  } else if(isDuplicate) {
    return;
  }
  createGroup(name, parent_id);
  onFormSubmit();


}


async function readFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = (event) => {
      const content = event.target.result;
      resolve(content);
    };

    reader.onerror = (error) => {
      reject(error);
    };

    reader.readAsText(file);
  });
}


async function importGroup() {
  const fileInput = fileInputRef.value;
  const file = fileInput.files[0];

  if (!file) {
    alert("Veuillez sélectionner un fichier CSV");
    return;
  }

  const fileContent = await readFile(file);
  const groupsData = await parseCSV(fileContent);

  for (const groupData of groupsData) {
    const groupName = groupData.group_name;
    const members = groupData.members;

    const isDuplicate = groups.value.some(group => group.group_name === groupName);
    if (isDuplicate) {
      alert(`Le nom de groupe "${groupName}" est déjà utilisé.`);
    } else {
      const group = await createGroup(groupName, null);
      for (const member of members) {
        const [json, statusCode] = await getUserByEmail(member[0].email);
        addUserToGroup(group[0].id,json.id);
      }
    }
  }

  onFormSubmit();
}

async function parseCSV(content) {
  const lines = content.split('\n');
  const groups = [];

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();

    if (line.length === 0) {
      continue; 
    }

    const fields = line.split(',');

    if (fields.length >= 6) {
      const groupName = fields[1].trim();
      const name = fields[2].trim();
      const surname = fields[3].trim();
      const email = fields[5].trim();

     
      const existingUser = await getUserByEmail(email);

      if (existingUser[1]==200) {
        const existingGroup = groups.find(group => group.group_name === groupName);

        if (existingGroup) {
          existingGroup.members.push(existingUser);
        } else {
          const newGroup = {
            group_name: groupName,
            members: [existingUser],
          };
          groups.push(newGroup);
        }
      } else {
        const user = await register(name,surname,email,"student");
        const existingGroup = groups.find(group => group.group_name === groupName);

        if (existingGroup) {
          existingGroup.members.push(user);
        } else {
          const newGroup = {
            group_name: groupName,
            members: [user],
          };
          groups.push(newGroup);
        }
      }
    }
  }

  return groups;
}



onMounted(async () => {
  await onFormSubmit();
});

</script>

<template>
  <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"
  >
  <div>
    <Header />
    <h1> 
      {{ $t("allGrp.Groups") }}
      <!-- My groups  -->
    </h1>
    <div class="return">
      <button class="btnReturn">
        <img
          src="@/components/icons/return.svg"
          alt="return"
          @click="router.push('/surveys')"
        >
      </button>
    </div>
    <table>
      <colgroup>
        <col>
        <col>
        <col>
        <col>
        <col>
      </colgroup>
      <thead>
        <tr>
          <th class="actions">
            {{ $t("allGrp.actions")}}
            <!-- Actions -->
          </th>
          <th>
            {{ $t("allGrp.groupe") }}
            <!-- Groupes -->
          </th>
          <th>
            {{ $t("allGrp.creator") }}
            <!-- Créateur -->
          </th>
          <th>
            {{ $t("allGrp.parent") }}
            <!-- Groupe parent -->
          </th>
          <th>
            {{ $t("allGrp.members") }}
            <!-- Nombre de membres -->
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="group in groups"
          :key="group.id"
        >
          <td class="actions">
            <router-link
              :to="'/group/' + group.id"
              class="table-row-link"
            >
              <span class="material-symbols-outlined">
                edit
              </span>
            </router-link>
          </td>
          <td>
            <router-link
              :to="'/group/' + group.id"
              class="table-row-link"
            >
              {{ group.group_name }}
            </router-link>
          </td>
          <td>
            <router-link
              :to="'/group/' + group.id"
              class="table-row-link"
            >
              {{ group.creator_id }}
            </router-link>
          </td>
          <td>
            <router-link
              :to="'/group/' + group.id"
              class="table-row-link"
            >
              {{ group.parent_id }}
            </router-link>
          </td>
          <td>
            <router-link
              :to="'/group/' + group.id"
              class="table-row-link"
            >
              {{ group.count }}
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="button-container">
      <div>
        <label>
          <p style="display: none"> Import </p>
          <button @click="createGroupPopUp">
            {{ $t("allGrp.createGroup") }}
          <!-- Créer un groupe -->
          </button>
        </label>
      </div>

      <div class="import-container">
        <label class="custom-file-upload">
          <input ref="importFile"
                 type="file"
                 class="importFile"
                 @change="handleFileChange"
          >
          {{ $t("allGrp.importGrp") }}
          <!-- Importer des groupes -->
        </label>
      </div>
    </div>
  </div>
  <Gear />
</template>


<style scoped>
* {
  font-family: "Sofia Sans", sans-serif;
  color: var(--text-color);
}


table {
  margin-left: auto;
  margin-right: auto;
  font-family: 'Sofia Sans', sans-serif;
  border: 2px solid var(--main-color);
  border-spacing: 0;
  width: 60%;
  border-radius: 30px;
  padding: 10px 20px 20px;
  margin-bottom: 40px;
}

th, td {
  text-align: center;
  overflow-wrap: normal;
}

td {
  padding: 10px;
  min-width: 150px;
}

.actions td {
  min-width: 20px;
}

.button-container {
  display: block;
}

.import-container {
  display: block;
}

.custom-file-upload:hover{
  background-color: var(--CTA-color);
  transition: linear 0.3s;

}

.import-container button {
  margin-bottom: 10px;
}


tr {
  border-bottom: 1px solid var(--white);
}

button  {
  border-radius: 30px;
  background-color: var(--white);
  border: 2px solid var(--main-color);
  cursor: pointer;
  margin-left: 50px;
  margin-right: 10px;
  padding: 8px 20px;
  margin-bottom: 10px;
  font-size: 1em;
}

.custom-file-upload {
  font-size: 1em;
  display: inline-block;
  padding: 8px 20px;
  cursor: pointer;
  background-color: var(--CTA-color);
  border: 1px solid var(--CTA-color);
  border-radius: 30px;
  color: white;
  margin-left: 50px;
}

.importFile {
  display: none;
}

button:hover  {
  background-color: var(--CTA-color);
  color: white;
  transition: linear 0.3s;
}

thead,
tfoot {
  background-color: var(--white);
  font-family: 'Sofia Sans', sans-serif;
  color: var(--main-color);
  text-align: left;
  font-size: 1.1em;
}

tbody tr:nth-child(odd) {
  background-color: var(--white);
}

.table-row-link {
  display: block;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

col {
  width: 25%;
}

.btnReturn {
  background-color: transparent;
  border: none;
  border-radius: 100%;
  cursor: pointer;
  transition: 500ms;
  filter: var(--filter);
}

.btnReturn:hover {
  background-color: #17273a23;
  border-radius: 10px;
  transition: 500ms;
}


.material-symbols-outlined {
  font-variation-settings:
      'FILL' 0,
      'wght' 400,
      'GRAD' 0,
      'opsz' 24
}

h1 {
  display: inline-block;
  margin-left: 10px;
}

</style>

