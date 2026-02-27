#!/bin/bash
# 部署前检查清单

echo "🔍 Vibe项目部署前检查..."
echo ""

# 1. 检查关键目录和文件
echo "✓ 检查目录结构..."
if [ ! -d "public" ]; then
  echo "❌ 缺少 public/ 目录"
  exit 1
fi
if [ ! -f "vite.config.js" ]; then
  echo "❌ 缺少 vite.config.js"
  exit 1
fi

# 2. 检查静态资源是否在public目录
echo "✓ 检查静态资源位置..."
if [ ! -d "public/images" ]; then
  echo "⚠️  警告: images/ 不在 public/ 下 (会导致图片无法显示)"
fi
if [ ! -f "public/data-bands.json" ]; then
  echo "⚠️  警告: bands.json 不在 public/ 下 (会导致数据无法加载)"
fi
if [ ! -d "public/music" ]; then
  echo "⚠️  警告: music/ 不在 public/ 下 (会导致音乐无法播放)"
fi

# 3. 构建检查
echo "✓ 运行构建..."
npm run build
if [ $? -ne 0 ]; then
  echo "❌ 构建失败"
  exit 1
fi

# 4. 检查dist输出
echo "✓ 检查构建输出..."
if [ ! -d "dist/assets" ]; then
  echo "❌ dist/assets/ 不存在"
  exit 1
fi

# 5. 检查关键文件是否被复制到dist
if [ ! -f "dist/data-bands.json" ]; then
  echo "⚠️  警告: dist/data-bands.json 不存在"
fi
if [ ! -d "dist/images" ]; then
  echo "⚠️  警告: dist/images/ 不存在"
fi
if [ ! -d "dist/music" ]; then
  echo "⚠️  警告: dist/music/ 不存在"
fi

echo ""
echo "✅ 检查完成！可以安全部署"
echo ""
echo "下一步："
echo "  git add -A"
echo "  git commit -m '更新内容'"  
echo "  git push"
