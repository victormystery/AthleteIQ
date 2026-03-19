<template>
  <component
    :is="tag"
    :type="tag === 'button' ? type : undefined"
    :disabled="disabled || loading"
    :class="classes"
    v-bind="$attrs"
  >
    <AppSpinner v-if="loading" size="sm" :color="variant === 'primary' || variant === 'danger' ? 'white' : 'muted'" />
    <slot />
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppSpinner from './AppSpinner.vue'

const props = defineProps<{
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  type?: string
  tag?: string
  loading?: boolean
  disabled?: boolean
  block?: boolean
}>()

const variant = computed(() => props.variant ?? 'primary')
const size = computed(() => props.size ?? 'md')

const classes = computed(() => [
  // Base
  'inline-flex items-center justify-center gap-2 font-semibold rounded-lg',
  'transition-all duration-150 whitespace-nowrap select-none',
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
  // Disabled / loading
  (props.disabled || props.loading) ? 'opacity-60 cursor-not-allowed' : '',
  // Block
  props.block ? 'w-full' : '',
  // Size
  {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base'
  }[size.value],
  // Variant
  {
    primary:   'bg-primary-600 text-white hover:bg-primary-700 focus-visible:ring-primary-500',
    secondary: 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-50 focus-visible:ring-slate-400',
    danger:    'bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500',
    ghost:     'bg-transparent text-slate-500 hover:bg-slate-100 hover:text-slate-800 focus-visible:ring-slate-400',
    outline:   'bg-transparent text-primary-600 border border-primary-600 hover:bg-primary-50 focus-visible:ring-primary-500'
  }[variant.value]
])
</script>
