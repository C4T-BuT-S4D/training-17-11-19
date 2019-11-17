<template>
  <div id="add-anime">
    <b-form @submit.prevent="onSubmit">
      <b-form-group id="title-fieldset" label="Anime title:" label-for="title">
        <b-form-input
          id="title"
          v-model="form.title"
          type="text"
          required
          placeholder="Enter anime title"
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="desc-fieldset"
        label="Description of anime"
        label-for="descr"
      >
        <b-form-input
          id="descr"
          v-model="form.description"
          type="text"
          required
          placeholder="Once upon a time"
        ></b-form-input>
      </b-form-group>
      <b-form-checkbox
        id="public-check"
        v-model="form.public"
        name="public"
        value="1"
        unchecked-value="0"
      >
        I authorize the free access to this anime
      </b-form-checkbox>
      <b-form-group id="year-fieldset" label="Year" label-for="year-inp">
        <b-form-input
          id="year-inp"
          v-model="form.year"
          type="number"
          placeholder="1337"
        ></b-form-input>
      </b-form-group>
      <b-form-invalid-feedback :state="error === null">
        {{ error }}
      </b-form-invalid-feedback>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        title: "",
        description: "",
        public: "0",
        year: null
      },
      error: null
    };
  },

  methods: {
    onSubmit: async function() {
      try {
        const anime = {
          title: this.form.title,
          description: this.form.description,
          public: this.form.public
        };
        if (this.form.year != null) {
          anime.year = this.form.year;
        }
        await this.$http.post("/db/anime", anime);
        this.error = null;
        this.$router.push({ name: "myList" });
      } catch (e) {
        const { data } = e.response;
        this.error = data;
      }
    }
  }
};
</script>
