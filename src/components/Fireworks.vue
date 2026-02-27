<template>
  <svg class="fireworks-svg" ref="svg">
    <defs>
      <filter id="glow">
        <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
        <feMerge>
          <feMergeNode in="coloredBlur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>
    <g class="particles-group">
      <circle
        v-for="(particle, idx) in particles"
        :key="idx"
        :cx="particle.x"
        :cy="particle.y"
        :r="particle.size / 2"
        :fill="particle.color"
        :opacity="Math.pow(Math.max(0, particle.life), 1.5)"
        filter="url(#glow)"
        class="particle"
      />
    </g>
  </svg>
</template>

<script>
export default {
  name: 'Fireworks',
  data() {
    return {
      svg: null,
      particles: [],
      animationId: null
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initSVG()
      this.createFireworks()
    })
  },
  beforeDestroy() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId)
    }
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    initSVG() {
      this.svg = this.$refs.svg
      if (!this.svg) return
      
      this.resizeSVG()
      this.handleResize = () => this.resizeSVG()
      window.addEventListener('resize', this.handleResize)
    },
    
    resizeSVG() {
      const rect = this.svg.parentElement.getBoundingClientRect()
      this.svg.setAttribute('width', rect.width)
      this.svg.setAttribute('height', rect.height)
      this.svg.setAttribute('viewBox', `0 0 ${rect.width} ${rect.height}`)
    },
    
    createFireworks() {
      const colorPalettes = [
        ['#ff1744', '#f50057', '#c51162'],
        ['#ffeb3b', '#fbc02d', '#f57f17'],
        ['#00e5ff', '#00b8d4', '#0097a7'],
        ['#76ff03', '#64dd17', '#558b2f'],
        ['#2979f0', '#1565c0', '#0d47a1']
      ]
      
      const rect = this.svg.parentElement.getBoundingClientRect()
      const w = rect.width
      const h = rect.height
      
      const burstPoints = [
        { x: w * 0.3, y: h * 0.2 },
        { x: w * 0.7, y: h * 0.2 },
        { x: w * 0.5, y: h * 0.35 },
        { x: w * 0.2, y: h * 0.4 },
        { x: w * 0.8, y: h * 0.4 }
      ]
      
      burstPoints.forEach((point, idx) => {
        setTimeout(() => {
          const colors = colorPalettes[idx % colorPalettes.length]
          
          // 每个爆发点创建 200 个粒子
          for (let i = 0; i < 200; i++) {
            const angle = (Math.PI * 2 * i) / 200
            const velocity = 2 + Math.random() * 15
            const spread = (Math.random() - 0.5) * 0.4
            
            this.particles.push({
              x: point.x,
              y: point.y,
              vx: Math.cos(angle + spread) * velocity,
              vy: Math.sin(angle + spread) * velocity,
              color: colors[Math.floor(Math.random() * colors.length)],
              size: 2 + Math.random() * 7,
              life: 1,
              maxLife: 1,
              decay: 0.007 + Math.random() * 0.013,
              gravity: 0.13,
              friction: 0.97
            })
          }
          
          if (this.particles.length > 0) {
            this.animate()
          }
        }, idx * 350)
      })
    },
    
    animate() {
      // 更新粒子物理
      for (let i = this.particles.length - 1; i >= 0; i--) {
        const p = this.particles[i]
        
        // 物理更新
        p.vx *= p.friction
        p.vy *= p.friction
        p.x += p.vx
        p.y += p.vy
        p.vy += p.gravity
        p.life -= p.decay
        
        if (p.life <= 0) {
          this.particles.splice(i, 1)
        }
      }
      
      if (this.particles.length > 0) {
        this.animationId = requestAnimationFrame(() => this.animate())
      }
    }
  }
}
</script>

<style scoped>
.fireworks-svg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9999;
}

.particle {
  transition: opacity 0.02s linear;
}
</style>
