<template>
  <div class="album">
    <img v-if="album.image" :src="album.image" :alt="album.title" class="cover-img" loading="lazy" />
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
    return { open: false };
  },
  methods: {
    toggle() { this.open = !this.open; }
  }
}
</script>

<style scoped lang="scss">
@import './AlbumCard.scss';
</style>
