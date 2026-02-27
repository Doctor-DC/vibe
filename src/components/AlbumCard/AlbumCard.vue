<template>
  <div class="album">
    <img
      v-if="displayImage && !imgError"
      :src="displayImage"
      :alt="album.title"
      class="cover-img"
      loading="lazy"
      @error="onImageError"
    />
    <div v-else class="cover">{{ album.title }}</div>

    <h4>{{ album.title }}</h4>
    <div class="meta">{{ album.year }}</div>

    <div v-if="album.tracks && album.tracks.length" class="tracks-wrap">
      <button class="toggle" @click="toggle" :aria-expanded="String(open)">{{ open ? '隐藏曲目' : '显示曲目' }}</button>
      <div v-show="open" class="tracks">
        <ol>
          <li v-for="(t, i) in album.tracks" :key="i">{{ t }}</li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlbumCard',
  props: {
    album: { type: Object, required: true }
  },
  data() {
    return {
      open: false,
      imgError: false,
      useProxy: false
    }
  },
  computed: {
    displayImage() {
      const image = this.album && this.album.image
      if (!image) return ''
      if (!this.useProxy) return image
      return this.toProxyImage(image)
    }
  },
  watch: {
    'album.image'() {
      this.resetImageState()
    }
  },
  methods: {
    toggle() { this.open = !this.open },
    resetImageState() {
      this.imgError = false
      this.useProxy = false
    },
    toProxyImage(url) {
      if (!url) return ''
      const normalized = url.replace(/^https?:\/\//, '')
      return `https://images.weserv.nl/?url=${encodeURIComponent(normalized)}`
    },
    onImageError() {
      if (!this.useProxy && this.album && this.album.image) {
        this.useProxy = true
        return
      }
      this.imgError = true
    }
  },
  created() {
    this.resetImageState()
  }
}
</script>

<style scoped lang="scss">
@import './AlbumCard.scss';
</style>
