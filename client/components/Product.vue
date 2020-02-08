<template>
  <div>
      <h1>{{ product.title }}</h1>

      <div>
          <img height=100 width=100 :src="product.imgSrc" />
      </div>

      <div>
        <a :href="product.url">Link</a>
      </div>
      
  </div>
</template>

<script>
import axios from 'axios'

export default {

  props: ['product'],

  data: function() {
    return {
    }
  },

  mounted: function() {
      console.log(this.product)
  },

  methods: {
  }

}
</script>