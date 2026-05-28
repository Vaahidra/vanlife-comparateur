<script setup lang="ts">
interface Props {
  title: string
  subtitle?: string
  intro?: string
}
defineProps<Props>()
</script>

<template>
  <section class="text-center py-12 sm:py-16">
    <h1 class="font-serif text-4xl sm:text-5xl lg:text-6xl font-bold text-anthracite-900 leading-tight mb-4">
      {{ title }}
    </h1>
    <p v-if="subtitle" class="text-xl sm:text-2xl text-sand-700 font-medium mb-6">
      {{ subtitle }}
    </p>
    <p v-if="intro" class="max-w-2xl mx-auto text-lg text-anthracite-700 leading-relaxed">
      {{ intro }}
    </p>
  </section>
</template>
