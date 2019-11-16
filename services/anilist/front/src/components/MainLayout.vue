<template>
  <layout>
    <b-row id="content-row">
      <b-col :cols="$store.state.user === null ? 12 : 8">
        <slot></slot>
      </b-col>
      <b-col cols="4" id="chat-col" v-if="$store.state.user !== null">
        <chat></chat>
      </b-col>
    </b-row>
  </layout>
</template>

<style scoped>
#content-row {
  height: 100%;
}

#chat-col {
  height: calc(100% - 30px);
}
</style>

<script>
import Layout from "./Layout";
import Chat from "./Chat";

export default {
  components: {
    Layout,
    Chat
  }
};
</script>
