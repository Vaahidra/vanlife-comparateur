# Decap CMS — Admin

Interface web pour relire/éditer les articles générés par le pipeline Python.

## Accès

- **Local** : http://localhost:3000/admin/
- **Prod** : https://<ton-projet>.vercel.app/admin/

## Setup OAuth GitHub (Phase 1)

Decap a besoin d'un OAuth proxy pour s'authentifier à GitHub depuis le navigateur.

### 1. Créer l'OAuth App GitHub

1. Aller sur https://github.com/settings/developers → New OAuth App
2. **Application name** : `Vanlife Comparateur CMS`
3. **Homepage URL** : `https://<ton-projet>.vercel.app`
4. **Authorization callback URL** : `https://<oauth-proxy>/callback`
5. Récupérer `Client ID` + `Client Secret`

### 2. Déployer l'OAuth proxy

Option A — fork + deploy [`vencax/netlify-cms-github-oauth-provider`](https://github.com/vencax/netlify-cms-github-oauth-provider) sur Vercel.

Option B — écrire une route serverless dans le projet Nuxt (`server/api/auth/`).

### 3. Mettre à jour `config.yml`

```yaml
backend:
  name: github
  repo: TON_USERNAME/vanlife-comparateur
  branch: main
  base_url: https://ton-oauth-proxy.vercel.app
```

## Setup local (sans OAuth, dev uniquement)

Pour bosser en local sans setup OAuth :

```bash
cd frontend
npx decap-server &       # démarre le proxy local sur :8081
npm run dev              # Nuxt sur :3000
```

Dans `config.yml`, commenter `backend: github` et activer :

```yaml
backend:
  name: proxy
  proxy_url: http://localhost:8081/api/v1
  branch: main
```

## Workflow

1. Pipeline Python génère `content/articles/<slug>.md` avec `draft: true`
2. Notification Telegram : "Article généré, à relire"
3. User va sur `/admin/`, ouvre l'article, retouche
4. Décocher "Brouillon" → publish → commit auto sur `main` → rebuild Vercel
