<template>
    <div class="flex flex-col space-y-4">
        <div class="flex items-center justify-between">
            <div class="text-lg font-medium">Docker選項</div>
        </div>
    </div>
</template>

<style scoped>

</style>

<script setup lang="ts">

import type {DockerInfo} from "@/utils/types.ts";

const info = defineModel<DockerInfo>();

</script>

