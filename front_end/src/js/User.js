export class User {
    constructor(messages, domain_origin) {
        console.log("User has been instantiated.")
        this.domain_origin = domain_origin
        this.messages = messages;
        this.login_email = "";
        this.login_password = "";
        this.user = {};
        this.checking = false;
        this.password_authorised = false
        this.mfa_authorised = false
        this.logged_in = true;
        this.mfa_secret_confirmed = false
        this.mfa_qr_image = []
        this.email = ""
        this.name = ""
        this.role_name = ""
        this.ip_address = "127.0.0.1"
        this.mfa_authenticator_code = ""
        this.status = "";
        this.invalid_token = false;
        this.session_jwt = "";
    }

    get_mfa_jwt_from_local_storage(email){
        return localStorage.getItem("mfa_jwt_"+email)
    }

    get_ip_address() {
        const url = "https://api.ipify.org?format=json"
        fetch(url)
            .then(response => response.json())
            .then(api_result => {
                this.ip_address = api_result.ip
            })
            .catch(error => {
                // Unable to get ip address from api, set ip_address to be self 
                this.ip_address = "127.0.0.1"
                console.log(error)
            });
    }

    api_reset_password_request(email) {

        var payload = {}
        payload.email = email
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        };
        var message = ""
        const url = this.domain_origin + '/api_reset_password_request'
        fetch(url, requestOptions)
            .then(response => response.json())
            .then(api_object => {
                this.messages.add_message(api_object.message,"text-success h6")
            })
            .catch(error => {
                console.log(error)
            });
    }

    api_reset_password(input) {

        var payload = {}
        payload.session_jwt = this.session_jwt
        payload.input = input
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        };
        var message = ""
        const url = this.domain_origin + '/api_reset_password'
        fetch(url, requestOptions)
            .then(response => response.json())
            .then(api_object => {

                if(api_object.rc==0){
                    this.messages.add_message(api_object.message, "text-success h6")
                    setTimeout(() => {
                        location.replace("/login")
                    }, 5000);
                }
                else {
                    this.messages.add_message(api_object.message, "text-danger h6")
                }
            })
            .catch(error => {
                console.log(error)
            });

    }

    check_mfa_authenticator_code() {

        // v-model already updated the codes directly into this object

        if (this.password_authorised) {
            var data = {}
            data.session_jwt = this.session_jwt
            data.ip_address = this.ip_address
            data.mfa_authenticator_code = this.mfa_authenticator_code
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            };
            var message = ""
            const url = this.domain_origin + '/api/auth/check_mfa_authenticator_code'
            fetch(url, requestOptions)
                .then(response => response.json())
                .then(api_object => {

                    try {
                        localStorage.removeItem("mfa_" + this.email)                        
                      
                    } catch (error) {   
                        console.log(error)                     
                    }
                    try {
                        localStorage.setItem("mfa_" + this.email,  api_object.mfa_jwt)                          
                      
                    } catch (error) {
                        console.log(error)                     
                        localStorage.setItem("mfa_" + this.email, "")                         
                    }
                    try {
                        if (api_object.mfa_jwt && (api_object.rc==0)){
                            this.mfa_authorised = true
                            this.mfa_secret_confirmed = true
                            this.logged_in = true
                            this.messages.add_message("The code authenticated correctly and you are now logged in ","text-success h6")
                        }
                        else {
                            this.mfa_authorised = false
                            this.logged_in = false
                            this.messages.add_message("The code did not authenticate correctly. It may have just missed the time expiry, get a new code and try again","text-danger h6")
                        }
                    } catch (error) {
                        
                    }
                })
                .catch(error => {
                    console.log(error)
                });
        }

        return data
    }

    getUserFromApi() {
        /*
            This runs a continuous cycle of checking that logged in users are still supposed to be 
            logged in 
            If the mfa_secret on teh db changes, then they will be logged off 
        */
        if (this.logged_in) {
            var data = {}
            data.session_jwt = this.session_jwt
            data.ip_address = this.ip_address
            data.mfa_jwt = localStorage.getItem("mfa_" + this.email)
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            };
            var message = ""
            const url = this.domain_origin + '/api_get_user'
            fetch(url, requestOptions)
                .then(response => response.json())
                .then(api_object => {

                    if (!api_object.user.logged_in) {
                        const showMessage = true
                        this.logOut(showMessage)
                    }
                })
                .catch(error => {
                    console.log(error)
                });
        }

        return data
    }



    // this method will search the cookies and look for the username, and if it finds the username it will
    // fetch the encrypted password before decrypting it and comparing it to the one entered.
    // If correct, the user will be logged_in and the jwt will be created
    login() {
        const mfa_jwt = localStorage.getItem("mfa_"+email)
        const data = {}
        data.email = this.login_email
        data.password = this.login_password
        data.ip_address = this.ip_address
        data.mfa_jwt = mfa_jwt
        this.login_email = "";
        this.login_password = "";
        
        if (this.logged_in == true) {
            this.messages.add_message("Already logged in", "text-danger h6");
        } else {
            // const login_details = { "email": this.login_email, "password": this.login_password };
            const post = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            };
            const url = this.domain_origin + "/api/auth/login"
            fetch(url, post)
            .then(response => response.json())
            .then(api_object => {
                this.session_jwt = api_object.session_jwt

                if(api_object.rc==0){
                    this.messages.add_message(api_object.message, "text-success h6")
                    const user = api_object.user
                    if (user.mfa_authorised) {
                        this.logged_in = true
                        this.mfa_authorised = true
                        this.mfa_secret_confirmed = true

                    }
                    else {
                        // If we are not mfa_authorised, the user needs to provide the correct codes
                        // The vue page opens up a response section to allow that  
                        this.logged_in = false
                        this.mfa_authorised = false
                        this.mfa_secret_confirmed = user.mfa_secret_confirmed
                        this.mfa_qr_image = api_object.mfa_qr_image

                    }
                    
                    if (user.password_authorised) {
                        // If we are not mfa_authorised, the user needs to provide the correct codes
                        // The vue page opens up a response section to allow that  

                        this.password_authorised = true
                        this.email = email
                        this.id = user.id
                        this.name = user.name
                        this.role_name = user.role_name
                        this.session_jwt = user.session_jwt
                        this.failed_login_streak = user.failed_login_streak
                    }
                    else {

                        this.password_authorised = false
                        this.logged_in = false
                        this.email = ""
                        this.id = ""
                        this.name = ""
                        this.role_name = ""
                        this.failed_login_streak = ""
                        this.logout()
                        
                        this.messages.add_message(api_object.message, "text-danger h6")
                        setTimeout(() => {
                            location.replace("/login")
                        }, 5000);                        
                    }                    
                }
                else {
                    setTimeout(() => {
                        location.replace("/login")
                    }, 5000);                        
                    this.messages.add_message(api_object.message, "text-danger h6")
                }
            })
            .catch(error => {
                console.log(error)
            });
        }
        return
    };

    logout() {
        console.log("inside logout method")
        this.logged_in = false;
        this.session_jwt = ""
        this.role_name = ""
        this.email = ""
        this.password_authorised = false;
    }

    get_secret_and_image(secret_and_image) {

        // the secret_and_image is stored in the vue page and passed in

        if (this.logged_in) {
            var data = {}
            data.session_jwt = this.session_jwt
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            };
            var message = ""
            const url = this.domain_origin + '/api_get_secret_and_image'
            fetch(url, requestOptions)
                .then(response => response.json())
                .then(api_object => {

                    if (api_object.rc==0){
                        this.messages.add_message("Us your authenticator app (from Google or Microsoft) to scan the qr-code","text-success h6")
                        const secret = api_object.secret
                        const image = api_object.image
                        secret_and_image.secret = secret
                        secret_and_image.image = image
                    }
                    else {
                        this.messages.add_message("There was a slight problem, if you can't proceed, please try again in 5 minutes","text-danger h6")
                        secret_and_image.secret = "Failed in user.js"
                        secret_and_image.image = ""
                        
                    }


                })
                .catch(error => {
                    secret_and_image.secret = ""
                    secret_and_image.image = ""
                    console.log(error)
                });
        }

        return data
    }    

    setlocalStorage() {
        // can use this to retain logged on status after refresh 
        // todo: retain logged on status after a refresh
        sessionStorage.setItem("user", JSON.stringify({ "logged_in": this.logged_in, role_name: this.role_name }));
    }

    api_reset_password(input) {

        var payload = {}
        payload.session_jwt = this.session_jwt
        payload.input = input
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        };
        var message = ""
        const url = this.domain_origin + '/api_reset_password'
        fetch(url, requestOptions)
            .then(response => response.json())
            .then(apiObject => {

                if(apiObject.rc==0){
                    this.messages.add_message(apiObject.message, "text-success h6")
                    setTimeout(() => {
                        location.replace("/login")
                    }, 5000);
                }
                else {
                    this.messages.add_message(apiObject.message, "text-danger h6")
                }
            })
            .catch(error => {
                console.log(error)
            });

    }
    
    check_token_validity() {
        if (this.logged_in) {
            const api_package = { "token": this.session_jwt };
            const post = {
                method: "POST",
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify(api_package),
            };
        const url = this.domain_origin + '/api/auth/check_jwt' 
        console.log(this.domain_origin)
        console.log(url)  
        fetch(url, post)
        .then((data) => {
                if (!data.ok) {
                    throw Error(data.status);
                }
                return data.json();
            })
            .then((response) => {
                console.log(response);
                if (response.status == "invalid") {
                    this.invalid_token = true;
                } else {
                    console.log("Token valid, still logged in.")
                    // if (response.message) {
                        //     this.messages.add_message(response.message, response.type)
                        // }
                    }
                })
                .catch((error) => {
                    console.log(error);
                });
            }
        }
        }