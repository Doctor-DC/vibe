<template>
  <div class="fireworks-container">
    <div
      v-for="(particle, idx) in particles"
      :key="idx"
      class="particle"
      :style="getParticleStyle(particle)"
    ></div>
  </div>
</template>

<script>
export default {
  name: 'Fireworks',
  data() {
    return {
      particles: []
    }
  },
  mounted() {
    this.createFireworks()
  },
  methods: {
    createFireworks() {
      const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffa500']
      
      // 创建多个烟花爆发
      for (let burst = 0; burst < 5; burst++) {
        setTimeout(() => {
          for (let i = 0; i < 40; i++) {
            const angle = (Math.PI * 2 * i) / 40
            const velocity = 4 + Math.random() * 8
            
            this.particles.push({
              x: Math.random() * window.innerWidth,
              y: window.innerHeight * 0.3,
              vx: Math.cos(angle) * velocity,
              vy: Math.sin(angle) * velocity,
              color: colors[Math.floor(Math.random() * colors.length)],
              size: 4 + Math.random() * 8,
              life: 1,
              decay: 0.015 + Math.random() * 0.01,
              gravity: 0.15
            })
          }
        }, burst * 400)
      }
      
      // 动画循环
      this.animate()
    },
    animate() {
      // 更新粒子
      for (let i = this.particles.length - 1; i >= 0; i--) {
        const p = this.particles[i]
        p.x += p.vx
        p.y += p.vy
        p.vy += p.gravity
        p.life -= p.decay
        
        if (p.life <= 0) {
          this.particles.splice(i, 1)
        }
      }
      
      if (this.particles.length > 0) {
        requestAnimationFrame(() => this.animate())
      }
    },
    getParticleStyle(particle) {
      return {
        left: particle.x + 'px',
        top: particle.y + 'px',
        width: particle.size + 'px',
        height: particle.size + 'px',
        backgroundColor: particle.color,
        opacity: particle.life,
        borderRadius: '50%',
        pointerEvents: 'none',
        boxShadow: `0 0 ${particle.size / 2}px ${particle.color}`
      }
    }
  }
}
</script>

<style scoped>
.fireworks-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9999;
}

.particle {
  position: fixed;
  pointer-events: none;
}
</style>
