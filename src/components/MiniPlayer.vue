<template>
  <div
    class="mini-floating-player"
    v-if="track"
    :style="floatStyle"
    @mouseenter="isHovering = true"
    @mouseleave="isHovering = false"
    @mousedown="startDrag"
    @touchstart.prevent="startDragTouch"
  >
    <img
      v-if="track && track.image"
      :src="track.image"
      :alt="track.title"
      class="floating-cover"
      draggable="false"
    />
    <button
      v-show="isHovering"
      class="floating-play-btn"
      @mousedown.stop
      @touchstart.stop
      @click.stop="togglePlay"
      :title="isPlaying ? '暂停' : '播放'"
    >
      {{ isPlaying ? '⏸' : '▶' }}
    </button>
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
      isHovering: false,
      isDragging: false,
      dragOffsetX: 0,
      dragOffsetY: 0,
      x: 0,
      y: 0,
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
    floatStyle() {
      return {
        transform: `translate(${this.x}px, ${this.y}px)`
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.audioRef = this.$refs.audio
      if (!this.audioRef) return

      this.initPosition()
      window.addEventListener('mousemove', this.onDrag)
      window.addEventListener('mouseup', this.stopDrag)
      window.addEventListener('touchmove', this.onDragTouch, { passive: false })
      window.addEventListener('touchend', this.stopDrag)
      
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
    window.removeEventListener('mousemove', this.onDrag)
    window.removeEventListener('mouseup', this.stopDrag)
    window.removeEventListener('touchmove', this.onDragTouch)
    window.removeEventListener('touchend', this.stopDrag)

    // 保存音乐状态
    musicStore.setIsPlaying(this.isPlaying)
    musicStore.setCurrentTime(this.currentTime)
    musicStore.setDuration(this.duration)
  },
  methods: {
    initPosition() {
      const size = 84
      this.x = Math.max(12, window.innerWidth - size - 24)
      this.y = Math.max(12, window.innerHeight - size - 120)
    },
    clampPosition(nextX, nextY) {
      const size = 84
      const maxX = Math.max(12, window.innerWidth - size - 12)
      const maxY = Math.max(12, window.innerHeight - size - 12)
      this.x = Math.min(Math.max(12, nextX), maxX)
      this.y = Math.min(Math.max(12, nextY), maxY)
    },
    startDrag(event) {
      if (event.button !== 0) return
      this.isDragging = true
      this.dragOffsetX = event.clientX - this.x
      this.dragOffsetY = event.clientY - this.y
    },
    startDragTouch(event) {
      const touch = event.touches && event.touches[0]
      if (!touch) return
      this.isDragging = true
      this.dragOffsetX = touch.clientX - this.x
      this.dragOffsetY = touch.clientY - this.y
    },
    onDrag(event) {
      if (!this.isDragging) return
      this.clampPosition(event.clientX - this.dragOffsetX, event.clientY - this.dragOffsetY)
    },
    onDragTouch(event) {
      if (!this.isDragging) return
      const touch = event.touches && event.touches[0]
      if (!touch) return
      event.preventDefault()
      this.clampPosition(touch.clientX - this.dragOffsetX, touch.clientY - this.dragOffsetY)
    },
    stopDrag() {
      this.isDragging = false
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
.mini-floating-player {
  position: fixed;
  top: 0;
  left: 0;
  width: 84px;
  height: 84px;
  z-index: 1200;
  border-radius: 50%;
  overflow: hidden;
  cursor: grab;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
  transition: box-shadow 0.2s ease;
}

.mini-floating-player:active {
  cursor: grabbing;
}

.mini-floating-player:hover {
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.35);
}

.floating-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  user-select: none;
  -webkit-user-drag: none;
}

.floating-play-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.45);
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-play-btn:hover {
  background: rgba(0, 0, 0, 0.6);
}

@media (max-width: 768px) {
  .floating-play-btn {
    display: flex;
    background: rgba(0, 0, 0, 0.45);
  }
}
</style>
