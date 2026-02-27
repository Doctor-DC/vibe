# Vibe — 后摇乐队与唱片展示站

这是一个基于 Vue2 + Vite 的静态站点。

## 本地开发

```bash
npm install
npm run dev
```

## 生产构建

```bash
npm run build
```

构建产物目录：`dist/`

## 部署

项目已包含：

- `vercel.json`
- `netlify.toml`

### 1) Vercel（推荐）

```bash
npm i -g vercel
vercel --prod
```

Vercel 会自动执行 `npm run build` 并发布 `dist/`。

### 2) Netlify

- Build command: `npm run build`
- Publish directory: `dist`

也可以用 Netlify CLI：

```bash
npm i -g netlify-cli
netlify deploy --prod
```

### 3) 任意静态服务器

上传 `dist/` 目录内容即可（Nginx / OSS / CDN / GitHub Pages 等）。
