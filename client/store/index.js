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