<template>
    <div class="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-3xl mx-auto"><h1 class="text-xl font-extrabold text-slate-900 mb-8 text-center tracking-tight">
            首頁
        </h1>
            <div class="space-y-4">
                <div v-for="name in names" :key="name"
                     class="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden transition-all duration-300"
                     :class="{'ring-2 ring-indigo-100 shadow-lg': editingName === name}">
                    <div class="flex items-center justify-between px-6 py-4">
                        <div class="flex items-center gap-3">
              <span class="relative flex h-3 w-3">
                <span
                        class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
              </span>
                            <span class="text-slate-700 font-semibold text-lg font-mono">
                {{ name }}
              </span>
                        </div>

                        <div class="flex items-center gap-2">
                            <a :href="`/${name}/`"
                               class="px-3 py-1.5 bg-indigo-50 text-indigo-700 text-sm font-bold rounded-lg hover:bg-indigo-100 transition-colors">
                                前往
                            </a>

                            <button @click="toggleEdit(name)" v-if="auth.role=='admin'"
                                    class="px-3 py-1.5 text-sm font-bold rounded-lg transition-colors flex items-center gap-1"
                                    :class="editingName === name ? 'bg-slate-200 text-slate-800' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
                                {{ editingName === name ? '取消' : '編輯' }}
                            </button>

                            <button @click="handleStart(name)"
                                    class="px-3 py-1.5 bg-emerald-50 text-emerald-700 text-sm font-bold rounded-lg hover:bg-emerald-100 transition-colors">
                                啟動
                            </button>

                            <button @click="handleStop(name)"
                                    class="px-3 py-1.5 bg-rose-50 text-rose-700 text-sm font-bold rounded-lg hover:bg-rose-100 transition-colors">
                                停止
                            </button>

                            <button @click="handleRemove(name)"
                                    class="px-3 py-1.5 bg-rose-50 text-rose-700 text-sm font-bold rounded-lg hover:bg-rose-100 transition-colors">
                                刪除容器
                            </button>
                        </div>
                    </div>

                    <transition
                            enter-active-class="transition-[max-height] duration-300 ease-out"
                            enter-from-class="max-height-0"
                            enter-to-class="max-height-96"
                            leave-active-class="transition-[max-height] duration-200 ease-in"
                            leave-from-class="max-height-96"
                            leave-to-class="max-height-0"
                    >
                        <div v-if="editingName === name"
                             class="overflow-hidden border-t border-slate-100 bg-slate-50/50">
                            <div class="px-6 py-5">
                                <EditComponent :name="name" v-model="service_table[name] as ServiceInfo"
                                               @close="editingName = null"/>
                            </div>
                        </div>
                    </transition>

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
import type {AService, ServiceInfo} from "@/utils/types.ts";
import EditComponent from "@/components/EditComponent.vue";

const names = ref<string[]>([]);
const auth = useAuthStore();
const router = useRouter();

const services = ref<AService[]>([]);
const service_table = ref<Record<string, ServiceInfo>>({});

// 關鍵狀態：記錄目前哪一個項目正在被編輯 (null 表示沒有項目在編輯)
const editingName = ref<string | null>(null)

// 切換編輯狀態的函數
const toggleEdit = (name: string) => {
    if (editingName.value === name) {
        // 如果點擊的是同一個，則關閉
        editingName.value = null
    } else {
        // 否則，打開點擊的這一個 (這也會自動關閉原本打開的另一個)
        editingName.value = name
    }
}

function fix_info(obj: ServiceInfo) {
    if (!obj.activate_info.docker) {
        obj.activate_info.docker = {
            "image": "Ubuntu"
        }
    }
    if (!obj.present_info.http) {
        obj.present_info.http = {
            "hostname": "host.docker.internal",
            "port": 8080
        }
    }
    if (!obj.activate_info.docker_compose) {
        obj.activate_info.docker_compose = {
            "filepath": "docker-compose.yml"
        }
    }
}

async function loadData() {
    await auth.load();
    if (auth.role == "unauthorized") {
        await router.push("/login");
        return;
    }
    const res = await axios.get("/api/services");
    services.value = res.data.services;
    const out = [];
    const table: Record<string, ServiceInfo> = {};
    for (let service of services.value) {
        out.push(service.service_name);
        fix_info(service.info);
        table[service.service_name] = service.info;
    }
    names.value = out;
    service_table.value = table
}

onMounted(async () => {
    await loadData();
});

async function handleStart(name: string) {
    try {
        const res = await axios.post("/api/services/on", {name: name});
        if (res.status === 200) {
            await show_modal("成功", res.data.message);
        } else {
            await show_modal("失敗", "Error " + res.status);
        }
    } catch (e) {
        await show_modal("失敗", (e as Error).message);
    }
}

async function handleStop(name: string) {
    try {
        const res = await axios.post("/api/services/off", {name: name});
        if (res.status === 200) {
            await show_modal("成功", res.data.message);
        } else {
            await show_modal("失敗", "Error " + res.status);
        }
    } catch (e) {
        await show_modal("失敗", (e as Error).message);
    }
}

async function handleRemove(name: string) {
    try {
        const res = await axios.post("/api/services/remove", {name: name});
        if (res.status === 200) {
            await show_modal("成功", res.data.message);
        } else {
            await show_modal("失敗", "Error " + res.status);
        }
    } catch (e) {
        await show_modal("失敗", (e as Error).message);
    }
}

</script>

