<template>
  <svg
    :class="[
      'animate-spin flex-shrink-0',
      sizeClass,
      colorClass
    ]"
    viewBox="0 0 24 24"
    fill="none"
    aria-hidden="true"
  >
    <circle
      cx="12" cy="12" r="10"
      stroke="currentColor"
      stroke-width="3"
      stroke-linecap="round"
      class="opacity-25"
    />
    <path
      d="M12 2a10 10 0 0 1 10 10"
      stroke="currentColor"
      stroke-width="3"
      stroke-linecap="round"
    />
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  size?: 'sm' | 'md' | 'lg'
  color?: 'white' | 'primary' | 'muted'
}>()

const sizeClass = computed(() => ({
  sm: 'w-4 h-4',
  md: 'w-6 h-6',
  lg: 'w-10 h-10'
}[props.size ?? 'md']))

const colorClass = computed(() => ({
  white: 'text-white',
  primary: 'text-primary-600',
  muted: 'text-slate-400'
}[props.color ?? 'primary']))
</script>
