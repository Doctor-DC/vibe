<template>
  <div class="home-page">
    <header class="site-header">
      <h1>后摇之声 • Vibe</h1>
      <p class="tagline">介绍后摇乐队与他们的全部专辑</p>
      
      <!-- 音乐播放器 -->
      <MusicPlayer />
      
      <!-- 游戏按钮 -->
      <div class="game-button-section">
        <router-link to="/game" class="game-btn">🎮 乐队猜测游戏</router-link>
      </div>
    </header>

    <main>
      <section id="bands-list" class="container">
        <div class="toolbar">
          <h2>乐队列表</h2>
          <input v-model="q" type="search" placeholder="搜索乐队或专辑" />
        </div>

        <div id="bands">
          <article class="band" v-for="b in filteredBands" :key="b.name">
            <div class="band-header" @click="toggle(b)">
              <img v-if="b.image" :src="b.image" :alt="b.name" class="band-image" />
              <div class="band-info">
                <h3>{{ b.name }}</h3>
                <div class="band-meta">{{ b.origin ? (b.origin + ' • ') : '' }}{{ b.played_in_china ? ('来过中国：' + (b.china_years && b.china_years.length ? b.china_years.join(', ') : '年份未知')) : '无来华演出记录' }}</div>
              </div>
              <div class="band-toggle">{{ b._open ? '收起' : '详细' }}</div>
            </div>

            <div class="albums" :class="{ collapsed: !b._open }">
              <AlbumCard v-for="alb in b.albums" :key="alb.title" :album="alb" />
            </div>
          </article>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <p>静态演示站 — Vite + Vue2</p>
    </footer>
  </div>
</template>

<script>
import AlbumCard from '../components/AlbumCard/AlbumCard.vue'
import MusicPlayer from '../components/MusicPlayer.vue'

export default {
  name: 'Home',
  components: { AlbumCard, MusicPlayer },
  data() {
    return { bands: [], q: '', triangles: [] }
  },
  computed: {
    filteredBands() {
      const q = (this.q || '').trim().toLowerCase();
      if (!q) return this.bands;
      return this.bands.filter(b => {
        const inName = b.name && b.name.toLowerCase().includes(q);
        const inAlbums = (b.albums || []).some(a => (a.title || '').toLowerCase().includes(q));
        return inName || inAlbums;
      });
    }
  },
  methods: {
    toggle(b) { this.$set(b, '_open', !b._open) }
  },
  created() {
    fetch('/data/bands.json').then(r => r.json()).then(js => {
      const list = (js && js.bands) ? js.bands : (Array.isArray(js) ? js : []);
      list.forEach(b => { if (typeof b._open === 'undefined') b._open = false });
      this.bands = list;
    }).catch(e => { console.error('加载数据失败', e); this.bands = [] });
    // create triangles fixed on left side
    // palette: light blue, white, purple
    const palette = ['rgba(100,180,255,0.95)','rgba(255,255,255,0.95)','rgba(178,153,255,0.95)']
    const count = 3
    this.triangles = Array.from({length: count}).map((_, idx)=>{
      const positions = [
        { left: 8, top: 15 },    // top left
        { left: 12, top: 45 },   // middle left
        { left: 6, top: 72 }     // bottom left
      ]
      return {
        left: positions[idx].left,
        top: positions[idx].top,
        size: Math.round(60 + Math.random()*40),
        rot: Math.round(-40 + Math.random()*80),
        color: palette[idx % palette.length],
        stroke: (0.9 + Math.random()*0.7).toFixed(2)
      }
    })
  }
}
</script>

<style scoped lang="scss">
@import '../App/App.scss';

.game-button-section {
  margin-top: 1rem;
  display: flex;
  justify-content: center;

  .game-btn {
    padding: 0.75rem 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    &:active {
      transform: translateY(0);
    }
  }
}
</style>
