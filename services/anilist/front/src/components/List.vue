<template>
  <div id="list">
    <div>
      <b-col lg="4" class="pb-2"
        ><b-button
          variant="primary"
          type="submit"
          @click="$router.push({ name: 'list' })"
          >Find anime</b-button
        ></b-col
      >
      <b-col lg="4" class="pb-2"
        ><b-button
          variant="secondary"
          type="submit"
          @click="$router.push({ name: 'myList' })"
          >My anime</b-button
        ></b-col
      >
      <b-col lg="4" class="pb-2"
        ><b-button
          variant="success"
          type="submit"
          @click="$router.push({ name: 'animeAdd' })"
          >Add anime</b-button
        ></b-col
      >
    </div>

    <!--<b-button-->
      <!--size="sm"-->
      <!--variant="danger"-->
      <!--type="submit"-->
      <!--:anime="anime"-->
      <!--@click="$router.push(getAnimeUrl(anime.token))"-->
      <!--&gt;WATCH ANIME</b-button-->
    <!--&gt;-->
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
