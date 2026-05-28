# Phase 6 — Setup affiliation (Amazon, Awin, AdSense)

Guide complet pour activer les sources de revenus. À suivre dans l'ordre.

---

## 1. Amazon Partenaires France

### A. Inscription (15 min)

1. Aller sur **https://partenaires.amazon.fr**
2. Cliquer "S'inscrire". Connexion avec compte Amazon perso (ou créer un compte pro).
3. Remplir :
   - **Nom du site / app** : `vanlife-comparateur.vercel.app` (ou ton futur domaine `.fr`)
   - **URL** : pareil
   - **Identifiant de magasin préféré** : suggestion `wahid-vanlife-21` (sera ton `partner_tag`)
   - **Description du site** : "Comparatif et guides d'achat pour matériel vanlife"
   - **Catégories** : Sports & Loisirs, Bricolage, High-Tech
   - **Sources de trafic** : SEO Google
4. Validation par Amazon : 24-48h (compte créé, mais "en attente")

### B. Activation finale

Pour que le compte passe en "Validé" et débloquer les commissions :
- **3 ventes minimum en 180 jours** via tes liens
- Sinon : compte fermé sans préavis

**Stratégie** : partager 1-2 liens à des amis vanlifers pour générer les premières ventes test rapidement (achat anodin OK, panier > 0,50€).

### C. Récupération du tag

Une fois inscrit, ton `partner_tag` est visible dans :
- Menu **Compte → Paramètres du compte → Identifiants de magasin**
- Format : `xxxxxx-21` (le suffixe `-21` = marketplace France)

**Exemple** : `wahid-vanlife-21`

### D. Configuration dans le projet

Édite `pipeline/.env` (créer si pas existe depuis `.env.example`) :

```bash
AMAZON_PARTNER_TAG=wahid-vanlife-21
NUXT_PUBLIC_AMAZON_PARTNER_TAG=wahid-vanlife-21
```

Le composant `<AmazonCta>` injecte ce tag automatiquement dans tous les liens des articles. Tu n'as **rien à modifier dans les .md**.

Pour le dev local Nuxt, créer aussi `frontend/.env` :

```bash
NUXT_PUBLIC_AMAZON_PARTNER_TAG=wahid-vanlife-21
```

### E. Récupération des ASIN produit

Pour chaque produit cité dans un article, l'`ASIN` est dans l'URL Amazon :

```
https://www.amazon.fr/dp/B0CKQXQXQX/...
                       ^^^^^^^^^^
                       ASIN (10 caractères)
```

**Outil pratique** : extension Chrome **SiteStripe** (proposée par Amazon Partenaires une fois inscrit). Affiche un bandeau en haut des fiches produit avec génération automatique de liens affiliés.

### F. Taux de commission Amazon France 2026

| Catégorie | Commission |
|---|---|
| Bricolage et Outils | **6%** |
| Sports et Loisirs | 3% |
| High-Tech (informatique, électronique) | 3% |
| Auto et Moto | **4-6%** |
| Cuisine et Maison | 4-6% |

→ La majorité du matos vanlife (batteries, panneaux, chauffages, frigos) tombe en **Bricolage** ou **Auto/Moto** = **4-6%**.

---

## 2. Awin (Cdiscount, ManoMano, Decathlon, etc.)

### A. Inscription (20 min)

1. Aller sur **https://www.awin.com/fr/**
2. "Rejoindre Awin" comme **éditeur** (Publisher)
3. Frais : **5$ (≈5€) à l'inscription**, **remboursés** après validation du compte par Awin (1-2 semaines)
4. Remplir formulaire :
   - Type de site : Comparateur / Guide d'achat
   - Catégories : Maison, Auto, Sport, Outdoor
   - Trafic estimé : sois honnête (peut être < 1000/mois au début)

### B. Validation

Awin examine ton site manuellement (1-2 semaines). Critères :
- Site opérationnel (pas en construction)
- Contenu original
- Mentions légales + politique de confidentialité présentes (✓ déjà fait Phase 0)
- Politique d'affiliation transparente (✓ déjà fait)

### C. Demandes d'affiliation marchands

Une fois validé, faire les demandes une par une dans **Awin → Programmes → Recherche** :

**Marchands vanlife prioritaires** :
- **Cdiscount** (commission 4-7%)
- **ManoMano** (commission 4-8%)
- **Decathlon** (commission 5-7%)
- **Naturabuy** (occasion outdoor, 5%)
- **Norauto / Feu Vert** (4-6%, pour pièces auto)
- **CampingGaz / Lampa** (5-8%)

Chaque demande = approbation par le marchand (24h-2 semaines).

### D. Récupération publisher_id

Dans **Awin → Compte → Mon profil** : ton `Publisher ID` (6 chiffres).

```bash
# pipeline/.env
AWIN_PUBLISHER_ID=123456
NUXT_PUBLIC_AWIN_PUBLISHER_ID=123456
```

### E. Génération des liens Awin

Format des liens Awin :
```
https://www.awin1.com/cread.php?awinmid={MERCHANT_ID}&awinaffid={PUBLISHER_ID}&p={DESTINATION_URL_ENCODED}
```

- `awinmid` = ID du marchand (Cdiscount = 14916, ManoMano = 15723, Decathlon = 14728)
- `awinaffid` = ton publisher_id
- `p` = URL produit du marchand (URL-encodée)

