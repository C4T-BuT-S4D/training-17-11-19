<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style scoped>
#app {
  height: 100%;
}
</style>

<style>
html,
body {
  height: 100%;
}
</style>

<script>
export default {
  mounted: async function() {
    try {
      const response = await this.$http.get("/auth/me");
      const { data } = response;

      this.$store.commit("setUser", data);
    } catch (e) {
      void 0;
    }
  }
};
</script>
