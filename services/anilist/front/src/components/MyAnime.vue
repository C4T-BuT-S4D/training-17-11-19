<template>
  <div id="myAnime">
    <h5>My animes:</h5>
    <ul v-for="anime in animes" v-bind:key="anime.id">
      <li>
        <a
          @click="
            $router.push({
              name: 'detail',
              params: {
                animeId: anime.id
              }
            })
          "
          >{{ anime.title }}</a
        >
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  methods: {
    getAnimes: async function() {
      try {
        const response = await this.$http.get("/db/my_anime");
        const {
          data: { result: animes }
        } = response;
        this.animes = animes;
      } catch (e) {
        this.animes = [];
      }
    }
  },
  data: function() {
    return {
      titleFilter: null,
      descriptionFilter: null,
      animes: []
    };
  },
  mounted: async function() {
    await this.getAnimes();
  }
};
</script>
