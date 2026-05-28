<script setup lang="ts">
interface Props {
  article: {
    path: string
    title: string
    description: string
    type?: string
    category?: string
    published_at?: string
    featured_image?: string
  }
}
const props = defineProps<Props>()

const typeLabel = computed(() => {
  switch (props.article.type) {
    case 'comparatif': return 'Comparatif'
    case 'test_produit': return 'Test'
    case 'guide_achat': return 'Guide d\'achat'
    default: return 'Article'
  }
})

const formattedDate = computed(() => {
  if (!props.article.published_at) return ''
  return new Date(props.article.published_at).toLocaleDateString('fr-FR', {
    year: 'numeric', month: 'long', day: 'numeric',
  })
})

// True si featured_image est une vraie URL/path locale (pas placeholder)
const hasRealImage = computed(() => {
  const img = props.article.featured_image
  return Boolean(img) && !img!.startsWith('placeholder://') && !img!.includes('picsum.photos')
})
</script>

<template>
  <article class="group bg-white border border-sand-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow">
    <NuxtLink :to="article.path" class="block no-underline">
      <div class="aspect-[16/9] overflow-hidden">
        <NuxtImg
          v-if="hasRealImage"
          :src="article.featured_image"
          :alt="article.title"
          class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          loading="lazy"
        />
        <PlaceholderImage
          v-else
          :title="article.title"
          :category="article.category"
          :type="article.type"
        />
      </div>

      <div class="p-5">
        <div class="flex items-center gap-3 mb-3 text-xs">
          <span class="px-2 py-0.5 bg-anthracite-900 text-sand-50 rounded font-medium uppercase tracking-wide">
            {{ typeLabel }}
          </span>
          <span v-if="article.category" class="text-sand-700 capitalize">
            {{ article.category }}
          </span>
        </div>

        <h3 class="font-serif text-xl font-bold text-anthracite-900 mb-2 leading-tight group-hover:text-sand-800 transition-colors">
          {{ article.title }}
        </h3>

        <p class="text-anthracite-700 text-sm leading-relaxed mb-3 line-clamp-2">
          {{ article.description }}
        </p>

        <p v-if="formattedDate" class="text-xs text-anthracite-500">
          {{ formattedDate }}
        </p>
      </div>
    </NuxtLink>
  </article>
</template>
