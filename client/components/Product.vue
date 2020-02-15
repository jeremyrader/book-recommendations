<template>
<div class="flex flex-row bg-gray-100 m-5">
  <div class="flex flex-col items-start">
      <h1>{{ product.title }}</h1>

      <div>
          <img height=100 width=100 :src="product.imgSrc" />
      </div>

      <div>
        <a :href="product.url">Link</a>
      </div>
      
  </div>
    <button class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded" @click="addReview">Add a Review</button>
    
    <div v-if="showReviewBox">
        <textarea v-model="review" placeholder="review text here"></textarea>
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="submitReview">Add a Review</button>
    </div>

    <div v-if="reviews.length > 0">
        <p v-for="(review, index) in reviews" :key="index">
            {{ review[2] }}
        </p>
    </div>
    
  </div>
</template>

<script>
import axios from 'axios'

export default {

  props: ['product'],

  data: function() {
    return {
        showReviewBox: false,
        review: '',
        reviews: []
    }
  },

  mounted: async function() {
      this.reviews = await this.getReviews()
  },

  methods: {
    addReview() {
        this.showReviewBox = true
    },

    async getReviews() {
      let res = await axios
        .get(`http://localhost:5000/reviews?id=${this.product.id}`)

      return res.data
    },
    async submitReview() {
        let res = await axios
            .post(`http://localhost:5000/review?id=${this.product.id}&review=${this.review}`)

        this.showReviewBox = false
        this.reviews = await this.getReviews()

        this.review=''

    }
  }

}
</script>