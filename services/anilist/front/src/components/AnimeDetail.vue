<template>
  <div id="anime-detail">
    <div id="animeInfo" v-if="anime !== null">
      <div>
        <h4>
          Title: <b>{{ anime.title }}</b>
        </h4>
      </div>
      <div>Description: {{ anime.description }}</div>
      <div>
        <p>Year: {{ anime.year }}</p>
      </div>
      <p>Links to the series:</p>
      <ul v-for="link in links" v-bind:key="link.id">
        <li>{{ link.content }}</li>
      </ul>
    </div>
    <div id="authorBlock" v-if="isAuthor">
      <br />
      <b-form @submit.prevent="onSubmitAuthor">
        <b-form-group
          id="link-group"
          label="Add Link to view"
          label-for="title"
        >
          <b-form-input
            id="link-input"
            v-model="authorForm.link"
            type="text"
            required
            placeholder="player/kek"
          ></b-form-input>
        </b-form-group>
        <b-form-invalid-feedback :state="error === null">
          {{ error }}
        </b-form-invalid-feedback>
        <b-button type="submit" variant="primary">Add link</b-button>
      </b-form>
      <br />
      Token to share view links: {{ access_token }}
      Send it to someone you want to share this anime.
    </div>
    <div id="noAccess" v-if="!haveAccess">
      <p>
        <b
          >It's looks like you dont have access to the series of this anime. Buy
          or get token from the creator and type it here:</b
        >
      </p>
      <b-form @submit.prevent="onSubmit">
        <b-form-group id="link-group" label="Token" label-for="token">
          <b-form-input
            id="token-input"
            v-model="form.token"
            type="text"
            required
            placeholder="looonng string"
          ></b-form-input>
        </b-form-group>
        <b-form-invalid-feedback :state="error === null">
          {{ error }}
        </b-form-invalid-feedback>
        <b-button type="submit" variant="primary">Get access</b-button>
      </b-form>
      <b-alert variant="info" dismissible :show="isAlert">{{ accessMessage }} </b-alert>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    onSubmitAuthor: async function() {
      try {
        await this.$http.post(`/db/anime/${this.animeId}`, {
          link: this.authorForm.link
        });
        this.error = null;
        this.getDetails();
      } catch (e) {
        const { data } = e.response;
        this.error = data;
      }
    },
    onSubmit: async function() {
      try {
        const response = await this.$http.get("/db/get_access", {
          params: {
            anime: this.animeId,
            token: this.form.token
          }
        });
        const {
          data: { result: accessResult }
        } = response;
        if (accessResult) {
          this.accessMessage = "Access granted";
        } else {
          this.accessMessage = "Bad token";
        }
      } catch (e) {
        this.accessMessage = e;
      }
      this.getDetails();
    },
    getDetails: async function() {
      try {
        const response = await this.$http.get(`/db/anime/${this.animeId}`);
        const {
          data: { result: result }
        } = response;
        console.log(result);
        this.anime = result.anime;
        if (result.links) {
          this.links = result.links;
          this.haveAccess = true;
        }
        this.access_token = result.access_token || null;
      } catch (e) {
        this.anime = null;
        this.links = [];
        this.access_token = null;
        this.haveAccess = false;
      }
    }
  },

  computed: {
    isAuthor: function() {
      return this.access_token != null;
    },
    isAlert: function() {
      return this.accessMessage != "";
    }
  },

  mounted: async function() {
    this.animeId = this.$route.params.animeId;
    await this.getDetails();
  },

  data: function() {
    return {
      animeId: "",
      anime: null,
      links: [],
      access_token: null,
      haveAccess: false,
      error: null,
      accessMessage: "",
      authorForm: {
        link: ""
      },
      form: {
        token: ""
      }
    };
  }
};
</script>
