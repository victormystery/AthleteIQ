<template>
  <div class="bg-white border border-slate-200 rounded-xl p-6 flex items-start gap-4 shadow-sm hover:shadow-md transition-shadow">
    <div
      class="w-12 h-12 rounded-xl flex items-center justify-center shrink-0"
      :style="{ background: iconBg }"
    >
      <slot name="icon" />
    </div>
    <div class="flex-1 min-w-0">
      <p class="text-sm font-medium text-slate-500">{{ label }}</p>
      <p class="text-2xl font-bold text-slate-800 leading-tight mt-1">{{ value }}</p>
      <p v-if="change !== undefined" class="flex items-center gap-1.5 text-xs mt-2">
        <span :class="change >= 0 ? 'text-green-600' : 'text-red-600'">
          {{ change >= 0 ? '↑' : '↓' }} {{ Math.abs(change) }}%
        </span>
        <span class="text-slate-400">vs last month</span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  value: string | number
  change?: number
  iconBg?: string
}>()
</script>
