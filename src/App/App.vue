<template>
  <div class="app-root">
    <!-- 背景保持不变 -->
    <div id="fancy-bg" aria-hidden="true">
      <div class="triangles">
        <svg style="display:none">
          <defs>
            <filter id="glow"><feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
          </defs>
        </svg>
        <template v-for="(t, idx) in triangles">
          <svg :key="idx" :class="['triangle-svg', `t${idx + 1}`]" :style="{ left: t.left + '%', top: t.top + '%', transform: `rotate(${t.rot}deg)` }" viewBox="0 0 40 40" :width="t.size" :height="t.size" aria-hidden="true">
            <polygon points="20,4 36,36 4,36" fill="none" :stroke="t.color" :stroke-width="t.stroke" filter="url(#glow)"/>
          </svg>
        </template>
      </div>
      <img class="paper-plane" id="paperPlane" role="img" aria-label="纸飞机" src="/images/paper-plane.svg" alt="纸飞机" />
    </div>

    <!-- 路由视图 -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return { triangles: [] }
  },
  created() {
    // create triangles fixed on left side
    // palette: light blue, white, purple
    const palette = ['rgba(100,180,255,0.95)','rgba(255,255,255,0.95)','rgba(178,153,255,0.95)']
    const count = 3
    const rotations = [-15, 25, -35]  // 为每个三角形设置不同的角度
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
        rot: rotations[idx],
        color: palette[idx % palette.length],
        stroke: (0.9 + Math.random()*0.7).toFixed(2)
      }
    })
  }
}
</script>

<style scoped lang="scss">
@import './App.scss';
</style>
