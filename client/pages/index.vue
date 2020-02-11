<template>
  <div class="container">
    <div>
      <h1 class="title">
        Recommendations
      </h1>

      <input v-model="keyword" type="text" placeholder="Search" @input="filterProducts" />

      <h2 class="subtitle">
        Our favorites
      </h2>
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="addNewProduct">
          Add new
      </button>
      <div v-if="showProductFields == true">
        <form>
          <input v-model="url" type="text" class="bg-gray-100" placeholder="Url"/>
          <input v-model="imgSrc" type="text" placeholder="ImgSrc"/>
          <input v-model="title" type="text" placeholder="Title"/>
          <button type="button" @click="submitNewProduct" :disabled="!imgSrc || !title || !url">
            Complete
          </button>
        </form>

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
      products: [],
      filteredProducts: [],
      showProductFields: false,
      url: '',
      imgSrc: '',
      title: '',
      keyword:'',
    }
  },

  mounted: async function() {
    this.filteredProducts = this.products = await this.getProducts()
  },

  methods: {
    async getProducts() {

      let res = await axios
        .get('http://localhost:5000/products')

      return res.data.products
    },

    addNewProduct() {
      this.showProductFields = true
    },

    async submitNewProduct() {
      let res = await axios
        .post(`http://localhost:5000/product?url=${this.url}&imgSrc=${this.imgSrc}&title=${this.title}`)

      this.products = await this.getProducts()

      this.showProductFields = false
      this.url = '',
      this.imgSrc = '',
      this.title = ''
    },

    filterProducts() {
      this.filteredProducts = this.products.filter(product => product.title.toLowerCase().includes(this.keyword.toLowerCase()))
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
