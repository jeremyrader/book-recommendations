<template>
    <div class="border border-gray-400 mb-5 flex flex-row">
        <p class="text-left w-4/5">
            "{{ review[2] }}"
        </p>
        <div class="flex flex-col w-1/5">
            <div class="flex justify-between items-center">
                {{review[3]}}
                <img class="w-10 h-10 rounded-full mr-4" src="https://lh3.googleusercontent.com/a-/AOh14Gj-L_2-VPPVXS6WKKXyG57FoLqpvBOxQwPr_nrG=s96-c" alt="Avatar of Jonathan Reinink" />
            </div>
            <div class="">
                Aug 18
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    props: ['review'],

    data: function() {
        return {
        }
  },

  mounted: async function() {
  },

  methods: {
  }

}
</script>