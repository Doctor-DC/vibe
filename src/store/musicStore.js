// 全局音乐播放状态管理
export const musicStore = {
  state: {
    isPlaying: false,
    currentTime: 0,
    duration: 0,
    volume: 70,
    trackIndex: 0, // 当前播放曲目索引
    track: null    // 当前播放的完整曲目信息
  },
  
  setIsPlaying(isPlaying) {
    this.state.isPlaying = isPlaying
  },
  
  setCurrentTime(time) {
    this.state.currentTime = time
  },
  
  setDuration(duration) {
    this.state.duration = duration
  },
  
  setVolume(volume) {
    this.state.volume = volume
  },
  
  setTrackIndex(index) {
    this.state.trackIndex = index
  },
  
  setTrack(track) {
    this.state.track = track
  },
  
  getState() {
    return this.state
  }
}
