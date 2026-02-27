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
  echo "⚠️  警告: images/ 不在 public/ 下"
fi
if [ ! -f "public/data-bands.json" ]; then
  echo "⚠️  警告: bands.json 不在 public/ 下"
fi
if [ ! -d "public/music" ]; then
  echo "⚠️  警告: music/ 不在 public/ 下"
fi

# 3. 检查图片文件大小（超过1MB警告，超过5MB错误）
echo "✓ 检查图片文件大小..."
echo "  📏 建议限制: 单个图片 < 500KB, 总大小 < 10MB"
echo ""

has_warning=0
total_size=0

find public/images -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) 2>/dev/null | while read file; do
  size_bytes=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
  size_mb=$(echo "scale=2; $size_bytes / 1048576" | bc)
  size_kb=$(echo "scale=0; $size_bytes / 1024" | bc)
  filename=$(basename "$file")
  
  total_size=$((total_size + size_bytes))
  
  if [ "$size_bytes" -gt 5242880 ]; then
    echo "   ❌ $filename (${size_mb}MB) - 太大！需要压缩"
    has_warning=1
  elif [ "$size_bytes" -gt 1048576 ]; then
    echo "   ⚠️  $filename (${size_mb}MB) - 考虑压缩"
    has_warning=1
  else
    echo "   ✅ $filename (${size_kb}KB)"
  fi
done

# 计算总大小
total_images_size=$(find public/images -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -exec stat -f%z {} \; 2>/dev/null | awk '{sum+=$1} END {print sum}')
total_images_mb=$(echo "scale=1; $total_images_size / 1048576" | bc)
echo ""
echo "  📊 图片总大小: ${total_images_mb}MB (建议 < 10MB)"

# 4. 构建检查
echo ""
echo "✓ 运行构建..."
npm run build
if [ $? -ne 0 ]; then
  echo "❌ 构建失败"
  exit 1
fi

# 5. 检查dist输出
echo "✓ 检查构建输出..."
if [ ! -d "dist/assets" ]; then
  echo "❌ dist/assets/ 不存在"
  exit 1
fi

# 6. 检查dist中的文件大小
dist_size=$(du -sh dist 2>/dev/null | awk '{print $1}')
echo "  📦 构建输出大小: $dist_size"

echo ""
if [ $has_warning -eq 1 ]; then
  echo "⚠️  警告: 发现过大的图片文件，建议先压缩"
  echo "  运行: python3 compress-images.py"
  echo ""
fi

echo "✅ 检查完成！"
echo ""
echo "下一步："
echo "  npm run build"
echo "  git add -A && git commit -m '更新内容'"  
echo "  git push"

