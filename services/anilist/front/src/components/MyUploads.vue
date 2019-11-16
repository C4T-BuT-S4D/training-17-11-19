<template>
  <div id="uploads">
    <b-row>
      <b-col>
        <h5>Your anime list:</h5>
      </b-col>
      <b-col>
        <b-button
          size="sm"
          variant="primary"
          type="primary"
          class="mr-2"
          @click="$router.push({ name: 'upload' })"
          >Upload anime!</b-button
        >
      </b-col>
    </b-row>
    <b-row>
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
    </b-row>
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
