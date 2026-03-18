<template>
    <div class="flex flex-col space-y-4">
        <div class="flex items-center justify-between">
            <div class="text-lg font-medium">啟動選項</div>
        </div>
    </div>
    <div class="w-full max-w-2xl space-y-4">
        <div
            v-for="opt in options"
            :key="opt.id"
            @click="info.activate = opt.id as ActivateType"
            :class="[
        'relative flex flex-col p-4 cursor-pointer rounded-xl border-2 transition-all duration-200 ease-in-out',
        info.activate === opt.id
          ? 'border-indigo-600 bg-indigo-50/30 ring-1 ring-indigo-600'
          : 'border-slate-200 bg-white hover:border-slate-300'
      ]"
        >
            <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-3">
                    <div
                        :class="[
              'w-5 h-5 rounded-full border flex items-center justify-center transition-colors',
              info.activate === opt.id ? 'border-indigo-600 bg-indigo-600' : 'border-slate-300 bg-white'
            ]"
                    >
                        <div v-if="info.activate === opt.id" class="w-2 h-2 rounded-full bg-white"></div>
                    </div>

                    <span :class="['font-semibold', info.activate === opt.id ? 'text-indigo-900' : 'text-slate-700']">
            {{ opt.label }}
          </span>
                </div>
            </div>

            <p v-if="opt.id === 'none'" class="ml-8 text-sm text-slate-500">
                {{ opt.description }}
            </p>

            <div
                v-if="opt.id !== 'none'"
                class="ml-8 mt-2 overflow-hidden transition-all"
                :class="[info.activate === opt.id ? 'opacity-100' : 'opacity-40 grayscale pointer-events-none']"
            >
                <DockerComposeOption v-if="opt.id === 'docker-compose'"/>
                <DockerOption v-if="opt.id === 'docker'" v-model="info.activate_info.docker as DockerInfo"/>
            </div>
        </div>
    </div>
    <div class="flex flex-col space-y-4">
        <div class="flex items-center justify-between">
            <div class="text-lg font-medium">呈現選項</div>
        </div>
    </div>
    <div class="w-full max-w-2xl space-y-4">
        <div
            v-for="opt in options2"
            :key="opt.id"
            @click="info.present = opt.id as PresentType"
            :class="[
        'relative flex flex-col p-4 cursor-pointer rounded-xl border-2 transition-all duration-200 ease-in-out',
        info.present === opt.id
          ? 'border-indigo-600 bg-indigo-50/30 ring-1 ring-indigo-600'
          : 'border-slate-200 bg-white hover:border-slate-300'
      ]"
        >
            <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-3">
                    <div
                        :class="[
              'w-5 h-5 rounded-full border flex items-center justify-center transition-colors',
              info.present === opt.id ? 'border-indigo-600 bg-indigo-600' : 'border-slate-300 bg-white'
            ]"
                    >
                        <div v-if="info.present === opt.id" class="w-2 h-2 rounded-full bg-white"></div>
                    </div>

                    <span :class="['font-semibold', info.present === opt.id ? 'text-indigo-900' : 'text-slate-700']">
            {{ opt.label }}
          </span>
                </div>
            </div>

            <p v-if="opt.id === 'none'" class="ml-8 text-sm text-slate-500">
                {{ opt.description }}
            </p>

            <div
                v-if="opt.id !== 'none'"
                class="ml-8 mt-2 overflow-hidden transition-all"
                :class="[info.present === opt.id ? 'opacity-100' : 'opacity-40 grayscale pointer-events-none']"
            >
                <HttpOption v-if="opt.id === 'http'" v-model="info.present_info.http as HttpInfo"/>
            </div>
        </div>
    </div>

    <button @click="handleSave()"
            class="px-3 py-1.5 bg-emerald-50 text-emerald-700 text-sm font-bold rounded-lg hover:bg-emerald-100 transition-colors">
        儲存
    </button>
</template>

<script setup lang="ts">
import DockerOption from './DockerOption.vue';
import DockerComposeOption from './DockerComposeOption.vue';
import type {ActivateType, DockerInfo, HttpInfo, PresentType, ServiceInfo} from "@/utils/types.ts";
import HttpOption from "@/components/HttpOption.vue";
import axios from "axios";
import {show_modal} from "@/utils/modal.ts";

interface Props {
    name: string;
}

const info = defineModel<ServiceInfo>({required: true});
const props = defineProps<Props>();

const options = [
    {id: 'none', label: '無', description: '不套用任何選項'},
    {id: 'docker', label: 'Docker', component: 'DockerOption'},
    {id: 'docker-compose', label: 'DockerCompose', component: 'DockerComposeOption'},
];

const options2 = [
    {id: 'none', label: '無', description: '不提供呈現'},
    {id: 'http', label: 'HTTP', component: 'HttpOption'},
];

async function handleSave() {
    const data = {
        "name": props.name,
        "info": info.value
    }
    try {
        const res = await axios.put("/api/services", data);
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