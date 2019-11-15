<template>
  <div id="list">
    <div>List component (@jnovikov)</div>
    <b-button
      size="sm"
      variant="danger"
      type="submit"
      :anime="anime"
      @click="$router.push(getAnimeUrl(anime.token))"
      >WATCH ANIME</b-button
    >
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      anime: {
        token: "broken"
      }
    };
  },
  methods: {
    getAnimeUrl: function(token) {
      return {
        name: "player",
        params: {
          token: token
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
