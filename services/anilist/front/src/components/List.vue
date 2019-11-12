<template>
  <div id="list">
    <div>List component (@jnovikov)</div>
    <b-button
      size="sm"
      variant="danger"
      type="submit"
      :anime="anime"
      @click="$router.push(getAnimeUrl(anime.id))"
      >WATCH ANIME</b-button
    >
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      anime: {
        id: 1
      }
    };
  },
  methods: {
    getAnimeUrl: function(idx) {
      return {
        name: "player",
        params: {
          id: idx
        }
      };
    }
  }
};
</script>

<style scoped>
#list {
  border: 1px solid #ff0000;
}
</style>
