<script setup lang="ts">
/**
 * Composant CTA Amazon avec injection automatique du partner_tag.
 *
 * Usage dans Markdown (MDC) :
 *   :amazon-cta{asin="B0CKQXQXQX" label="Voir le prix sur Amazon"}
 *
 * Usage dans Vue :
 *   <AmazonCta asin="B0CKQXQXQX" label="Voir le prix sur Amazon" />
 *
 * Le tag est lu depuis runtimeConfig.public.amazonPartnerTag
 * (env var NUXT_PUBLIC_AMAZON_PARTNER_TAG).
 *
 * Si le tag est absent (dev local sans .env) : lien généré SANS tag,
 * + warning console pour dev.
 */
interface Props {
  asin: string
  label?: string
  /** Override : si tu veux un produit qui n'est pas vraiment sur Amazon */
  hideIfNoTag?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  label: 'Voir le prix sur Amazon',
  hideIfNoTag: false,
})

const runtimeConfig = useRuntimeConfig()
const partnerTag = computed(() => runtimeConfig.public.amazonPartnerTag as string | undefined)

const amazonUrl = computed(() => {
  const base = `https://www.amazon.fr/dp/${props.asin}`
  if (partnerTag.value) {
    return `${base}?tag=${partnerTag.value}`
  }
  if (import.meta.dev) {
    console.warn(
      `[AmazonCta] NUXT_PUBLIC_AMAZON_PARTNER_TAG manquant. Lien généré sans tag : ${base}`,
    )
  }
  return base
})

const shouldRender = computed(() => {
  if (!props.hideIfNoTag) return true
  return Boolean(partnerTag.value)
})
</script>

<template>
  <a
    v-if="shouldRender"
    :href="amazonUrl"
    rel="sponsored nofollow noopener"
    target="_blank"
    class="cta-button-amazon my-4"
  >
    {{ label }}
    <span aria-hidden="true">→</span>
  </a>
</template>
