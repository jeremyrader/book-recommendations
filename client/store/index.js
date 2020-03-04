import VuexPersistence from 'vuex-persist'

const vuexLocal = new VuexPersistence({
    storage: window.localStorage
})

export const state = () => ({
    authorized: false,
    user: {}
})
  
export const mutations = {
    authorizeUser (state, user) {
        state.authorized = true
        state.user = user
    },
    unauthorizeUser (state) {
        state.authorized = false
    }
}

export const plugins = [new VuexPersistence().plugin]