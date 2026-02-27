<template>
  <div class="music-player">
    <div class="player-header">
      <h3>🎵 音乐播放器 - Explosions in the Sky</h3>
      <span class="current-song">{{ currentSong }}</span>
    </div>

    <!-- 播放进度条 -->
    <div class="progress-container">
      <div class="progress-bar" @click="seekTo">
        <div class="buffer" :style="{ width: buffered + '%' }"></div>
        <div class="progress" :style="{ width: progress + '%' }"></div>
      </div>
      <div class="time-display">
        <span>{{ formatTime(currentTime) }}</span>
        <span>{{ formatTime(duration) }}</span>
      </div>
    </div>

    <!-- 播放控制 -->
    <div class="player-controls">
      <button @click="previousTrack" class="control-btn" title="上一曲">⏮</button>
      <button @click="togglePlay" class="control-btn play-btn" :title="isPlaying ? '暂停' : '播放'">
        {{ isPlaying ? '⏸' : '▶' }}
      </button>
      <button @click="nextTrack" class="control-btn" title="下一曲">⏭</button>
      <button @click="toggleRepeat" class="control-btn" :class="{ active: repeatMode > 0 }">🔁</button>
    </div>

    <!-- 音量控制 -->
    <div class="volume-control">
      <span class="volume-icon">🔊</span>
      <input type="range" v-model.number="volume" min="0" max="100" class="volume-slider" />
      <span class="volume-text">{{ volume }}%</span>
    </div>

    <!-- 状态信息 -->
    <div class="player-status">
      <div v-if="isLoading" class="status-item loading">⏳ 正在加载...</div>
      <div v-if="error" class="status-item error">❌ {{ error }}</div>
      <div v-if="!isLoading && !error && isPlaying" class="status-item playing">▶ 正在播放</div>
    </div>

    <!-- 曲目列表 -->
    <div class="playlist">
      <div class="playlist-header">曲目列表</div>
      <div 
        v-for="(track, idx) in tracks" 
        :key="idx"
        @click="selectTrack(idx)"
        :class="['track-item', { 
          active: currentTrackIndex === idx, 
          playing: isPlaying && currentTrackIndex === idx
        }]"
      >
        <span class="track-number">{{ idx + 1 }}</span>
        <span class="track-name">{{ track.title }}</span>
        <span class="track-duration">{{ track.duration }}</span>
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
        { title: 'Your Hand in Mine', duration: '4:32', url: '/music/your-hand-in-mine.mp3' }
      ]
    }
  },
  computed: {
    currentSong() {
      return this.tracks[this.currentTrackIndex]?.title || ''
    },
    progress() {
      return this.duration > 0 ? (this.currentTime / this.duration) * 100 : 0
    }
  },
  methods: {
    formatTime(seconds) {
      if (!seconds || isNaN(seconds)) return '0:00'
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
        if (!audio.src) {
          this.error = '请先上传或配置音乐文件'
          return
        }
        // 如果之前是静音的，现在取消静音
        if (audio.muted) {
          audio.muted = false
        }
        // 第一次播放时从30秒开始
        if (!this.hasStarted) {
          audio.currentTime = 30
          this.hasStarted = true
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
      if (track.url) {
        this.$refs.audioPlayer.src = track.url
        if (this.isPlaying) {
          this.$refs.audioPlayer.play().catch(err => {
            this.error = '播放失败: ' + err.message
          })
        }
      } else {
        this.error = `"${track.title}" 暂无音源`
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
    },
    onPause() {
      this.isPlaying = false
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
      // 初始化第一首歌曲的URL
      const firstTrack = this.tracks[0]
      if (firstTrack && firstTrack.url) {
        audio.src = firstTrack.url
      }
    }
  }
}
</script>

<style scoped lang="scss">
@import '../../styles/variables';
@import '../../styles/mixins';

.music-player {
  background: color(light-white-03);
  border-radius: 12px;
  padding: 1.5rem;
  margin: 1rem auto;
  max-width: 500px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.player-header {
  text-align: center;
  margin-bottom: 1rem;

  h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
    color: color(text);
  }

  .current-song {
    display: block;
    color: color(accent);
    font-size: 0.95rem;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.progress-container {
  margin: 1rem 0;

  .progress-bar {
    background: color(light-white-04);
    height: 6px;
    border-radius: 3px;
    overflow: hidden;
    cursor: pointer;
    margin-bottom: 0.5rem;
    position: relative;

    .buffer {
      position: absolute;
      background: rgba(102, 126, 234, 0.3);
      height: 100%;
    }

    .progress {
      background: color(accent);
      height: 100%;
      border-radius: 3px;
      transition: width 0.1s linear;
    }
  }

  .time-display {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: color(muted);
  }
}

.player-controls {
  @include flex-center;
  gap: 1rem;
  margin: 1rem 0;

  .control-btn {
    background: color(light-white-04);
    color: color(text);
    border: none;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      background: color(accent);
      color: white;
      transform: scale(1.1);
    }

    &:active {
      transform: scale(0.95);
    }

    &.play-btn {
      width: 52px;
      height: 52px;
      background: color(accent);
      color: white;
      font-size: 1.3rem;
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    &.active {
      background: color(accent);
      color: white;
    }
  }
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 1rem 0;
  padding: 0.75rem;
  background: color(light-white-04);
  border-radius: 6px;

  .volume-icon {
    font-size: 1rem;
    min-width: 24px;
  }

  .volume-slider {
    flex: 1;
    height: 5px;
    border-radius: 5px;
    outline: none;
    -webkit-appearance: none;
    appearance: none;
    background: linear-gradient(to right, color(light-white-01), color(accent));

    &::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: color(accent);
      cursor: pointer;
    }

    &::-moz-range-thumb {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: color(accent);
      cursor: pointer;
      border: none;
    }
  }

  .volume-text {
    font-size: 0.85rem;
    color: color(muted);
    min-width: 35px;
    text-align: right;
  }
}

.player-status {
  margin: 0.75rem 0;
  min-height: 20px;

  .status-item {
    font-size: 0.85rem;
    padding: 0.4rem 0.6rem;
    border-radius: 4px;
    text-align: center;

    &.loading {
      color: #ff9800;
      background: rgba(255, 152, 0, 0.1);
    }

    &.error {
      color: #f44336;
      background: rgba(244, 67, 54, 0.1);
    }

    &.playing {
      color: color(accent);
      background: rgba(102, 126, 234, 0.1);
    }
  }
}

.playlist {
  max-height: 220px;
  overflow-y: auto;
  border-top: 1px solid color(light-white-04);
  margin-top: 1rem;
  padding-top: 0.75rem;

  .playlist-header {
    font-size: 0.85rem;
    font-weight: 600;
    color: color(muted);
    margin-bottom: 0.5rem;
    padding: 0 0.5rem;
  }

  .track-item {
    display: flex;
    align-items: center;
    padding: 0.6rem;
    margin: 0.25rem 0;
    border-radius: 6px;
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
    }

    .track-number {
      color: color(muted);
      font-size: 0.8rem;
      min-width: 25px;
      text-align: center;
    }

    .track-name {
      flex: 1;
      font-size: 0.9rem;
      margin: 0 0.5rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .track-duration {
      color: color(muted);
      font-size: 0.8rem;
      min-width: 40px;
      text-align: right;
    }
  }
}

</style>
