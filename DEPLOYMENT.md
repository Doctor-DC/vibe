# 部署到Vercel指南

## ⚡ 部署前性能检查清单

**必须运行**：
```bash
chmod +x pre-deploy-check.sh
./pre-deploy-check.sh
```

这会检查：
- ✅ 所有静态资源位置是否正确
- ✅ **文件大小是否合理** ⭐ 关键
- ✅ Vite构建是否成功
- ✅ `dist/` 输出是否完整

### 文件大小标准

| 类型 | 建议限制 | 超过该大小需要压缩 |
|------|---------|-------------------|
| 单个图片 | < 500KB | > 1MB ⚠️ |
| **总图片** | < 10MB | > 10MB ❌ |
| JSON文件 | < 100KB | > 500KB ❌ |
| 音乐文件 | < 15MB | > 20MB ❌ |

## 常见问题排查

### ❌ 界面加载慢（图片大）
**原因：** 图片文件过大（超过1MB）
**标志：** 无法立即看到图片，需要等待几秒

**解决步骤：**
1. 运行 `./pre-deploy-check.sh` 识别超大图片
2. 压缩图片（推荐使用 TinyJPG 或 ImageCompressor）
3. 替换 `/public/images/` 中的文件
4. 重新构建并推送

**压缩工具：**
- https://tinyjpg.com （推荐，快速）
- https://imagecompressor.com （无限免费）
- 本地脚本：`python3 compress-images.py`

### ❌ 图片无法显示
**原因：** 图片不在 `/public/images` 目录
**解决：** 
```bash
mv images public/images
npm run build && git add -A && git commit -m "move images to public" && git push
```

### ❌ 数据（JSON）无法加载
**原因：** JSON文件不在 `/public/` 目录
**解决：** 数据文件必须在 `/public/data-bands.json`

### ✅ 部署规则

**Vercel只提供 `/public` 目录下的文件！**

| 目录 | 内容 | 部署时 |
|------|------|--------|
| `/src` | Vue组件代码 | 被Vite编译 |
| **/public** | **所有静态资源** | **直接复制** |
| `/dist` | 构建输出 | Vercel部署此目录 |

## 推送到GitHub并自动部署

```bash
git add -A
git commit -m "描述你的更改"
git push
```

Vercel会自动检测GitHub推送，在1-2分钟内完成部署！
