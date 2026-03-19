<template>
  <div :class="[
    'bg-white border border-slate-200 rounded-xl overflow-hidden',
    flat ? 'shadow-none' : 'shadow-sm',
    hoverable ? 'transition-all duration-150 hover:shadow-md hover:-translate-y-0.5 cursor-pointer' : ''
  ]">
    <div v-if="$slots.header || title" class="flex items-start justify-between gap-4 px-6 py-4 border-b border-slate-200">
      <slot name="header">
        <div>
          <h3 class="text-base font-semibold text-slate-800">{{ title }}</h3>
          <p v-if="subtitle" class="mt-0.5 text-sm text-slate-500">{{ subtitle }}</p>
        </div>
      </slot>
      <div v-if="$slots.actions" class="shrink-0">
        <slot name="actions" />
      </div>
    </div>
    <div class="p-6">
      <slot />
    </div>
    <div v-if="$slots.footer" class="px-6 py-3 bg-slate-50 border-t border-slate-200">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title?: string
  subtitle?: string
  hoverable?: boolean
  flat?: boolean
}>()
</script>
