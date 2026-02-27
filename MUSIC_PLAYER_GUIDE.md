# 🎵 音乐播放器使用指南

## 功能概述

本项目的音乐播放器现在已升级为**完整功能版本**，支持：

- ✅ 真实音频文件播放
- ✅ 播放进度控制
- ✅ 音量调节
- ✅ 曲目列表管理
- ✅ 重复模式（无重复、重复全部、重复单曲）
- ✅ 缓冲进度显示
- ✅ 文件上传功能

## 配置音乐源 - 3种方法

### 方法1️⃣：上传本地文件（最简单）

1. **打开应用的主页**
   - 向下滚动找到"📁 上传音乐文件："区域

2. **点击上传区域选择文件**
   - 支持格式：MP3、OGG、WAV、FLAC 等
   - 可选择多个文件
   - 文件名会自动匹配到曲目列表

3. **开始播放**
   - 上传后直接点击 ▶ 按钮即可播放

### 方法2️⃣：放置文件到项目目录

1. **创建音乐文件夹**
   ```bash
   mkdir -p public/music
   ```

2. **复制音乐文件**
   ```bash
   cp your-songs/*.mp3 public/music/
   ```

3. **编辑配置文件**
   ```
   src/config/musicConfig.js
   ```
   
   修改 URL：
   ```javascript
   {
     title: 'Your Hand in Mine',
     duration: '4:32',
     url: '/music/your-hand-in-mine.mp3'  // ← 修改这里
   }
   ```

### 方法3️⃣：使用在线音乐 URL

在 `src/config/musicConfig.js` 中填写公开的音乐 URL：

```javascript
{
  title: 'Your Hand in Mine',
  url: 'https://example.com/music/song.mp3'
}
```

**推荐的免费音乐资源：**
- 🎵 **Bensound**: https://www.bensound.com/
- 🎵 **Free Music Archive**: https://freemusicarchive.org/
- 🎵 **ccMixter**: https://ccmixter.org/
- 🎵 **Incompetech**: https://incompetech.com/

## 使用说明

### 播放控制
- **⏮ 按钮**: 上一曲（如果播放时间超过2秒，则重新开始当前曲）
- **▶/⏸ 按钮**: 播放/暂停
- **⏭ 按钮**: 下一曲
- **🔁 按钮**: 切换重复模式（无重复 → 重复全部 → 重复单曲）

### 进度条
- 点击进度条可以快速跳转到指定位置
- 灰色部分表示已缓冲的内容

### 音量控制
- 使用滑块可以调节音量（0-100%）
- 显示当前音量百分比

### 曲目列表
- 点击列表中的曲目可以直接切换
- 当前播放的曲目会高亮显示（紫色背景）
- 正在播放的曲目有播放指示符

## 常见问题

### Q: 上传了文件但无法播放？
**A:** 
- 检查文件格式是否为音频文件
- 确保浏览器支持该音频格式
- 查看浏览器控制台（F12）是否有错误信息

### Q: 播放出现"播放失败"错误？
**A:**
- 确保音乐文件有效且完整
- 检查网络连接（如果使用在线 URL）
- 尝试不同的浏览器
- 检查文件是否被浏览器 CORS 策略阻止

### Q: 如何添加更多曲目？
**A:**
在 `src/components/MusicPlayer.vue` 中的 `data()` 函数里，修改 `tracks` 数组：
```javascript
tracks: [
  { title: '曲目1', duration: '4:32', url: '/music/song1.mp3' },
  { title: '曲目2', duration: '5:00', url: '/music/song2.mp3' },
  // 添加更多...
]
```

### Q: 为什么不能播放 YouTube 或 Spotify 的音乐？
**A:** 这些平台有版权保护和 DRM 限制，无法直接调用。需要：
- 使用这些平台的 API（需要 API 密钥和用户认证）
- 或使用其他合法的音乐源

## 技术细节

### 音频格式支持
取决于浏览器支持，通常包括：
- MP3 (MPEG-3)
- OGG (Ogg Vorbis)
- WAV (PCM)
- FLAC (如浏览器支持)
- M4A (AAC)

### 浏览器兼容性
- ✅ Chrome 55+
- ✅ Firefox 50+
- ✅ Safari 11+
- ✅ Edge 79+

## 开发者信息

### 相关文件
- `src/components/MusicPlayer.vue` - 播放器组件
- `src/config/musicConfig.js` - 音乐配置文件
- `public/music/` - 本地音乐文件存储位置

### Vue 组件方法
```javascript
// 导入音乐文件
$refs.audioPlayer.src = 'path/to/music.mp3'

// 播放/暂停
$refs.audioPlayer.play()
$refs.audioPlayer.pause()

// 跳转到指定位置
$refs.audioPlayer.currentTime = 120 // 跳转到 2 分钟
```

---

**祝你享受音乐！** 🎶
