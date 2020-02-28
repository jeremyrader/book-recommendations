<template>
  <div>
    <div>
      <h1 class="title">
        Login
      </h1>

      <div id="google-signin-button"></div>

    </div>
  </div>
</template>

<script>

import axios from 'axios'

export default {
  data: function() {
    return {
      authenticated: false
    }
  },

  mounted: async function() {
    gapi.signin2.render('google-signin-button', {
      onsuccess: this.onSignIn
    })
  },

  methods: {
    async onSignIn(googleUser) {

        var profile = googleUser.getBasicProfile();

        // The ID token you need to pass to your backend:
        var id_token = googleUser.getAuthResponse().id_token;

        let res = await axios
        .post(`http://localhost:5000/auth?token=${id_token}`)
        
        if (res.status === 200) {
          this.$store.commit('authorizeUser', { id: profile.getId(), name: profile.getName(), image: profile.getImageUrl()})
          this.$router.push({ name: 'index'})
        }

    },
  }
}
</script>
