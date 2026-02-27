<template>
  <div class="music-player-mini" v-if="currentTrack">
    <!-- 背景专辑封面 -->
    <div class="player-bg" :class="{ rotating: isPlaying }" :style="{ backgroundImage: `url('${currentTrack.image}')` }">
      <!-- 深色遮罩 -->
      <div class="player-overlay">
        <!-- 小猫在旋转 -->
        <div v-if="isPlaying" class="cat-walker" :class="{ walking: isPlaying }">
          <span class="cat">�</span>
        </div>
      </div>
    </div>

    <!-- 底部：进度条、时间和导航按钮 -->
    <div class="player-footer">
      <!-- 时间显示和进度条容器 -->
      <div class="progress-container">
        <!-- 进度条 -->
        <div class="progress-bar-mini" @click="seekTo" :title="`${formatTime(currentTime)} / ${formatTime(duration)}`">
          <div class="progress" :style="{ width: progress + '%' }"></div>
        </div>
        <!-- 时间信息 -->
        <div class="time-info-row">
          <span class="time-current">{{ formatTime(currentTime) }}</span>
          <span class="time-total">{{ formatTime(duration) }}</span>
        </div>
      </div>

      <!-- 控制按钮 -->
      <div class="controls-bar">
        <button @click="previousTrack" class="mini-btn">⏮</button>
        <button @click="togglePlay" class="mini-btn play-btn">{{ isPlaying ? '⏸' : '▶' }}</button>
        <button @click="nextTrack" class="mini-btn">⏭</button>
        <button @click="toggleRepeat" class="mini-btn" :class="{ active: repeatMode > 0 }">🔁</button>
      </div>
    </div>

    <!-- 播放列表 -->
    <div class="songs-list">
      <div class="list-header">📋 播放列表</div>
      <div class="list-content">
        <div 
          v-for="(track, idx) in tracks"
          :key="idx"
          class="song-row"
          :class="{ active: currentTrackIndex === idx, playing: isPlaying && currentTrackIndex === idx }"
          @click="selectTrack(idx)"
        >
          <span class="row-number">{{ idx + 1 }}</span>
          <div class="row-info">
            <div class="row-title">{{ track.title }}</div>
            <div class="row-album">{{ track.album }}</div>
          </div>
          <div class="row-duration">{{ track.duration }}</div>
        </div>
      </div>
    </div>

    <!-- 音频元素 -->
    <audio 
      ref="audioPlayer" 
      @timeupdate="updateProgress"
      @loadedmetadata="onMetadataLoaded"
      @ended="handleTrackEnd"
      @play="onPlay"
      @pause="onPause"
      @error="onError"
      @progress="onProgress"
      crossorigin="anonymous"
    ></audio>
  </div>
</template>

<script>
import { musicStore } from '../store/musicStore'

