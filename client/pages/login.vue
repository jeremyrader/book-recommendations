<template>
  <div>
    <div>
      <h1 class="title">
        Login
      </h1>

      <div id="google-signin-button"></div>
      <p v-if="error">{{error}}</p>
    </div>
  </div>
</template>

<script>

import axios from 'axios'

export default {
  data: function() {
    return {
      authenticated: false,
      error: null
    }
  },

  mounted: async function() {
    gapi.signin2.render('google-signin-button', {
      onsuccess: this.onSignIn
    })
  },

  methods: {
    async onSignIn(googleUser) {

      let domain = googleUser.getHostedDomain()

      if (domain !== 'zennify.com') {
        this.error = 'You must sign in using a zennify.com address'
      }
      else {
          var profile = googleUser.getBasicProfile();

          // The ID token you need to pass to your backend:
          var id_token = googleUser.getAuthResponse().id_token;

          let res = await axios
          .post(`http://localhost:5000/auth?token=${id_token}`)

          if (res.status === 200 && res.data.authorized == false) {
              this.error = 'You must sign in using a zennify.com address'
          }

          if (res.status === 200 && res.data.authorized === true) {
            this.error = null
            this.$store.commit('authorizeUser', { id: profile.getId(), name: profile.getName(), image: profile.getImageUrl()})
            this.$router.push({ name: 'index'})
          }
      }

    },
  }
}
</script>
