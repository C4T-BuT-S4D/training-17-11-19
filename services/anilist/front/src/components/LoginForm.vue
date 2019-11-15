<template>
  <div class="form">
    <b-form @submit.prevent="onSubmit">
      <b-form-group
              id="input-group-name"
              label="Name:"
              label-for="input-name"
      >
        <b-form-input
                id="input-name"
                placeholder="Enter name"
                type="text"
                required
                v-model="name"
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-password"
        label="Password:"
        label-for="input-password"
      >
        <b-form-input
          id="input-password"
          v-model="password"
          type="password"
          required
          placeholder="Enter password"
        ></b-form-input>
        <b-form-invalid-feedback :state="error === null">
          {{ error }}
        </b-form-invalid-feedback>
      </b-form-group>
      <b-button type="submit" variant="primary">Login</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
        name: "",
      password: "",
      error: null
    };
  },
  methods: {
    onSubmit: async function() {
      const user = {
          name: this.name,
        password: this.password
      };
      try {
        await this.$http.post("/auth/login", user);
        this.error = null;
        this.$store.commit("setUser", user);
        this.$router.push({ name: "home" });
      } catch (e) {
        const { data } = e.response;
        this.error = data.error;
      }
    }
  }
};
</script>

<style scoped>
.form {
  width: 50%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateY(-50%) translateX(-50%);

  border: 1px dashed #000000;
  border-radius: 20px;
  padding: 15px;
}
</style>