Awin propose un **Link Builder** dans son interface pour générer ces liens facilement.

---

## 3. Programmes directs constructeurs (commissions max)

Une fois traffic > 1000/mois, écrire directement aux marques. Commissions souvent **2-3× supérieures** à Amazon.

| Marque | Programme | Commission | URL |
|---|---|---|---|
| **EcoFlow** | EcoFlow Affiliate | **8-12%** | https://www.ecoflow.com/affiliate |
| **Bluetti** | Bluetti Affiliate | **6-10%** | https://www.bluettipower.com/pages/affiliate-program |
| **Jackery** | Jackery Affiliate | **8%** | https://www.jackery.com/pages/affiliate |
| **Victron Energy** | Distributeur agréé | Variable | Via distributeurs (Energie Mobile, ...) |
| **Renogy** | Renogy Affiliate | **5-8%** | https://www.renogy.eu/pages/affiliate |
| **Goal Zero** | Goal Zero Affiliate | **6%** | Via Awin |
| **Bestway / Lay-Z-Spa** | Affilae | 5-7% | https://affilae.com |

**Stratégie** : commencer Amazon + Awin. Programmes directs = bonus quand l'audience est là.

---

## 4. Google AdSense (Phase 9, plus tard)

**Critères Google** pour accepter ton site :
- Min ~20 articles publiés, qualité humaine
- Min 100-300 visites/jour pendant 1 mois
- Site complet (mentions légales ✓, à propos ✓, contact ✓)
- Trafic organique vérifiable

**Inscription** : https://www.google.com/adsense

**Validation** : 1-3 semaines (parfois 1 mois). Beaucoup de refus en 2026 pour sites jeunes.

**Alternatives meilleur RPM** (à activer une fois 10k+ visites/mois) :
- **Ezoic** (min ~10k visites/mois) — RPM 2× AdSense
- **Mediavine** (min 50k visites/mois) — RPM 3× AdSense
- **Raptive** (ex-AdThrive) — premium tier

Pour Phase 0/1/6 : **on s'en occupe pas**. Trop tôt.

---

## 5. Déclaration fiscale (obligation légale)

**Dès le 1er euro perçu** :

### Option 1 : Micro-BNC (recommandé pour démarrer)

- Statut auto-entrepreneur déjà existant ? Bingo.
- Sinon : créer via `autoentrepreneur.urssaf.fr` (5 min, gratuit)
- Activité principale : "Conseil en stratégie web" ou "Création de contenu en ligne"
- Plafond : **77 700€/an** de chiffre d'affaires
- Cotisations : **21,2%** du CA (URSSAF + impôt forfaitaire)
- Déclaration : trimestrielle, simple

### Option 2 : Micro-BIC (si revenu pub plus que conseil)

- Plafond : **188 700€/an**
- Cotisations : 12,8% (vente bien) ou 22,2% (prestation service)

→ Demander à un comptable lors du premier dépassement 30k€/an pour optimiser (passer en EI ou SASU).

### Comment déclarer Amazon / Awin / AdSense

Ces plateformes émettent un **récapitulatif annuel** des sommes versées. À reporter dans la déclaration URSSAF trimestrielle puis annuelle (formulaire 2042-C-PRO en France).

⚠️ **Pas de TVA si CA < 39 100€/an** (franchise micro). Au-delà, facturer + reverser la TVA.

---

## 6. Checklist activation

- [ ] Compte Amazon Partenaires créé, `partner_tag` récupéré
- [ ] `AMAZON_PARTNER_TAG` + `NUXT_PUBLIC_AMAZON_PARTNER_TAG` dans `.env`
- [ ] Compte Awin créé (en attente validation)
- [ ] Auto-entrepreneur créé / activé
- [ ] 1er lien d'affiliation testé en cliquant depuis incognito et vérifié dans tableau Amazon (24h)
- [ ] 3 ventes en 180 jours (validation finale Amazon)
- [ ] Première commission perçue (virement bancaire mensuel)

---

## 7. Quand on installe quoi dans le code

| Step | À installer | Quand |
|---|---|---|
| 1 | `NUXT_PUBLIC_AMAZON_PARTNER_TAG` dans `frontend/.env` | Dès inscription Amazon faite |
| 2 | `AMAZON_PARTNER_TAG` dans `pipeline/.env` | Idem (pipeline Phase 4+) |
| 3 | Vrais `asin` dans articles `.md` (remplacer `B0EXAMPLE`) | Au fur et à mesure |
| 4 | `NUXT_PUBLIC_AWIN_PUBLISHER_ID` | Dès validation Awin |
| 5 | Composant `<AwinCta>` dans articles | Dès 1ère affiliation marchand approuvée |
| 6 | Snippet AdSense `<script>` dans `app.vue` | Phase 9 |
| 7 | `ads.txt` dans `public/` | Phase 9 (AdSense) |

---

## Recap honnête sur les revenus

- **Mois 1-3** : 0€ — site indexation Google en cours
- **Mois 4-6** : 10-100€/mois — premières ventes affiliés Amazon
- **Mois 7-12** : 100-1000€/mois — montée trafic SEO
- **Mois 12+** : 500-3000€/mois (objectif réaliste du doc projet)

**Pas de jackpot**. Le truc fait revenu passif **uniquement si tu publies régulièrement** (2 articles/sem) et **maintiens la qualité** (relecture humaine = critique).