export default {
  name: 'MusicPlayer',
  data() {
    return {
      isPlaying: false,
      isLoading: false,
      currentTrackIndex: 0,
      currentTime: 0,
      duration: 0,
      buffered: 0,
      volume: 70,
      repeatMode: 0,
      error: null,
      hasStarted: false,
      tracks: [
        {
          title: 'Your Hand in Mine',
          artist: 'Explosions in the Sky',
          album: 'The Earth Is Not a Cold Dead Place',
          duration: '4:32',
          id: '26402127',
          url: '/music/your-hand-in-mine.mp3',
          image: '/images/albums/explosions-in-the-sky__the-earth-is-not-a-cold-dead-place.jpg'
        }
      ]
    }
  },
  computed: {
    currentSong() {
      return this.tracks[this.currentTrackIndex]?.title || ''
    },
    currentTrack() {
      return this.tracks[this.currentTrackIndex]
    },
    progress() {
      return this.duration > 0 ? (this.currentTime / this.duration) * 100 : 0
    }
  },
  methods: {
    formatTime(seconds) {
      if (seconds === undefined || seconds === null || isNaN(seconds)) return '0:00'
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins}:${secs < 10 ? '0' : ''}${secs}`
    },
    togglePlay() {
      if (!this.$refs.audioPlayer) return
      const audio = this.$refs.audioPlayer
      if (this.isPlaying) {
        audio.pause()
      } else {
        // 如果没有src，先加载当前曲目
        if (!audio.src) {
          const track = this.currentTrack
          if (track && track.url) {
            audio.src = track.url
          } else {
            this.error = '暂无音乐文件'
            return
          }
        }
        
        if (audio.muted) {
          audio.muted = false
        }
        
        audio.play().catch(err => {
          this.error = '播放失败: ' + err.message
          this.isPlaying = false
        })
      }
    },
    selectTrack(idx) {
      this.currentTrackIndex = idx
      this.currentTime = 0
      this.error = null
      const track = this.tracks[idx]
      
      // 保存到musicStore
      musicStore.setTrackIndex(idx)
      musicStore.setTrack(track)
      
      if (track && track.url) {
        this.$refs.audioPlayer.src = track.url
        if (this.isPlaying) {
          this.$refs.audioPlayer.play().catch(err => {
            this.error = '播放失败: ' + err.message
          })
        }
      } else {
        this.error = `"${track?.title}" 暂无音乐文件`
      }
    },
    nextTrack() {
      let nextIdx = this.currentTrackIndex + 1
      if (nextIdx >= this.tracks.length) {
        if (this.repeatMode === 1) {
          nextIdx = 0
        } else {
          this.isPlaying = false
          return
        }
      }
      this.selectTrack(nextIdx)
    },
    previousTrack() {
      if (this.currentTime > 2) {
        this.$refs.audioPlayer.currentTime = 0
      } else {
        let prevIdx = this.currentTrackIndex - 1
        if (prevIdx < 0) prevIdx = this.tracks.length - 1
        this.selectTrack(prevIdx)
      }
    },
    toggleRepeat() {
      this.repeatMode = (this.repeatMode + 1) % 3
    },
    seekTo(event) {
      const rect = event.currentTarget.getBoundingClientRect()
      const percent = (event.clientX - rect.left) / rect.width
      const time = percent * this.duration
      this.$refs.audioPlayer.currentTime = time
    },
    updateProgress() {
      const audio = this.$refs.audioPlayer
      if (audio) {
        this.currentTime = audio.currentTime
        this.duration = audio.duration || 0
        // 实时更新musicStore
        musicStore.setCurrentTime(this.currentTime)
        musicStore.setDuration(this.duration)
      }
    },
    onMetadataLoaded() {
      const audio = this.$refs.audioPlayer
      if (audio) {
        this.duration = audio.duration || 0
      }
    },
    onProgress() {
      const audio = this.$refs.audioPlayer
      if (audio && audio.buffered.length > 0) {
        const bufferedEnd = audio.buffered.end(audio.buffered.length - 1)
        this.buffered = (bufferedEnd / (audio.duration || 1)) * 100
      }
    },
    onPlay() {
      this.isPlaying = true
      this.isLoading = false
      musicStore.setIsPlaying(true)
    },
    onPause() {
      this.isPlaying = false
      musicStore.setIsPlaying(false)
    },
    onError() {
      this.error = '播放出错，请检查文件'
      this.isPlaying = false
    },
    handleTrackEnd() {
      if (this.repeatMode === 2) {
        this.$refs.audioPlayer.currentTime = 0
        this.$refs.audioPlayer.play()
      } else {
        this.nextTrack()
      }
    }
  },
  watch: {
    volume(newVal) {
      if (this.$refs.audioPlayer) {
        this.$refs.audioPlayer.volume = newVal / 100
      }
    }
  },
  mounted() {
    const audio = this.$refs.audioPlayer
    if (audio) {
      audio.volume = this.volume / 100
    }
    
    // 从musicStore恢复状态
    const state = musicStore.getState()
    if (state.track && state.track.url) {
      this.currentTrackIndex = state.trackIndex
      audio.src = state.track.url
      this.currentTime = state.currentTime
      if (audio) {
        audio.currentTime = state.currentTime
      }
      
      // 如果之前在播放，继续播放
      if (state.isPlaying && audio) {
        this.isPlaying = true
        audio.play().catch(err => {
          console.warn('自动播放被阻止:', err)
          this.isPlaying = false
        })
      }
    } else {
      // 初始化第一首歌曲的URL
      const firstTrack = this.tracks[0]
      if (firstTrack && firstTrack.url) {
        audio.src = firstTrack.url
      }
    }
  },
  
  beforeDestroy() {
    // 保存当前播放状态
    if (this.currentTrack) {
      musicStore.setTrack(this.currentTrack)
      musicStore.setTrackIndex(this.currentTrackIndex)
    }
    musicStore.setIsPlaying(this.isPlaying)
    musicStore.setCurrentTime(this.currentTime)
    musicStore.setDuration(this.duration)
    musicStore.setVolume(this.volume)
  },
}
</script>

<style scoped lang="scss">
@import '../../styles/variables';
@import '../../styles/mixins';

.music-player-mini {
  position: relative;
  width: 320px;
  margin: 1rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.player-bg {
  position: relative;
  width: 240px;
  height: 240px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  flex-shrink: 0;
  transition: transform 0.3s ease;

  &.rotating {
    animation: spin 20s linear infinite;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes spin-reverse {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(-360deg);
  }
}

.player-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: transparent;
  z-index: 2;
}

.player-bg.rotating .player-overlay {
  animation: spin-reverse 20s linear infinite;
}

.cat-walker {
  position: absolute;
  width: 130%;
  height: 130%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 3;
}

@keyframes cat-walk {
  0%, 100% {
    transform: translateX(-50%) translateX(-80px);
  }
  50% {
    transform: translateX(-50%) translateX(80px);
  }
}

.cat {
  position: absolute;
  font-size: 1.8rem;
  left: 50%;
  top: -40px;
  animation: cat-walk 4s ease-in-out infinite;
  transform: translateX(-50%);
}

@keyframes cat-face-rotate {
  0% {
    transform: translateX(-50%) scaleX(-1) rotate(0deg);
  }
  100% {
    transform: translateX(-50%) scaleX(-1) rotate(360deg);
  }
}

.progress-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.progress-bar-mini {
  width: 100%;
  height: 4.5px;
  background: rgba(128, 128, 128, 0.4);
  border-radius: 2.25px;
  overflow: hidden;
  cursor: pointer;

  .progress {
    height: 100%;
    background: linear-gradient(90deg, #64b4ff, #00d4ff);
    border-radius: 2.25px;
    transition: width 0.1s linear;
  }
}

.time-info-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: rgba(0, 0, 0, 0.6);
  padding: 0 2px;
}

.time-current {
  font-weight: 500;
}

.time-total {
  opacity: 0.8;
}

.time-info-center {
  font-size: 0.75rem;
  color: rgba(0, 0, 0, 0.6);
  white-space: nowrap;
  margin-bottom: 0.6rem;
}


.player-footer {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  width: 100%;
  margin-top: 1rem;
  justify-content: center;
  align-items: center;
}

.controls-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: white;

  .mini-btn {
    background: rgba(255, 255, 255, 0.15);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    width: 32px;
    height: 32px;
    border-radius: 50%;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;

    &:hover {
      background: rgba(255, 255, 255, 0.25);
      border-color: rgba(255, 255, 255, 0.5);
      transform: scale(1.05);
    }

    &:active {
      transform: scale(0.95);
    }

    &.play-btn {
      width: 40px;
      height: 40px;
      font-size: 1rem;
      background: rgba(255, 255, 255, 0.25);
      border-color: rgba(255, 255, 255, 0.6);
    }
  }

  .time-info {
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.5);
    margin-left: 0.4rem;
    white-space: nowrap;
  }
}

.songs-list {
  margin-top: 1.2rem;
  background: color(light-white-03);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  .list-header {
    padding: 0.8rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: color(text);
    border-bottom: 1px solid color(light-white-04);
    background: rgba(102, 126, 234, 0.05);
  }

  .list-content {
    max-height: 320px;
    overflow-y: auto;
  }

  .song-row {
    display: flex;
    align-items: center;
    padding: 0.7rem 0.8rem;
    border-bottom: 1px solid color(light-white-04);
    cursor: pointer;
    transition: all 0.2s ease;
    color: color(text);

    &:hover {
      background: color(light-white-04);
    }

    &.active {
      background: rgba(102, 126, 234, 0.1);
      color: color(accent);
    }

    &.playing {
      background: color(accent);
      color: white;
      font-weight: 600;

      .row-album {
        color: rgba(255, 255, 255, 0.8);
      }
    }

    .row-number {
      font-size: 0.8rem;
      color: color(muted);
      min-width: 30px;
      text-align: center;
      font-weight: 500;
    }

    .row-info {
      flex: 1;
      margin: 0 0.8rem;

      .row-title {
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 0.2rem;
      }

      .row-album {
        font-size: 0.75rem;
        color: color(muted);
        opacity: 0.8;
      }
    }

    .row-duration {
      font-size: 0.8rem;
      color: color(muted);
      min-width: 45px;
      text-align: right;
    }
  }
}

</style>
