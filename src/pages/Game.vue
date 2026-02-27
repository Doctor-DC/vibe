<template>
  <div class="game-page">
    <!-- 分数/进度 -->
    <div class="game-header">
      <router-link to="/" class="back-btn">← 返回</router-link>
      <div class="score">{{ progressScore }}/3</div>
      <div class="status">{{ gameStatus }}</div>
    </div>

    <!-- 游戏容器 -->
    <div v-if="gameActive" class="game-container">
      <div class="album-display">
        <img v-if="currentAlbum" :src="currentAlbum.image" :alt="currentAlbum.title" class="album-cover" />
        <p v-if="currentAlbum" class="album-title">{{ currentAlbum.title }}</p>
      </div>

      <div class="options">
        <button 
          v-for="band in options"
          :key="band"
          @click="selectAnswer(band)"
          :disabled="answered"
          :class="['option-btn', { 
            correct: answered && band === correctBand,
            wrong: answered && band !== correctBand && band === selectedBand
          }]"
        >
          {{ band }}
        </button>
      </div>

      <div v-if="answered" class="feedback">
        <div v-if="selectedBand === correctBand" class="correct-feedback">✓ 正确！</div>
        <div v-else class="wrong-feedback">✗ 错误，正确答案是 {{ correctBand }}</div>
        <button @click="nextQuestion" class="next-btn">下一题</button>
      </div>
    </div>

    <!-- 游戏结束 -->
    <div v-else class="game-over">
      <Fireworks v-if="score === 3" />
      <div class="result">
        <h2 v-if="score === 3">🎉 完美！</h2>
        <h2 v-else>游戏结束</h2>
        <p class="final-score">最终得分：{{ score }}/3</p>
        <p v-if="score === 3" class="message">你是后摇乐迷！</p>
        <p v-else class="message">再来一次吧，多了解一些乐队！</p>
        
        <router-link to="/" class="restart-btn">返回首页</router-link>
      </div>
    </div>

    <!-- 失败弹窗 -->
    <FailureModal v-if="showFailureModal" @retry="retryGame" @home="goHome" />
    
    <!-- 迷你播放器 -->
    <MiniPlayer />
  </div>
</template>

<script>
import Fireworks from '../components/Fireworks.vue'
import FailureModal from '../components/FailureModal.vue'
import MiniPlayer from '../components/MiniPlayer.vue'

export default {
  name: 'Game',
  components: { Fireworks, FailureModal, MiniPlayer },
  data() {
    return {
      bands: [],
      allAlbums: [],
      score: 0,
      currentQuestion: 0,
      currentAlbum: null,
      correctBand: null,
      selectedBand: null,
      answered: false,
      options: [],
      gameActive: true,
      showFailureModal: false,
      wrongAnswers: 0
    }
  },
  computed: {
    gameStatus() {
      return this.gameActive ? '进行中' : '已结束'
    },
    progressScore() {
      return this.gameActive ? Math.min(this.score + 1, 3) : 3
    }
  },
  methods: {
    selectAnswer(band) {
      if (this.answered) return
      
      this.selectedBand = band
      this.answered = true

      if (band === this.correctBand) {
        this.score++
        // 如果达到3题，游戏结束
        if (this.score === 3) {
          setTimeout(() => {
            this.gameActive = false
          }, 1500)
        }
      } else {
        this.wrongAnswers++
        // 如果错3次后，游戏失败
        if (this.wrongAnswers >= 3) {
          setTimeout(() => {
            this.showFailureModal = true
          }, 1500)
        }
      }
    },
    nextQuestion() {
      if (this.selectedBand === this.correctBand) {
        this.loadQuestion()
        this.answered = false
        this.selectedBand = null
      }
    },
    loadQuestion() {
      if (this.allAlbums.length === 0) return
      
      // 随机选择一个专辑
      const randomAlbum = this.allAlbums[Math.floor(Math.random() * this.allAlbums.length)]
      this.currentAlbum = randomAlbum
      
      // 找到包含该专辑的乐队
      let correctBand = null
      for (const band of this.bands) {
        if (band.albums.some(a => a.title === randomAlbum.title)) {
          correctBand = band.name
          break
        }
      }
      
      this.correctBand = correctBand
      
      // 生成4个选项（包括正确答案）
      const shuffled = this.bands.map(b => b.name).sort(() => Math.random() - 0.5)
      this.options = shuffled.slice(0, 4)
      
      // 确保正确答案在选项中
      if (!this.options.includes(correctBand)) {
        this.options[Math.floor(Math.random() * 4)] = correctBand
      }
      
      this.options = this.options.sort(() => Math.random() - 0.5)
    },
    retryGame() {
      this.score = 0
      this.wrongAnswers = 0
      this.showFailureModal = false
      this.gameActive = true
      this.answered = false
      this.selectedBand = null
      this.loadQuestion()
    },
    goHome() {
      this.$router.push('/')
    }
  },
  created() {
    // 加载数据
    fetch('/data-bands.json')
      .then(r => r.json())
      .then(js => {
        this.bands = (js && js.bands) ? js.bands : (Array.isArray(js) ? js : [])
        
        // 提取所有专辑
        this.allAlbums = []
        for (const band of this.bands) {
          if (band.albums) {
            this.allAlbums.push(...band.albums)
          }
        }
        
        // 开始游戏
        this.loadQuestion()
      })
      .catch(e => {
        console.error('加载数据失败', e)
      })
  }
}
</script>

