# Vibe — 后摇乐队与唱片展示站

这是一个简单静态站点示例，用于展示后摇（post-rock）乐队与他们的专辑。

本地查看：

```bash
# 在项目根目录运行一个简单静态服务器（推荐）
python3 -m http.server 8000
# 或者使用 Node.js 的 http-server
npx http-server -c-1 .
```

然后在浏览器打开 `http://localhost:8000`。

数据文件位于 `data/bands.json`，可以在此补全或修改乐队信息与专辑目录。前端使用 `src/App.vue`（Vite + Vue2）或可直接打开 `index.html` 以查看预编译模板；样式为 `styles.css`。

如果你希望我把某些乐队的完整唱片表（所有专辑与曲目）填入 `data/bands.json`，请列出想要的乐队，我可以为其补全条目。
