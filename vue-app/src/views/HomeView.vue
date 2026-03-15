<template>
    <h1>這是首頁</h1>
    <p v-for="name in names" :key="name">
        <a :href="`/${name}/`">{{ name }}</a>
    </p>
</template>

<script setup lang="ts">

import {onMounted, ref} from "vue";
import axios from "axios";

const names = ref<string[]>([]);

async function loadData(){
    const res = await axios.get("/api/services");
    const out = [];
    for(let service of res.data.services){
        out.push(service.service_name);
    }
    names.value = out;
}
onMounted(async () => {
    await loadData();
});

</script>

