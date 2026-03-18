<script setup lang="ts">
import DockerOption from './DockerOption.vue';
import DockerComposeOption from './DockerComposeOption.vue';

const selected = defineModel<string>({default: 'none'});

const options = [
    {id: 'none', label: '無', description: '不套用任何選項'},
    {id: 'docker', label: 'Docker', component: 'DockerOption'},
    {id: 'docker-compose', label: 'DockerCompose', component: 'DockerComposeOption'},
];
</script>

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
            @click="selected = opt.id"
            :class="[
        'relative flex flex-col p-4 cursor-pointer rounded-xl border-2 transition-all duration-200 ease-in-out',
        selected === opt.id
          ? 'border-indigo-600 bg-indigo-50/30 ring-1 ring-indigo-600'
          : 'border-slate-200 bg-white hover:border-slate-300'
      ]"
        >
            <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-3">
                    <div
                        :class="[
              'w-5 h-5 rounded-full border flex items-center justify-center transition-colors',
              selected === opt.id ? 'border-indigo-600 bg-indigo-600' : 'border-slate-300 bg-white'
            ]"
                    >
                        <div v-if="selected === opt.id" class="w-2 h-2 rounded-full bg-white"></div>
                    </div>

                    <span :class="['font-semibold', selected === opt.id ? 'text-indigo-900' : 'text-slate-700']">
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
                :class="[selected === opt.id ? 'opacity-100' : 'opacity-40 grayscale pointer-events-none']"
            >
                <DockerComposeOption v-if="opt.id === 'docker-compose'" />
                <DockerOption v-if="opt.id === 'docker'" />
            </div>
        </div>
    </div>
</template>