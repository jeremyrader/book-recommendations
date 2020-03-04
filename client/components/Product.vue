<template>
    <div class="max-w-sm w-full lg:max-w-full lg:flex mb-10">
        <div class="w-full border-r border-b border-l border-gray-400 lg:border-l-0 lg:border-t lg:border-gray-400 bg-white rounded-b lg:rounded-b-none lg:rounded-r p-4 flex flex-col justify-between leading-normal">
            <div v-if="showReviewBox">
                <p v-if="reviews.length === 0" class="mb-5">Be the first to review this recommendation!</p>
                <p v-for="(review, index) in reviews" :key="index">
                    <Review :review="review" />
                </p>
                <div class="flex">
                    <textarea v-model="review" placeholder="review text here" class="w-full mr-5 border border-gray-400 resize-none outline-none"></textarea>
                    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="submitReview">Add a Review</button>
                    <button class="font-bold py-2 px-4 rounded outline-none" @click="closeReviewBox">Cancel</button>
                </div>
                
            </div>
            <div v-else>
                <div class="mb-8">
                    <p v-if="false" class="text-sm text-gray-600 flex items-center">
                        <img src="./reading-list.svg" style="height:30px;" />
                    Book
                    </p>
                    <div class="text-gray-900 font-bold text-xl text-left mb-2">{{ product.title }}</div>
                    <p class="text-gray-700 text-base text-left">{{ product.description }}</p>
                </div>
                <div class="flex items-center">
                    <img class="w-10 h-10 rounded-full mr-4" src="https://lh3.googleusercontent.com/a-/AOh14Gj-L_2-VPPVXS6WKKXyG57FoLqpvBOxQwPr_nrG=s96-c" alt="Avatar of Jonathan Reinink">
                    <div class="text-sm">
                        <p class="text-gray-900 leading-none">{{product.userId}}</p>
                        <p class="text-gray-600">Aug 18</p>
                    </div>
                    <div class="w-3/5"></div>
                    <div class="w-1/5 flex flex-row justify-end">
                        <span v-if="reviews.length > 0" class="flex rounded-full bg-indigo-500 uppercase px-2 py-1 text-xs font-bold mr-3 w-auto">{{ reviews.length }}</span>
                        <button class="bg-teal-500 hover:bg-teal-700 border-teal-500 hover:border-teal-700 text-sm border-4 text-white py-1 px-2 rounded" @click="addReview">View Reviews</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import Review from '../components/Review.vue'

export default {
    props: ['product'],

    components: {
        Review
    },

    data: function() {
        return {
            showReviewBox: false,
            review: '',
            reviews: []
        }
    },

    mounted: async function() {
        console.log(this.product)
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
                .post(`http://localhost:5000/review?id=${this.product.id}&review=${this.review}&userName=${this.$store.state.user.name}`)

            this.showReviewBox = false
            this.reviews = await this.getReviews()

            this.review=''

        },

        closeReviewBox() {
            this.showReviewBox = false
        }
    }

}
</script>