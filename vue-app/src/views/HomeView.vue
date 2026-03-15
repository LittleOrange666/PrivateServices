<template>
    <div class="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md mx-auto">

            <h1 class="text-3xl font-extrabold text-slate-900 mb-8 text-center tracking-tight">
                這是首頁
            </h1>

            <nav class="space-y-3">
                <div v-for="name in names" :key="name">
                    <a :href="`/${name}/`"
                       class="group block px-6 py-4 bg-white border border-slate-200 rounded-2xl shadow-sm
                    hover:shadow-md hover:border-indigo-400 hover:bg-indigo-50/30
                    transition-all duration-200 ease-in-out">

                        <div class="flex items-center justify-between">
              <span class="text-slate-700 font-medium group-hover:text-indigo-600 transition-colors">
                {{ name }}
              </span>

                            <svg xmlns="http://www.w3.org/2000/svg"
                                 class="h-5 w-5 text-slate-400 group-hover:text-indigo-500 group-hover:translate-x-1 transition-all"
                                 fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="9 5l7 7-7 7" />
                            </svg>
                        </div>

                    </a>
                </div>
            </nav>

        </div>
    </div>
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

