<template>
  <div class="min-vh-100 d-flex align-items-center">
    <div class="row w-100">
      <div class="col-md-2 col-lg-3 col-xl-4">
      </div>
      <div class="col-md-8 col-lg-6 col-xl-4">
        <div>
          <div class="card  px-0">
            <div class="text-center">
              <img class="card-img-top m-4" src="../assets/dt_squad_logo.png" alt="Logo" style="width:90px;">
            </div>
            <div class="card-body m-3 pb-1 mb-0" v-if="!this.user.password_authorised">
              <div class="row my-2">
                <FloatLabel>
                  <InputText class="form-control" type="email" id="email" name="email" v-model="user.login_email" />
                  <label for="username">Email</label>
                </FloatLabel>
              </div>
              <div class="flex items-center space-x-2 mt-5">
                <div class="flex-1">
                  <FloatLabel>
                    <InputText class="form-control" :type="password_visible ? 'text' : 'password'" name="password"
                      id="password" v-model="this.user.login_password" />
                    <label for="password">Password</label>
                  </FloatLabel>
                </div>
                <div class="cursor-pointer" v-on:click="password_visible = !password_visible">
                  <i :class="password_visible ? 'pi pi-eye' : 'pi pi-eye-slash'" class="text-xl"></i>
                </div>
              </div>
              <div class="flex flex-row items-center space-x-2">
                <div class="flex-1">
                  <p class="text-center text-sm mb-0">
                    <label for="data_usage_checked" class="inline-block">
                      <small>I'm happy with the <strong>Data Usage</strong><br>(tick to enable Login)</small>
                    </label>
                  </p>
                </div>
                <div class="flex-none">
                  <div class="form-check">
                    <Checkbox id="data_usage_checked" value="data_usage_checked" v-model="data_usage_checked" />
                  </div>
                </div>
                <div class="flex-grow">
                  <Button @click="this.login()"
                    :disabled='((data_usage_checked.length == 0) || (this.user.login_email.length == 0) || (this.user.login_password.length == 0))'
                    label="Login" class="w-full" />
                </div>
              </div>
              <div class="row mt-3 mb-0">
                <div class="col-12 d-grid gap-1">
                  <Button
                    class="bg-red-500 text-white text-sm py-1 px-4 rounded my-1 hover:bg-red-600 disabled:opacity-50"
                    :disabled='(this.user.login_email.length == 0)'
                    @click="this.user.api_reset_password_request(this.user.login_email)">
                    Set / Reset Your Password for the email above
                  </Button>
                </div>
              </div>
            </div>
            <!-- mfa stuff here -->
            <div class="card-body mx-3 my-0" v-if="this.user.password_authorised && !this.user.mfa_authorised">
              <div class="row">
                <div class="d-grid gap-1">
                  <span v-if="!this.user.mfa_secret_confirmed && this.user.password_authorised">First
                    set up MFA by following the instructions above the qr-code and then...</span>

                  <p>Enter the code from your authenticator and press [enter] or click the button</p>
                  <div class="input-group">
                    <span class="input-group-text">6 Digit Code</span>
                    <input class="form-control" type="text" id="mfa_authenticator_code" autocomplete="off"
                      name="mfa_authenticator_code" v-model="this.user.mfa_authenticator_code"
                      placeholder="MFA Authenticator code" @keyup.enter="this.user.check_mfa_authenticator_code()" />
                  </div>
                  <button type="button" class="btn btn-primary btn-lg my-1"
                    @click="this.user.check_mfa_authenticator_code()">Check authenticator
                    code</button>
                </div>
              </div>
            </div>
            <div class="card-body border border-1 rounded m-3"
              v-if="!this.user.mfa_secret_confirmed && this.user.password_authorised">
              <h3>Set up MFA
                <a class="btn btn-success btn-sm" target="_blank" href="https://vimeo.com/799113927/57039dd5d5"
                  role="button">2 min. explainer
                  video</a>
              </h3>
              <p>It's now a requirement that all systems used within the Volkswagen Group must be secured
                with "Multi Factor Authentication"
              </p>

              <p>
                Scan this QR Code with the Microsoft or Google Authenticator and enter the 6 digit
                MFA Authenticator Code
                for the <strong>Volkswagen Readiness Tracker</strong> in the field above
              </p>
              <div class="text-center">
                <canvas class="img-fluid w-50" id="qr_code_canvas" width="490" height="490"
                  style=" border: 1px solid black"></canvas>
              </div>
            </div>
            <div class="m-3" v-if="this.user.logged_in && this.mfa_authorised">
              <div class="row">
                <div class="d-grid gap-1">
                  <button type="button" class="btn btn-primary btn-lg my-1" @click="user.logout()">Logout</button>
                </div>
              </div>
            </div>
            <div class="card-body m-3" v-if="(!this.user.password_authorised)">
              <h6 class="card-title">Data Usage</h6>
              <p class="small ">By signing in, you confirm that you are an authorised user and using this
                system in a
                business context. The only
                personal information it contains is your name and email address</p>
              <p class="small ">We will only use the data to monitor the progress made on key tasks </p>
              <p class="small ">There is no personally identifiable sensitive information stored by design
                in
                the
                system and it's your responsibility to not enter data that is personally
                sensitive</p>
              <p class="small "><strong> You must keep your password secret and not share it with anyone
                  else</strong>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      needsVueRefresh: { data: false, keepLooping: false },
      mfa_qr_image_rendered: false,
      password_visible: false,
      data_usage_checked: [],
    };
  },
  methods: {
    go_to_index_if_logged_in() {
      if (this.user.logged_in) {
        this.$router.push("index")
      };
    },
    login() {
      this.user.login();
      this.go_to_index_if_logged_in();
    },
    vue_refresh_login() {
      // console.log("insude vue_refresh_login login")
      try {
        this.needsVueRefresh.data = "";
        this.needsVueRefresh.data =
          this.needsVueRefresh.data + " " + this.user.mfa_authorised;
        this.needsVueRefresh.data =
          this.needsVueRefresh.data + " " + this.user.password_authorised;
        this.needsVueRefresh.data =
          this.needsVueRefresh.data + " " + this.user.mfa_qr_image.length;
        this.needsVueRefresh.data =
          this.needsVueRefresh.data + " " + this.user.mfa_qr_image_rendered;
        this.needsVueRefresh.data =
          this.needsVueRefresh.data + " " + this.user.mfa_authorised;
        this.needsVueRefresh.data =
          this.needsVueRefresh.data + " " + this.user.mfa_secret_confirmed;
        this.needsVueRefresh.data =
          this.needsVueRefresh.data + " " + this.user.logged_in;
      } catch (error) {
        console.log("vue refresh data cannot be calculated");
        console.log(this.user.mfa_qr_image);
        console.log(error);
      }

      if (this.user.mfa_qr_image.length > 0) {
        if (!this.mfa_qr_image_rendered) {
          this.render_qr_code();
        }
      }

      if (this.user.logged_in) {
        this.$router.push("index");
      }

      if (this.needsVueRefresh.keepLooping) {
        const myTimeout = setTimeout(this.vue_refresh_login, 500);
      }
    },
    // check_logged_in() {
    //   // this.users.current_user = this.user.check_logged_in();
    //   if (this.user.logged_in) {
    //     this.$router.push("index")
    //   }
    //   console.log("inside check_logged_in loginview")
    //   this.login_timeout = setTimeout(this.check_logged_in, 5000);
    // },
    render_qr_code() {
      // https://codepen.io/rebelchris/pen/ZEWRoMg

      // const height = this.secret_and_image.image.length
      // const width = this.secret_and_image.image[0].length
      const height = this.user.mfa_qr_image.length;
      const width = this.user.mfa_qr_image[0].length;

      var canvas = document.getElementById("qr_code_canvas");

      // resize the canvas
      canvas.width = width;
      canvas.height = height;

      // get an array of the canvas data
      var ctx = canvas.getContext("2d");

      // draw newly modified pixels back onto the canvas
      ctx.fillRect(0, 0, width, height);
      var my_image_data = ctx.getImageData(0, 0, width, height);
      // prepare data
      const data = my_image_data.data;

      for (var row_index = 0; row_index < height; row_index++) {
        for (var col_index = 0; col_index < width; col_index++) {
          const value = this.user.mfa_qr_image[row_index][col_index];
          if (![0, 255].includes(value)) {
            console.log(value);
          }
          const data_index = row_index * width * 4 + col_index * 4;
          const message = `Data length is: ${data.length}. We are on data_index: ${data_index} Row: ${row_index}, Col: ${col_index} is set to value: ${value}`;

          data[data_index] = value;
          data[data_index + 1] = value;
          data[data_index + 2] = value;
          data[data_index + 3] = 255;
        }
      }

      ctx.putImageData(my_image_data, 0, 0);

      this.mfa_qr_image_rendered = true;
    },
  },
  props: ["users", "user", "roles"],
  created() {
    this.needsVueRefresh.keepLooping = true;
    this.vue_refresh_login();
    // this.check_logged_in();
  },
  beforeUnmount() {
    // we are leaving the page so don't need to keep refershing the local list
    this.needsVueRefresh.keepLooping = false;
    // need to scrap check_logged_in2 as well
    clearTimeout(this.login_timeout)
  },
};
</script>