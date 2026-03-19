<template>
  <div class="flex flex-col gap-1.5">
    <label v-if="label" :for="inputId" class="text-sm font-medium text-slate-700">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-0.5" aria-hidden="true">*</span>
    </label>
    <div class="relative">
      <span v-if="$slots.prefix" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none flex items-center">
        <slot name="prefix" />
      </span>
      <input
        :id="inputId"
        v-bind="$attrs"
        :type="type"
        :value="modelValue"
        :disabled="disabled"
        :placeholder="placeholder"
        :required="required"
        :autocomplete="autocomplete"
        :class="[
          'w-full px-3 py-2 text-sm text-slate-800 bg-white rounded-lg outline-none',
          'border transition-all duration-150',
          'placeholder:text-slate-400',
          'disabled:bg-slate-50 disabled:opacity-60 disabled:cursor-not-allowed',
          $slots.prefix ? 'pl-9' : '',
          error
            ? 'border-red-400 focus:border-red-500 focus:ring-2 focus:ring-red-500/20'
            : 'border-slate-300 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20'
        ]"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        @blur="$emit('blur', $event)"
      />
    </div>
    <p v-if="error" class="text-xs text-red-600" role="alert">{{ error }}</p>
    <p v-else-if="hint" class="text-xs text-slate-500">{{ hint }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue?: string
  label?: string
  type?: string
  placeholder?: string
  error?: string
  hint?: string
  disabled?: boolean
  required?: boolean
  autocomplete?: string
  inputId?: string
}>()

defineEmits<{
  'update:modelValue': [value: string]
  'blur': [event: FocusEvent]
}>()

defineOptions({ inheritAttrs: false })

const inputId = `input-${Math.random().toString(36).slice(2, 7)}`
</script>
