<template>
    <div class="container">
        <div>
            <div class="flex justify-end">
                <div class="flex flex-col">
                    <div class="flex items-center">
                        {{user.name}}
                        <img class="w-10 h-10 rounded-full ml-4" src="https://lh3.googleusercontent.com/a-/AOh14Gj-L_2-VPPVXS6WKKXyG57FoLqpvBOxQwPr_nrG=s96-c" alt="Avatar of Jonathan Reinink" />
                    </div>
                    <a href="#" @click="signOut">Sign out</a>
                </div>
            </div>
        
            <h1 class="font-bold text-6xl">Zenn Recommendations</h1>
            <h2 class="subtitle">Our favorites</h2>

            <form class="flex w-full mb-10">
                <div class="flex items-center border-b border-b-2 border-teal-500 py-2 mr-20">
                    <input
                        v-model="url"
                        class="appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" type="text" placeholder="url" aria-label="Full name">
                    <button
                        @click="submitNewProduct"
                        class="flex-shrink-0 bg-teal-500 hover:bg-teal-700 border-teal-500 hover:border-teal-700 text-sm border-4 text-white py-1 px-2 rounded" type="button">
                        Submit
                    </button>
                </div>
                <input v-model="keyword" type="text" placeholder="Search" @input="filterProducts" />
            </form>

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
      products: [],
      filteredProducts: [],
      showProductFields: false,
      url: '',
      keyword:''
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
