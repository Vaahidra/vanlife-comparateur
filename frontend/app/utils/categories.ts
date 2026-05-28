/**
 * Métadonnées des catégories — source unique de vérité.
 * Utilisé par le layout, les pages catégories, le sitemap.
 */

export interface Category {
  slug: string
  label: string
  description: string
}

export const CATEGORIES: Category[] = [
  {
    slug: 'energie',
    label: 'Énergie',
    description: 'Batteries lithium, panneaux solaires, convertisseurs, stations électriques portables.',
  },
  {
    slug: 'cuisine',
    label: 'Cuisine',
    description: 'Frigos 12V à compression, plaques de cuisson, kits cuisine compacts.',
  },
  {
    slug: 'confort',
    label: 'Confort',
    description: 'Chauffages stationnaires diesel, douches portables, toilettes sèches.',
  },
  {
    slug: 'securite',
    label: 'Sécurité',
    description: 'Alarmes, GPS trackers, cadenas, surveillance fourgon.',
  },
  {
    slug: 'amenagement',
    label: 'Aménagement',
    description: 'Isolation, mobilier modulable, organisation, rangements vanlife.',
  },
]

export function getCategoryBySlug(slug: string): Category | undefined {
  return CATEGORIES.find(c => c.slug === slug)
}
