<template>
  <div id="layout">
    <b-navbar toggleable="lg" type="dark" variant="dark">
      <b-navbar-brand @click="$router.push({ name: 'home' })"
        >Anilist</b-navbar-brand
      >

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <b-button
            size="sm"
            variant="success"
            type="submit"
            class="mr-2"
            @click="$router.push({ name: 'login' })"
            v-if="$store.state.user === null"
            >Login</b-button
          >
          <b-button
            size="sm"
            variant="success"
            type="submit"
            class="mr-2"
            @click="$router.push({ name: 'uploads' })"
            v-else
            >My anime ({{ $store.state.user.name }})</b-button
          >
          <b-button
            size="sm"
            variant="danger"
            type="submit"
            @click="$router.push({ name: 'register' })"
            v-if="$store.state.user === null"
            >Register</b-button
          >
          <b-button
            size="sm"
            variant="danger"
            type="submit"
            @click="logout"
            v-else
            >Logout</b-button
          >
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <b-container id="content">
      <slot></slot>
    </b-container>
  </div>
</template>

<style scoped>
#layout {
  position: relative;
  height: 100%;
}
#content {
  height: calc(100% - 56px - 25px);
  margin-top: 25px;
}
</style>

<script>
export default {
  methods: {
    logout: async function() {
      await this.$http.post("/auth/logout");
      this.$store.commit("setUser", null);
    }
  }
};
</script>
