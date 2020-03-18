<template>
    <div class="flex items-center justify-center text-center mx-20">
        <div>
            <div class="flex justify-end items-center p-4">
                <form class="flex w-full" spellcheck="false">
                    <div class="flex items-center bg-white rounded-full pl-5">
                        <svg v-if="showSearchIcon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-search text-gray-500"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
                        <input class="rounded pl-5 outline-none search" v-model="keyword" type="text" placeholder="Search" @input="filterProducts" @focus="handleSearchFocus" @blur="handleSearchBlur" />
                    </div>
                    
                    <div class="flex items-center border-b border-b-2 border-teal-500 py-2 ml-20">
                        <input
                            v-model="url"
                            class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight outline-none" type="text" placeholder="url" aria-label="Full name">
                        <button
                            @click="submitNewProduct"
                            class="flex-shrink-0 bg-teal-500 hover:bg-teal-700 border-teal-500 hover:border-teal-700 text-sm border-4 text-white py-1 px-2 rounded" type="button">
                            Submit
                        </button>
                    </div>
                </form>
                <div class="flex flex-col border border-gray-500 rounded-lg p-4 cursor-pointer" @click="toggleProfileOptions">
                    <div class="flex items-center font-bold">
                        <img class="w-10 h-10 rounded-full mr-4" :src="user.image" alt="Google User Avatar" />
                        {{user.name}}
                    </div>
                    <a class="flex justify-end font-medium" v-if="showProfileOptions" href="#" @click="signOut">Sign out</a>
                </div>
            </div>
        
            <div class="mt-20 mb-10">
                <h1 class="font-bold text-6xl">Zenn Recommendations</h1>
                <h2 class="subtitle">Our favorites</h2>
            </div>

            <Product v-for="(product, index) in filteredProducts" :product="product" :key="index" />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import Product from '../components/Product.vue'

export default {

  components: {
    Product
  },

  data: function() {
    return {
        showProfileOptions: false,
        products: [],
        filteredProducts: [],
        showProductFields: false,
        url: '',
        keyword:'',
        showSearchIcon: true
    }
  },

  mounted: async function() {
    if (!this.$store.state.authorized) {
      this.$router.push({ path: '/login'})
    }
    else {
      this.filteredProducts = this.products = await this.getProducts()
    }
  },
  computed: {
    user() {
      return this.$store.state.user
    }
  },
  methods: {
    async getProducts() {
      let res = await axios
        .get('http://localhost:5000/products')

      return res.data
    },

    async submitNewProduct() {
      let res = await axios
        .post(`http://localhost:5000/product?url=${this.url}&userName=${this.$store.state.user.name}`)

      this.products = await this.getProducts()

      this.url = ''
    },

    filterProducts() {
      this.filteredProducts = this.products.filter(product => product.title.toLowerCase().includes(this.keyword.toLowerCase()))
    },

    signOut() {
      var auth2 = gapi.auth2.getAuthInstance();
      auth2.signOut().then(() => {
        this.$store.commit('unauthorizeUser')
        this.$router.push({ name: 'login'})
      });
    },

    toggleProfileOptions() {
        this.showProfileOptions = !this.showProfileOptions
    },

    handleSearchFocus() {
        this.showSearchIcon = false
    },

    handleSearchBlur() {
        this.showSearchIcon = true
    }

  }

}
</script>

<style>
/* Sample `apply` at-rules with Tailwind CSS
.container {
  @apply min-h-screen flex justify-center items-center text-center mx-auto;
}
*/
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>
