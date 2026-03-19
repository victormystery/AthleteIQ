<template>
  <Transition name="fade">
    <div
      v-if="show"
      :class="[
        'flex items-start gap-3 p-4 rounded-lg border',
        typeClasses
      ]"
      role="alert"
    >
      <div class="shrink-0 mt-0.5">
        <!-- success -->
        <svg v-if="type === 'success'" viewBox="0 0 20 20" fill="currentColor" class="w-4.5 h-4.5"><path fill-rule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16zm3.857-9.809a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5z" clip-rule="evenodd"/></svg>
        <!-- error -->
        <svg v-else-if="type === 'error'" viewBox="0 0 20 20" fill="currentColor" class="w-4.5 h-4.5"><path fill-rule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM8.28 7.22a.75.75 0 0 0-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 1 0 1.06 1.06L10 11.06l1.72 1.72a.75.75 0 1 0 1.06-1.06L11.06 10l1.72-1.72a.75.75 0 0 0-1.06-1.06L10 8.94 8.28 7.22z" clip-rule="evenodd"/></svg>
        <!-- warning -->
        <svg v-else-if="type === 'warning'" viewBox="0 0 20 20" fill="currentColor" class="w-4.5 h-4.5"><path fill-rule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 10 5zm0 9a1 1 0 1 0 0-2 1 1 0 0 0 0 2z" clip-rule="evenodd"/></svg>
        <!-- info -->
        <svg v-else viewBox="0 0 20 20" fill="currentColor" class="w-4.5 h-4.5"><path fill-rule="evenodd" d="M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0zm-7-4a1 1 0 1 1-2 0 1 1 0 0 1 2 0zM9 9a.75.75 0 0 0 0 1.5h.253a.25.25 0 0 1 .244.304l-.459 2.066A1.75 1.75 0 0 0 10.747 15H11a.75.75 0 0 0 0-1.5h-.253a.25.25 0 0 1-.244-.304l.459-2.066A1.75 1.75 0 0 0 9.253 9H9z" clip-rule="evenodd"/></svg>
      </div>
      <div class="flex-1 min-w-0">
        <p v-if="title" class="font-semibold text-sm mb-0.5">{{ title }}</p>
        <p class="text-sm"><slot /></p>
      </div>
      <button
        v-if="dismissible"
        class="shrink-0 opacity-60 hover:opacity-100 transition-opacity p-0.5 rounded"
        @click="$emit('dismiss')"
        aria-label="Dismiss"
      >
        <svg viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4"><path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22z"/></svg>
      </button>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  type?: 'success' | 'error' | 'warning' | 'info'
  title?: string
  show?: boolean
  dismissible?: boolean
}>()

defineEmits<{ dismiss: [] }>()

const typeClasses = computed(() => ({
  success: 'bg-green-50 border-green-200 text-green-800',
  error:   'bg-red-50 border-red-200 text-red-800',
  warning: 'bg-amber-50 border-amber-200 text-amber-800',
  info:    'bg-primary-50 border-primary-200 text-primary-800'
}[props.type ?? 'info']))
</script>
