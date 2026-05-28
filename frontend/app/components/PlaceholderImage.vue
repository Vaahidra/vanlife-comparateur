<script setup lang="ts">
/**
 * Image placeholder SVG cohérente avec le design vanlife.
 * Utilisé tant que les vraies photos produit ne sont pas générées (Phase 5 pipeline).
 */
interface Props {
  title: string
  category?: string
  type?: string
}
const props = defineProps<Props>()

// Couleur dominante selon catégorie
const palette = computed(() => {
  switch (props.category) {
    case 'energie': return { from: '#caa66c', to: '#82603a', accent: '#faf7f2' }
    case 'cuisine': return { from: '#dcc599', to: '#6b4f33', accent: '#faf7f2' }
    case 'confort': return { from: '#b88c4f', to: '#58422c', accent: '#faf7f2' }
    case 'securite': return { from: '#3a414a', to: '#1a1d29', accent: '#dcc599' }
    case 'amenagement': return { from: '#a07640', to: '#3a414a', accent: '#faf7f2' }
    default: return { from: '#b88c4f', to: '#2d3142', accent: '#faf7f2' }
  }
})

// Icône SVG path par catégorie (Heroicons style)
const iconPath = computed(() => {
  switch (props.category) {
    case 'energie': // bolt
      return 'M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z'
    case 'cuisine': // beaker/cup
      return 'M4.5 3.75h15v3.75H4.5V3.75zM5.625 9h12.75l-1.5 11.25H7.125L5.625 9z'
    case 'confort': // fire / flame
      return 'M15.362 5.214A8.252 8.252 0 0112 21 8.25 8.25 0 016.038 7.048 8.287 8.287 0 009 9.6a8.983 8.983 0 013.361-6.867 8.21 8.21 0 003 2.48z'
    case 'securite': // shield
      return 'M9 12.75L11.25 15 15 9.75M12 2.25l8.954 4.477a.75.75 0 01.046.255v6.018a9 9 0 11-18 0V6.982a.75.75 0 01.046-.255L12 2.25z'
    case 'amenagement': // home / cube
      return 'M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21'
    default: // simple star
      return 'M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.562.562 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z'
  }
})

const typeLabel = computed(() => {
  switch (props.type) {
    case 'comparatif': return 'Comparatif'
    case 'test_produit': return 'Test'
    case 'guide_achat': return 'Guide'
    default: return ''
  }
})
</script>

<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 1200 675"
    class="w-full h-full"
    preserveAspectRatio="xMidYMid slice"
    role="img"
    :aria-label="title"
  >
    <defs>
      <linearGradient :id="`grad-${title.length}`" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" :stop-color="palette.from" />
        <stop offset="100%" :stop-color="palette.to" />
      </linearGradient>
      <pattern :id="`dots-${title.length}`" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
        <circle cx="20" cy="20" r="1" :fill="palette.accent" fill-opacity="0.15" />
      </pattern>
    </defs>

    <!-- Background gradient -->
    <rect width="1200" height="675" :fill="`url(#grad-${title.length})`" />

    <!-- Dots pattern overlay -->
    <rect width="1200" height="675" :fill="`url(#dots-${title.length})`" />

    <!-- Icône grande, en arrière-plan -->
    <g transform="translate(900, 100)" :fill="palette.accent" fill-opacity="0.12">
      <svg width="500" height="500" viewBox="0 0 24 24" stroke="none">
        <path :d="iconPath" />
      </svg>
    </g>

    <!-- Type label (badge) -->
    <g v-if="typeLabel" transform="translate(60, 80)">
      <rect width="180" height="42" rx="6" fill="#1a1d29" />
      <text
        x="90"
        y="28"
        text-anchor="middle"
        :fill="palette.accent"
        font-family="Inter, sans-serif"
        font-size="16"
        font-weight="600"
        letter-spacing="2"
      >
        {{ typeLabel.toUpperCase() }}
      </text>
    </g>

    <!-- Catégorie -->
    <text
      v-if="category"
      x="60"
      y="150"
      :fill="palette.accent"
      fill-opacity="0.7"
      font-family="Inter, sans-serif"
      font-size="22"
      font-weight="500"
      letter-spacing="3"
    >
      {{ category.toUpperCase() }}
    </text>

    <!-- Titre principal (wrap manuel : 3 lignes max) -->
    <foreignObject x="60" y="200" width="800" height="400">
      <div
        xmlns="http://www.w3.org/1999/xhtml"
        :style="{
          color: palette.accent,
          fontFamily: 'Crimson Pro, Georgia, serif',
          fontSize: '64px',
          fontWeight: 700,
          lineHeight: 1.1,
        }"
      >
        {{ title }}
      </div>
    </foreignObject>
  </svg>
</template>
