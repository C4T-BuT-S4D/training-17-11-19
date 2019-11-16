<template>
  <div id="chat">
    <b-button @click="enter" id="enter" v-if="!entered">Enter chat</b-button>
    <template v-else-if="selectedUser !== null">
      <b-button @click="cancel" id="enter">Cancel</b-button>
      <b-input
        placeholder="message"
        class="um"
        v-model="currentMessage"
      ></b-input>
      <b-button @click="send" id="enter">Send</b-button>
      <b-button
        pill
        variant="outline-success"
        v-for="(message, index) in messages"
        :key="index"
        class="um"
        >{{ message.message }}</b-button
      >
    </template>
    <template v-else>
      <b-button @click="getUsers" id="enter">Get Users</b-button>
      <template v-if="users !== null">
        <b-button
          pill
          variant="outline-danger"
          v-for="(user, index) in users"
          :key="index"
          class="um"
          @click="selectUser(user.name)"
          >{{ user.name }}</b-button
        >
      </template>
    </template>
  </div>
</template>

<style scoped>
#chat {
  border: 1px dashed #000000;
  border-radius: 10px;
  background-color: #11111108;
  min-height: 100%;
  padding: 5px;
}
#enter {
  margin: 0 auto;
  width: 70%;
  display: block;
}
.um {
  display: block;
  margin: 15px auto;
  width: 70%;
}
</style>

<script>
export default {
  methods: {
    enter: async function() {
      try {
        await this.$http.post("/chat/enter/");
        this.entered = true;
      } catch (e) {
        void 0;
      }
    },
    getUsers: async function() {
      try {
        const response = await this.$http.get("/chat/users/");
        const {
          data: { result: users }
        } = response;
        this.users = users;
      } catch (e) {
        this.users = [];
      }
    },
    send: async function() {
      await this.$http.post("/chat/send_message/", {
        to: this.selectedUser,
        message: this.currentMessage
      });
    },
    selectUser: function(name) {
      this.selectedUser = name;
      this.timer = setInterval(this.fetchMessages.bind(this), 1000);
    },
    fetchMessages: async function() {
      const response = await this.$http.post("/chat/get_messages/", {
        to: this.selectedUser
      });

      const {
        data: { result: messages }
      } = response;

      this.messages = messages;
    },
    cancel: function() {
      clearInterval(this.timer);
      this.selectedUser = null;
      this.messages = [];
    }
  },
  data: function() {
    return {
      entered: false,
      users: null,
      selectedUser: null,
      timer: null,
      messages: [],
      currentMessage: ""
    };
  }
};
</script>
