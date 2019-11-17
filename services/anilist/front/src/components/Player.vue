<template>
  <div id="player">
    <div>Anime token: {{ animeToken }}</div>
    <div>Anime name: {{ animeName }}</div>
    <div>
      <pre id="frame" :style="frameStyle">{{
        parsedFrames[this.currentFrame % this.firstEmpty]
      }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    showFrame() {
      this.currentFrame += 1;
      setTimeout(this.showFrame.bind(this), 100);
    },

    loadVideo: async function() {
      let i = 0;
      while (await this.loadVideoChunk(i)) {
        i += 1;
        if (i == 1) {
          this.showFrame();
        }
      }
    },

    loadVideoChunk: async function(current) {
      let start = current * 30;
      let end = (current + 1) * 30 - 1;
      if (this.firstEmpty !== -1 && this.firstEmpty < start) {
        return false;
      }
      await this.loadFrames(start, end);
      await this.parseFrames(start, end);
      return true;
    },

    parseFrames: async function(start, end) {
      let cur = [];
      for (let i = start; i <= end; i += 1) {
        if (this.loadedFrames[i] !== undefined) {
          cur.push(this.loadedFrames[i]);
        }
      }
      const response = await this.$http.post(`/player/parse_chunk/`, {
        frames: cur
      });
      const {
        data: { response: frames }
      } = response;

      frames.forEach((element, i) => {
        this.$set(this.parsedFrames, start + i, atob(element));
      });
    },

    loadFrames: async function(start, end) {
      let token = this.animeToken;
      try {
        const response = await this.$http.get(
          `/player/get_chunk/?token=${token}&start=${start}&end=${end}`
        );
        const {
          data: { response: frames }
        } = response;
        let empty = false;
        let firstEmpty = 0;
        frames.forEach((element, i) => {
          if (!empty) {
            if (element.length === 0) {
              empty = true;
              firstEmpty = start + i;
            } else {
              this.loadedFrames[start + i] = element;
            }
          }
        });
        if (empty) {
          this.firstEmpty = firstEmpty;
        }
      } catch (e) {
        void 0;
      }
    }
  },

  computed: {
    frameStyle: function() {
      return {
        fontSize: `0.01%`,
        letterSpacing: `-0.5px`,
        lineHeight: `0.5`,
        overflow: `hidden`
      };
    }
  },

  mounted: async function() {
    this.animeToken = this.$route.params.token;

    try {
      const response = await this.$http.get(
        `/player/info/?token=${this.animeToken}`
      );
      const {
        data: { name }
      } = response;
      this.animeName = name;
    } catch (e) {
      void 0;
    }

    this.loadVideo();
  },

  data: function() {
    return {
      loadedFrames: {},
      parsedFrames: {},
      firstEmpty: 1000 * 1000 * 1000,
      currentFrame: -1,
      animeName: "",
      animeToken: ""
    };
  }
};
</script>
