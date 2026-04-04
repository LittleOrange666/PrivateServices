<template>
  <span class="relative flex h-3 w-3" v-if="status === 'running'">
    <span
            class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
    <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
  </span>
    <span class="relative flex h-3 w-3" v-if="status === 'stopped'">
    <span
            class="animate-ping absolute inline-flex h-full w-full rounded-full bg-slate-400 opacity-75"></span>
    <span class="relative inline-flex rounded-full h-3 w-3 bg-slate-500"></span>
  </span>
    <span class="relative flex h-3 w-3" v-if="status === 'error'">
    <span
            class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
    <span class="relative inline-flex rounded-full h-3 w-3 bg-rose-500"></span>
  </span>
    <span class="relative flex h-3 w-3" v-if="status === 'idle'">
    <span
            class="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
    <span class="relative inline-flex rounded-full h-3 w-3 bg-amber-500"></span>
  </span>
</template>

<script setup lang="ts">
type StatusType = 'running' | 'stopped' | 'error' | 'idle';
interface Props{
    status: StatusType
}
defineProps<Props>();

</script>