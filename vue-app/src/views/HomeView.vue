<template>
    <div class="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-2xl mx-auto"><h1
            class="text-3xl font-extrabold text-slate-900 mb-8 text-center tracking-tight">
            首頁
        </h1>

            <div class="space-y-4">
                <div v-for="name in names" :key="name"
                     class="flex items-center justify-between px-6 py-4 bg-white border border-slate-200 rounded-2xl shadow-sm transition-all">

          <span class="text-slate-700 font-semibold text-lg">
            {{ name }}
          </span>

                    <div class="flex items-center gap-2">
                        <a :href="`/${name}/`"
                           class="px-4 py-2 bg-indigo-50 text-indigo-700 text-sm font-bold rounded-xl hover:bg-indigo-600 hover:text-white transition-colors duration-200">
                            前往
                        </a>

                        <button @click="handleStart(name)"
                                class="px-4 py-2 bg-emerald-50 text-emerald-700 text-sm font-bold rounded-xl hover:bg-emerald-600 hover:text-white transition-colors duration-200">
                            啟動
                        </button>

                        <button @click="handleStop(name)"
                                class="px-4 py-2 bg-rose-50 text-rose-700 text-sm font-bold rounded-xl hover:bg-rose-600 hover:text-white transition-colors duration-200">
                            停止
                        </button>
                    </div>

                </div>
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">

import {onMounted, ref} from "vue";
import axios from "axios";
import {show_modal} from "@/utils/modal.ts";
import {useAuthStore} from "@/stores/auth.ts";
import {useRouter} from "vue-router";

const names = ref<string[]>([]);
const auth = useAuthStore();
const router = useRouter();

async function loadData() {
    await auth.load();
    if (auth.role == "unauthorized"){
        await router.push("/login");
        return;
    }
    const res = await axios.get("/api/services");
    const out = [];
    for (let service of res.data.services) {
        out.push(service.service_name);
    }
    names.value = out;
}

onMounted(async () => {
    await loadData();
});

async function handleStart(name: string) {
    try{
        const res = await axios.post("/api/services/on", {name: name});
        if (res.status === 200) {
            await show_modal("成功", res.data.message);
        }else{
            await show_modal("失敗", "Error "+res.status);
        }
    }catch (e){
        await show_modal("失敗", (e as Error).message);
    }
}

async function handleStop(name: string) {
    try{
        const res = await axios.post("/api/services/off", {name: name});
        if (res.status === 200) {
            await show_modal("成功", res.data.message);
        }else{
            await show_modal("失敗", "Error "+res.status);
        }
    }catch (e){
        await show_modal("失敗", (e as Error).message);
    }
}

</script>

