<script setup lang="ts">
const route = useRoute()
const path = computed(() => route.path)

const { data: article } = await useAsyncData(
  `article-${path.value}`,
  () => queryCollection('articles').path(path.value).first(),
)

if (!article.value) {
  throw createError({ statusCode: 404, statusMessage: 'Article introuvable', fatal: true })
}

useSeoMeta({
  title: () => article.value?.title,
  description: () => article.value?.description,
  ogTitle: () => article.value?.title,
  ogDescription: () => article.value?.description,
  ogType: 'article',
  ogImage: () => article.value?.featured_image,
  articlePublishedTime: () => article.value?.published_at,
  articleModifiedTime: () => article.value?.updated_at,
  articleAuthor: () => article.value?.author ? [article.value.author] : undefined,
  articleSection: () => article.value?.category,
})

const typeLabel = computed(() => {
  switch (article.value?.type) {
    case 'comparatif': return 'Comparatif'
    case 'test_produit': return 'Test produit'
    case 'guide_achat': return 'Guide d\'achat'
    default: return 'Article'
  }
})

const formattedDate = computed(() => {
  if (!article.value?.published_at) return ''
  return new Date(article.value.published_at).toLocaleDateString('fr-FR', {
    year: 'numeric', month: 'long', day: 'numeric',
  })
})

const hasRealImage = computed(() => {
  const img = article.value?.featured_image
  return Boolean(img) && !img!.startsWith('placeholder://') && !img!.includes('picsum.photos')
})
</script>

<template>
  <article v-if="article">
    <!-- Breadcrumb -->
    <nav class="text-sm text-anthracite-600 mb-4 not-prose">
      <NuxtLink to="/" class="hover:underline">Accueil</NuxtLink>
      <span class="mx-2">/</span>
      <NuxtLink to="/articles" class="hover:underline">Articles</NuxtLink>
      <template v-if="article.category">
        <span class="mx-2">/</span>
        <NuxtLink :to="`/categories/${article.category}`" class="hover:underline capitalize">
          {{ article.category }}
        </NuxtLink>
      </template>
    </nav>

    <!-- Header article -->
    <header class="mb-8 not-prose">
      <div class="flex items-center gap-3 mb-4 text-xs">
        <span class="px-2 py-0.5 bg-anthracite-900 text-sand-50 rounded font-medium uppercase tracking-wide">
          {{ typeLabel }}
        </span>
        <span v-if="formattedDate" class="text-anthracite-600">{{ formattedDate }}</span>
        <span v-if="article.author" class="text-anthracite-600">par {{ article.author }}</span>
      </div>

      <h1 class="font-serif text-4xl sm:text-5xl font-bold text-anthracite-900 leading-tight mb-3">
        {{ article.title }}
      </h1>
      <p class="text-xl text-anthracite-700 leading-relaxed">
        {{ article.description }}
      </p>
    </header>

    <!-- Featured image (vraie photo si dispo, sinon SVG placeholder cohérent) -->
    <figure class="mb-10 not-prose rounded-lg overflow-hidden aspect-[16/9]">
      <NuxtImg
        v-if="hasRealImage"
        :src="article.featured_image"
        :alt="article.title"
        class="w-full h-full object-cover"
        loading="eager"
      />
      <PlaceholderImage
        v-else
        :title="article.title"
        :category="article.category"
        :type="article.type"
      />
    </figure>

    <!-- Corps article (markdown via ContentRenderer) -->
    <ContentRenderer :value="article" />

    <!-- Footer article -->
    <footer class="mt-16 pt-8 border-t border-sand-300 not-prose">
      <NuxtLink
        v-if="article.category"
        :to="`/categories/${article.category}`"
        class="inline-block text-sand-700 hover:text-sand-900 underline"
      >
        ← Plus d'articles {{ article.category }}
      </NuxtLink>
    </footer>
  </article>
</template>
