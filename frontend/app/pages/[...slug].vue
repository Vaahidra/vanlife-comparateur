<script setup lang="ts">
/**
 * Catch-all pour pages statiques: /about, /mentions-legales, /contact, /politique-*.
 * Les routes /articles/* et /categories/* ont leurs propres pages dédiées.
 */
const route = useRoute()

const { data: page } = await useAsyncData('page-' + route.path, () =>
  queryCollection('pages').path(route.path).first(),
)

if (!page.value) {
  throw createError({ statusCode: 404, statusMessage: 'Page non trouvée', fatal: true })
}

useSeoMeta({
  title: () => page.value?.title,
  description: () => page.value?.description,
})
</script>

<template>
  <ContentRenderer
    v-if="page"
    :value="page"
  />
</template>
