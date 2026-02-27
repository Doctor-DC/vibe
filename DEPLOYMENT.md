# 部署到Vercel指南

## 部署步骤

### 方案A：通过GitHub+Vercel（推荐，自动化）

1. **初始化Git仓库**
```bash
cd /Users/wuduochao/vibe
git init
git add .
git commit -m "Initial commit"
```

2. **创建GitHub仓库**
   - 访问 https://github.com/new
   - 创建新仓库 `vibe`
   - 按照指示推送本地代码到GitHub

3. **部署到Vercel**
   - 访问 https://vercel.com
   - 用GitHub账号登录
   - 点击 "Import Project"
   - 选择你的 `vibe` 仓库
   - 点击 "Deploy"
   - 等待部署完成（1-2分钟）

完成后，你会获得一个公网URL，例如：`https://vibe.vercel.app`

### 方案B：使用Vercel CLI（快速）

1. **安装Vercel CLI**
```bash
npm install -g vercel
```

2. **部署**
```bash
cd /Users/wuduochao/vibe
vercel
```

3. 按照提示：
   - 是否继续？选择 `y`
   - 项目名称？默认 `vibe`
   - 项目路径？默认
   - 是否修改设置？选择 `n`

完成后会显示公网URL。

## 项目已构建

生产版本已在 `/Users/wuduochao/vibe/dist` 目录，Vercel会自动使用。

## 访问方式

部署完成后，同事可以通过以下方式访问：
- 访问Vercel提供的URL（例如 `vibe.vercel.app`）
- 分享给任何人，他们都能通过公网访问

## 注意事项

- 音乐文件 `/public/music/your-hand-in-mine.mp3` 会自动上传
- 页面背景、游戏功能都会正常工作
- 后续修改代码后，自动部署（如果使用GitHub+Vercel方案）
