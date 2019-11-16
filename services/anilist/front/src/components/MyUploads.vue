<template>
  <div id="uploads">
    <h5>Your anime list:</h5>
    <ul v-for="anime in animeList" v-bind:key="anime.id">
      <li>
        <a
          @click="
            $router.push({
              name: 'player',
              params: {
                token: anime.token
              }
            })
          "
          >{{ anime.name }}</a
        >
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      animeList: []
    };
  },

  mounted: async function() {
    try {
      const response = await this.$http.get(`/player/my_uploads/`);
      const { data } = response;
      this.animeList = data;
    } catch (e) {
      void 0;
    }
  }
};
</script>
