#!/usr/bin/env python3
"""
批量压缩图片脚本
使用PIL库（Python内置支持）
"""

import os
from PIL import Image
import glob

def compress_images(quality=85, max_width=1920, max_height=1440):
    """压缩public/images目录下的所有图片"""
    
    print("🖼️  开始压缩图片...\n")
    
    # 查找所有图片文件
    image_files = glob.glob("public/images/**/*.jpg", recursive=True) + \
                  glob.glob("public/images/**/*.jpeg", recursive=True) + \
                  glob.glob("public/images/**/*.png", recursive=True)
    
    total_saved = 0
    
    for image_path in sorted(image_files):
        try:
            # 获取原始文件大小
            original_size = os.path.getsize(image_path)
            original_kb = original_size / 1024
            
            # 打开和压缩图片
            with Image.open(image_path) as img:
                # 转换RGBA到RGB（JPG不支持透明度）
                if img.mode in ('RGBA', 'LA', 'P'):
                    # 创建白色背景
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # 如果图片很大，缩小尺寸
                img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                
                # 保存（压缩质量）
                if image_path.lower().endswith('.png'):
                    img.save(image_path, 'PNG', optimize=True)
                else:
                    img.save(image_path, 'JPEG', quality=quality, optimize=True)
            
            # 计算新大小和节省空间
            new_size = os.path.getsize(image_path)
            new_kb = new_size / 1024
            saved = original_size - new_size
            saved_kb = saved / 1024
            percent = int((saved / original_size) * 100) if saved > 0 else 0
            
            if percent > 10:  # 只显示节省超过10%的
                print(f"✅ {os.path.basename(image_path)}")
                print(f"   {original_kb:.0f}KB → {new_kb:.0f}KB (节省 {percent}%)")
                total_saved += saved
            else:
                print(f"⊘ {os.path.basename(image_path)} (已是最优)")
                
        except Exception as e:
            print(f"❌ {image_path}: {str(e)}")
    
    print(f"\n✅ 压缩完成!")
    print(f"📊 总计节省: {total_saved / 1024 / 1024:.1f}MB")
    print("\n下一步:\n  npm run build")
    print("  git add -A && git commit -m 'Optimize: compress images'")
    print("  git push")

if __name__ == "__main__":
    compress_images()
