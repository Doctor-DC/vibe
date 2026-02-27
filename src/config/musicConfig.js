// 音乐播放器配置文件
// 在这里配置你的音乐源 URL

export const musicConfig = {
  // 方式1：使用免费音乐库的公开URL
  // 示例来自 Bensound (https://www.bensound.com/)、ccMixter 等
  tracks: [
    {
      title: 'Your Hand in Mine',
      duration: '4:32',
      // 配置音乐URL - 可以是：
      // 1. 你的服务器上的文件路径
      // 2. 公开的音乐流 URL
      // 3. 数据 URI
      url: '/music/your-hand-in-mine.mp3' // 修改为实际的文件路径
    },
    {
      title: 'How Strange, Innocence',
      duration: '5:33',
      url: '/music/how-strange-innocence.mp3'
    },
    {
      title: 'Remember Me as a Time of Day',
      duration: '3:45',
      url: '/music/remember-me-as-time-of-day.mp3'
    },
    {
      title: 'This Night Has Opened My Eyes',
      duration: '2:58',
      url: '/music/this-night-opened-my-eyes.mp3'
    },
    {
      title: 'The Only Moment We Were Alone',
      duration: '4:12',
      url: '/music/the-only-moment-we-were-alone.mp3'
    }
  ]
}

/*
设置方法：

1. 本地音乐文件：
   - 将 MP3 文件放在 /public/music/ 文件夹中
   - 在 url 字段中设置路径，如 '/music/song.mp3'

2. 远程 URL：
   - 使用任何可公开访问的音乐 URL
   - 示例：'https://example.com/music/song.mp3'
   - 注意：需要启用 CORS 跨域请求

3. 在线音乐服务 API：
   - YouTube Music API（需API密钥）
   - Spotify API（需认证）
   - Last.fm API
   - SoundCloud API

4. 免费音乐资源：
   - Bensound: https://www.bensound.com/
   - Free Music Archive: https://freemusicarchive.org/
   - ccMixter: https://ccmixter.org/
   - Incompetech: https://incompetech.com/

使用本地文件的最简单方法：
1. 在 public 文件夹中创建 music 目录
2. 将你的 MP3 文件复制到里面
3. 更新此配置文件中的 url 路径
*/
