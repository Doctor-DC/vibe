<template>
  <div class="mini-player" v-if="track">
    <div class="mini-player-content">
      <img v-if="track && track.image" :src="track.image" :alt="track.title" class="mini-cover" />
      <div class="mini-info">
        <div class="mini-title">{{ track ? track.title : '加载中...' }}</div>
        <div class="mini-time">{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</div>
      </div>
      <button @click="togglePlay" class="mini-play-btn">{{ isPlaying ? '⏸' : '▶' }}</button>
    </div>
    <div class="mini-progress">
      <div class="mini-progress-bar" @click="seekTo" :style="{ width: progress + '%' }"></div>
    </div>
    <audio ref="audio" @timeupdate="updateTime" @loadedmetadata="setDuration" @ended="stopPlay" @play="play" @pause="pause" />
  </div>
</template>

<script>
import { musicStore } from '../store/musicStore'

export default {
  name: 'MiniPlayer',
  data() {
    return {
      isPlaying: false,
      currentTime: 0,
      duration: 0,
      track: {
        title: 'Your Hand in Mine',
        artist: 'Explosions in the Sky',
        album: 'The Earth Is Not a Cold Dead Place',
        duration: '4:32',
        url: '/music/your-hand-in-mine.mp3',
        image: '/images/albums/explosions-in-the-sky__the-earth-is-not-a-cold-dead-place.jpg'
      },
      audioRef: null
    }
  },
  computed: {
    progress() {
      return this.duration > 0 ? (this.currentTime / this.duration) * 100 : 0
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.audioRef = this.$refs.audio
      if (!this.audioRef) return
      
      // 从musicStore恢复当前播放的歌曲信息
      const state = musicStore.getState()
      
      if (state.track && state.track.url) {
        // 使用当前正在播放的歌曲
        this.track = state.track
      } else {
        // 使用data中的默认值
        this.track = this.$data.track
      }
      
      // 设置音频源
      if (this.track && this.track.url) {
        this.audioRef.src = this.track.url
      }
      
      // 恢复播放位置
      if (state.currentTime > 0) {
        this.currentTime = state.currentTime
        this.audioRef.currentTime = state.currentTime
      }
      
      // 恢复播放状态
      if (state.duration > 0) {
        this.duration = state.duration
      }
      
      // 如果之前在播放，继续播放
      if (state.isPlaying) {
        this.isPlaying = true
        this.audioRef.play().catch(err => console.warn('自动播放被阻止:', err))
      }
    })
  },
  beforeDestroy() {
    // 保存音乐状态
    musicStore.setIsPlaying(this.isPlaying)
    musicStore.setCurrentTime(this.currentTime)
    musicStore.setDuration(this.duration)
  },
  methods: {
    formatTime(seconds) {
      if (seconds === undefined || seconds === null || isNaN(seconds)) return '0:00'
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins}:${secs < 10 ? '0' : ''}${secs}`
    },
    togglePlay() {
      if (!this.audioRef) return
      if (this.isPlaying) {
        this.audioRef.pause()
      } else {
        this.audioRef.play().catch(err => console.warn('自动播放被阻止:', err))
      }
    },
    updateTime() {
      if (!this.audioRef) return
      this.currentTime = this.audioRef.currentTime
      musicStore.setCurrentTime(this.currentTime)
    },
    setDuration() {
      if (!this.audioRef) return
      this.duration = this.audioRef.duration
      musicStore.setDuration(this.duration)
    },
    seekTo(e) {
      if (!this.audioRef || !this.duration) return
      const rect = e.currentTarget.getBoundingClientRect()
      const percent = (e.clientX - rect.left) / rect.width
      this.audioRef.currentTime = percent * this.duration
    },
    play() {
      this.isPlaying = true
      musicStore.setIsPlaying(true)
    },
    pause() {
      this.isPlaying = false
      musicStore.setIsPlaying(false)
    },
    stopPlay() {
      this.isPlaying = false
      musicStore.setIsPlaying(false)
    }
  }
}
</script>

<style scoped>
.mini-player {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  z-index: 1000;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.mini-player-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
}

.mini-cover {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.mini-info {
  flex: 1;
  min-width: 0;
}

.mini-title {
  font-size: 13px;
  font-weight: 500;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mini-time {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 2px;
}

.mini-play-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mini-play-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.mini-play-btn:active {
  transform: scale(0.95);
}

.mini-progress {
  height: 2px;
  background: rgba(255, 255, 255, 0.2);
  cursor: pointer;
}

.mini-progress-bar {
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  transition: width 0.1s linear;
}
</style>
