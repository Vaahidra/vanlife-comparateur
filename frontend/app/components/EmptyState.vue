<script setup lang="ts">
interface Props {
  title?: string
  message?: string
}
withDefaults(defineProps<Props>(), {
  title: 'Bientôt disponible',
  message: 'Les premiers articles sont en cours de rédaction. Reviens dans quelques jours.',
})
</script>

<template>
  <div class="text-center py-16 px-4">
    <div class="font-serif text-5xl text-sand-300 mb-4">⌛</div>
    <h2 class="font-serif text-2xl font-bold text-anthracite-900 mb-2">{{ title }}</h2>
    <p class="text-anthracite-700 max-w-md mx-auto">{{ message }}</p>
    <NuxtLink
      to="/"
      class="inline-block mt-6 text-sm text-sand-700 underline hover:text-sand-900"
    >
      ← Retour à l'accueil
    </NuxtLink>
  </div>
</template>
