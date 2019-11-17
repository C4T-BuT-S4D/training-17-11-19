<template>
  <div id="listAnime">
    <h5>Our Anime DB:</h5>
    <b-form-input v-model="titleFilter" placeholder="Boku no"></b-form-input>
    <b-form-input
      v-model="descriptionFilter"
      placeholder="Once upon a time"
    ></b-form-input>
    <b-button @click="getAnimes" id="enter">Find Anime!</b-button>
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
        const response = await this.$http.get("/db/anime", {
          params: {
            title: this.titleFilter,
            description: this.descriptionFilter
          }
        });
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
