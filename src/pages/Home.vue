<template>
  <div class="home-page">
    <header class="site-header">
      <h1>后摇之声</h1>
      <p class="tagline"></p>
      
      <!-- 音乐播放器 -->
      <MusicPlayer />
      
      <!-- 游戏按钮 -->
      <div class="game-button-section">
        <router-link to="/game" class="game-btn">🎮 看图猜乐队</router-link>
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
                <div class="band-meta">{{ b.origin }}</div>
              </div>
              <div class="band-toggle">{{ b._open ? '收起' : '详细' }}</div>
            </div>

            <div v-if="b._open" class="band-details">
              <!-- 巡演城市信息 -->
              <div v-if="b.played_in_china && b.china_tours && b.china_tours.length" class="band-tours">
                <h4>🎤 中国巡演城市</h4>
                <div class="tours-list">
                  <div v-for="tour in b.china_tours" :key="tour.year" class="tour-item">
                    <span class="tour-year">{{ tour.year }}年：</span>
                    <span class="tour-cities">{{ tour.cities.join(' • ') }}</span>
                  </div>
                </div>
              </div>
              <div v-else-if="b.china_tours && b.china_tours.length" class="band-tours">
                <h4>🎤 曾访问地区</h4>
                <div class="tours-list">
                  <div v-for="tour in b.china_tours" :key="tour.year" class="tour-item">
                    <span class="tour-year">{{ tour.year }}年：</span>
                    <span class="tour-cities">{{ tour.cities.join(' • ') }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="albums" :class="{ collapsed: !b._open }">
              <AlbumCard v-for="alb in b.albums" :key="alb.title" :album="alb" />
            </div>
          </article>
        </div>
      </section>
    </main>

    <footer class="site-footer">
      <p>静态演示站</p>
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
    return { bands: [], q: '' }
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
    fetch('/data-bands.json').then(r => r.json()).then(js => {
      const list = (js && js.bands) ? js.bands : (Array.isArray(js) ? js : []);
      list.forEach(b => { if (typeof b._open === 'undefined') b._open = false });
      this.bands = list;
    }).catch(e => { console.error('加载数据失败', e); this.bands = [] });
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

.band-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  
  h3 {
    margin: 0;
  }
}

/* 巡演信息样式 */
.band-details {
  padding: 0.8rem 1rem;
  background: rgba(100, 150, 255, 0.05);
  border-left: 4px solid rgba(102, 126, 234, 0.5);
  margin: 0.5rem 0;
  border-radius: 6px;
}

.band-tours {
  h4 {
    margin: 0 0 0.6rem 0;
    font-size: 1rem;
    color: #667eea;
  }
}

.tours-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.tour-item {
  display: flex;
  gap: 0.8rem;
  font-size: 0.9rem;
  line-height: 1.3;
  align-items: flex-start;

  .tour-year {
    font-weight: 600;
    color: #764ba2;
    min-width: 70px;
    flex-shrink: 0;
  }

  .tour-cities {
    color: #555;
    word-break: break-word;
  }
}

</style>
