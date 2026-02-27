#!/bin/bash
# 批量压缩图片脚本

echo "🖼️  开始压缩图片..."
echo ""

# 检查是否安装了ImageMagick
if ! command -v convert &> /dev/null; then
    echo "需要安装ImageMagick"
    echo "运行: brew install imagemagick"
    exit 1
fi

# 压缩所有JPG和PNG文件
find public/images -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | while read file; do
    original_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    
    # 创建临时文件
    temp_file="${file}.tmp"
    
    # 压缩图片（降低质量到85%，缩小尺寸）
    convert "$file" -quality 85 -resize 1920x1440 "$temp_file"
    
    new_size=$(stat -f%z "$temp_file" 2>/dev/null || stat -c%s "$temp_file" 2>/dev/null)
    
    # 如果压缩后更小，就替换原文件
    if [ $new_size -lt $original_size ]; then
        mv "$temp_file" "$file"
        original_kb=$((original_size / 1024))
        new_kb=$((new_size / 1024))
        percent=$((100 - (new_size * 100 / original_size)))
        echo "✅ $(basename "$file")"
        echo "   $(printf '%5s' "$original_kb")KB → $(printf '%5s' "$new_kb")KB (节省 $percent%)"
    else
        rm "$temp_file"
        echo "⊘ $(basename "$file") (已是最优)"
    fi
done

echo ""
echo "✅ 压缩完成！"
echo "下一步: npm run build && git add -A && git commit -m 'Optimize: compress images' && git push"
