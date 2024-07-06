<template>

    <div class="min-vh-100 d-flex align-items-center">
        <div class="row w-100">
            <div class="col-md-2 col-lg-3 col-xl-4">
            </div>
            <div class="col-md-8 col-lg-6 col-xl-4">
                <div class="card my-2 px-0">
                    <div class="card-body">
                        <h3 class="card-title">Password Set / Reset</h3>
                        <div v-if="this.input.password_reset_token > 0">
                            <p class="card-text">The link you have clicked on is only valid for a short while. If it has
                                timed out, you will get a rejection message and you will need to send another request at
                                the
                                main login page </p>
                        </div>
                        <p class="card-text">You are about to set / reset your password.</p>
                        <p class="card-text">A password complexity algorithm is in place so choose carefully according
                            to these rules. Your password must:</p>
                        <ul>
                            <li>be between 8 and 64 characters long</li>
                            <li>contain an uppercase character</li>
                            <li>contain a lowercase character</li>
                            <li>contain a numerical character</li>
                            <li>not have more than half the characters as the same character</li>
                            <li>not be one of the passwords that are known to be insecure ("password123" for example)</li>
                        </ul>
                        <p>If your password fails any of these tests, there will be a rejection message.</p>
                        <p class="card-text">We recommend using a password manager to choose secure passwords and help
                            you
                            use them in a convenient way.</p>
                        <p class="card-text">
                            <label for="password" id="password" class="form-label">Enter new password</label>
                            <input class="form-control" :class="this.users.password_valid" type="password" name="password" v-model="input.password_1"
                                placeholder="Password" @change="this.users.check_password_valid(this.input.password_1)"/>
                                <div class="valid-feedback">Strong enough</div>
                        </p>
                        <p class="card-text">
                            <label for="password" id="password" class="form-label">Confirm new password</label>
                            <input class="form-control" type="password" name="password" v-model="input.password_2"
                                placeholder="Password" />
                        </p>
                        <div class="d-grid gap-1">
                            <button type="button" class="btn btn-success btn-lg my-1"
                                @click="this.user.api_reset_password(this.input)">Set / Reset Your Password</button>

                        </div>
                        <div class="d-grid gap-1">
                            
                            <router-link class="btn btn-primary" to="/">Help & Info</router-link>
                        </div>                   
                    </div>
                </div>
            </div>
            <div class="col-md-2 col-lg-3 col-xl-4">
            </div>
        </div>
    </div>

</template>

<script>
export default {
    name: 'PasswordResetView',
    data() {
        return {
            input: {
                password_reset_token: this.$route.query.password_reset_token,
                password_1: "",
                password_2: "",
            }
        }
    },
    methods: {

    },
    props: ["user", 'users'],
}
</script>

<style scoped>

</style>