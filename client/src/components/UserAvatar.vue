<template>
  <div
    :class="[
      'rounded-full overflow-hidden flex items-center justify-center shrink-0 font-semibold text-white select-none',
      sizeClass
    ]"
    :style="avatarStyle"
  >
    <img v-if="src" :src="src" :alt="name" class="w-full h-full object-cover" />
    <span v-else>{{ initials }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  name?: string
  src?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
  color?: string
}>()

const sizeClass = computed(() => ({
  sm: 'w-8 h-8 text-xs',
  md: 'w-10 h-10 text-sm',
  lg: 'w-14 h-14 text-lg',
  xl: 'w-20 h-20 text-2xl'
}[props.size ?? 'md']))

const initials = computed(() => {
  if (!props.name) return '?'
  return props.name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0].toUpperCase())
    .join('')
})

const palette = ['#ea580c', '#c2410c', '#16a34a', '#d97706', '#dc2626', '#9333ea', '#db2777', '#0d9488']

const avatarStyle = computed(() => {
  if (props.src) return {}
  const color = props.color || palette[(props.name?.charCodeAt(0) ?? 0) % palette.length]
  return { background: color }
})
</script>