<style scoped lang="scss">
@import '../../styles/variables';
@import '../../styles/mixins';

.game-page {
  position: relative;
  min-height: 100vh;
  padding: 2rem 1rem;
  padding-bottom: 100px;
  z-index: 10;
}

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 600px;
  margin: 0 auto 2rem;
  padding: 1rem;
  background: color(light-white-03);
  border-radius: 12px;

  .back-btn {
    padding: 0.5rem 1rem;
    background: linear-gradient(135deg, #e0e0e0 0%, #c0c0c0 100%);
    color: #333;
    border: none;
    border-radius: 6px;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;

    &:hover {
      transform: translateY(-2px);
      background: linear-gradient(135deg, #f0f0f0 0%, #d0d0d0 100%);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  }

  .score {
    font-size: 1.5rem;
    font-weight: bold;
    color: color(accent);
  }

  .status {
    color: color(muted);
  }
}

.game-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background: color(light-white-02);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.album-display {
  text-align: center;
  margin-bottom: 2rem;

  .album-cover {
    width: 240px;
    height: 240px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    object-fit: cover;
  }

  .album-title {
    margin-top: 1rem;
    color: color(muted);
    font-size: 0.9rem;
  }
}

.options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 2rem;

  .option-btn {
    padding: 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: 2px solid #5668d8;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1.05rem;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    color: white;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);

    &:hover:not(:disabled) {
      border-color: #5668d8;
      background: linear-gradient(135deg, #7a8ff5 0%, #8558b2 100%);
      transform: translateY(-4px);
      box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }

    &:disabled {
      cursor: not-allowed;
      opacity: 0.6;
      transform: none;
    }

    &.correct {
      border-color: #2e7d32;
      background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
      color: #1b5e20;
      font-weight: bold;
      box-shadow: 0 4px 12px rgba(45, 125, 50, 0.3);
    }

    &.wrong {
      border-color: #d32f2f;
      background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
      color: #b71c1c;
      font-weight: bold;
      box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
    }
  }
}

.feedback {
  text-align: center;
  padding: 1rem;
  border-radius: 8px;
  background: color(light-white-03);
  margin-top: 1rem;

  .correct-feedback {
    color: #4caf50;
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }

  .wrong-feedback {
    color: #f44336;
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }

  .next-btn {
    padding: 0.75rem 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
    font-weight: 600;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
  }
}

.game-over {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  padding: 2rem;
}

.result {
  background: color(light-white-02);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);

  h2 {
    font-size: 2.2rem;
    margin-bottom: 1rem;
    color: color(accent);
  }

  .final-score {
    font-size: 1.8rem;
    font-weight: bold;
    color: color(text);
    margin: 1rem 0;
  }

  .message {
    font-size: 1.1rem;
    color: color(muted);
    margin-bottom: 2rem;
  }

  .restart-btn {
    display: inline-block;
    padding: 1rem 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-decoration: none;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-size: 1.1rem;
    font-weight: 600;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }
  }
}
</style>
