<template>
  <div id="upload">
    <b-form @submit.prevent="onSubmit">
      <b-form-group id="name-fieldset" label="Anime name:" label-for="name">
        <b-form-input
          id="name"
          v-model="form.name"
          type="text"
          required
          placeholder="Enter anime name"
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="files-fieldset"
        description="See frame format at your backend :)"
        label="Upload your anime frames"
        label-for="files"
      >
        <b-form-file
          id="files"
          v-model="form.framesFiles"
          :state="Boolean(form.framesFiles)"
          placeholder="Choose frames files or drop it here..."
          drop-placeholder="Drop files here..."
          :file-name-formatter="formatNames"
          multiple
        ></b-form-file>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
    <div v-if="progressStage !== ''">
      <h5>{{ progressStage }}</h5>
      <b-progress
        :value="progressValue"
        :max="progressMax"
        show-value
        class="mb-3"
      ></b-progress>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        framesFiles: [],
        name: ""
      },
      progressValue: 0,
      progressMax: 100,
      progressStage: ""
    };
  },

  methods: {
    readUploadedFileAsArrayBuffer: async function(inputFile) {
      const temporaryFileReader = new FileReader();

      return new Promise((resolve, reject) => {
        temporaryFileReader.onerror = () => {
          temporaryFileReader.abort();
          reject(new DOMException("Problem parsing input file."));
        };

        temporaryFileReader.onload = () => {
          let binary = "";
          let bytes = new Uint8Array(temporaryFileReader.result);
          let len = bytes.byteLength;
          let curLen = len;
          for (let j = 0; j < 8; j++) {
            binary += String.fromCharCode(curLen % 256);
            curLen /= 256;
          }
          for (let j = 0; j < len; j++) {
            binary += String.fromCharCode(bytes[j]);
          }
          let b64 = window.btoa(binary);

          resolve(b64);
        };
        temporaryFileReader.readAsArrayBuffer(inputFile);
      });
    },

    onSubmit: async function() {
      let { framesFiles: files, name } = this.form;
      let frames = Array();
      this.progressStage = "Prepairing for upload";
      this.progressMax = files.length;
      this.progressValue = 0;

      for (let element of files) {
        frames.push(await this.readUploadedFileAsArrayBuffer(element));
        this.progressValue += 1;
      }

      this.progressStage = "Uploading";
      this.progressMax = files.length;
      this.progressValue = 0;

      try {
        let response = await this.$http.post("/player/init_upload/", {
          name: name
        });
        let {
          data: { token }
        } = response;
        for (let i = 0; i < frames.length; i += 30) {
          let chunk = frames.slice(i, i + 30);
          await this.$http.post("/player/upload_chunk/", {
            token: token,
            start: i,
            frames: chunk
          });
          this.progressValue += chunk.length;
        }
        this.progressStage = "";

        this.$router.push({
          name: "player",
          params: {
            token: token
          }
        });
      } catch (error) {
        void 0;
      }
    },

    formatNames(files) {
      if (files.length === 1) {
        return files[0].name;
      } else {
        return `${files.length} files selected`;
      }
    }
  }
};
</script>
