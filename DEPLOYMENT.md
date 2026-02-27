# 部署到Vercel指南

## 快速部署检查清单

在部署前，**务必运行检查脚本**：

```bash
chmod +x pre-deploy-check.sh
./pre-deploy-check.sh
```

这会检查：
- ✅ 所有静态资源（图片、JSON、音乐）是否在 `/public` 目录
- ✅ Vite构建是否成功
- ✅ `dist/` 中是否包含所有必需的文件

## 常见问题排查

### ❌ 图片无法显示
**原因：** 图片不在 `/public/images` 目录
**解决：** 
```bash
mv images public/images
npm run build
git add -A && git commit -m "move images to public" && git push
```

### ❌ 数据（JSON）无法加载
**原因：** JSON文件不在 `/public/` 目录
**解决：** 
```bash
mv data/bands.json public/data-bands.json
# 并更新代码中的路径
```

### ❌ 音乐无法播放
**原因：** 音乐文件不在 `/public/music/` 目录
**解决：** 
```bash
mkdir -p public/music
mv music/* public/music/
```

### ✅ 记住的规则

**Vercel只提供 `/public` 目录下的静态文件！**

- `/src` - Vue组件（会被Vite处理）
- **`/public` - 所有静态资源（图片、JSON、音乐等）**
- `dist/` - 构建输出（不要手动编辑）
