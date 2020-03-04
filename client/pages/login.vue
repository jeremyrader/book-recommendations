<template>
    <div class="w-full max-w-xl">
        <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 flex flex-col">
            <h1 class="text-3xl font-bold text-center mb-10">Zenn Recommends</h1>
            <div class="flex flex-row h-35 mb-10">
                <img id="posts" src="../assets/images/posts.svg" class="w-1/4 mr-10"/>
                <p class="w-3/4 flex my-auto text-lg font-thin">
                    Post recommendations for books, movies, podcasts, games, tv shows
                </p>
            </div>
            <div class="flex flex-row h-35 mb-10">
                <p class="w-3/4 flex my-auto text-lg font-thin">
                    Get to know your coworkers and provide recommendations based on their interests
                </p>
                <img src="../assets/images/hangout.svg" class="w-1/4 "/>
            </div>
            <hr class="mb-10 border">
            <div class="flex self-center mb-5" id="google-signin-button"></div>
            <p class="text-center text-gray-500 text-xs" :class="{ 'text-red-600 font-bold': error }">Please sign in using your Zennify email account</p>
        </div>
    </div>
</template>

<script>

import axios from 'axios'

export default {
    layout: 'simple',
	data: function() {
		return {
			authenticated: false,
			error: false
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
				this.error = true
			}
			else {
					var profile = googleUser.getBasicProfile();

					// The ID token you need to pass to your backend:
					var id_token = googleUser.getAuthResponse().id_token;

					let res = await axios
					.post(`http://localhost:5000/auth?token=${id_token}`)

					if (res.status === 200 && res.data.authorized == false) {
						this.error = true
					}

					if (res.status === 200 && res.data.authorized === true) {
						this.$store.commit('authorizeUser', { id: profile.getId(), name: profile.getName(), image: profile.getImageUrl()})
                        this.$router.push({ name: 'index'})
                        this.error = false
					}
			}

		},
	}
}
</script>