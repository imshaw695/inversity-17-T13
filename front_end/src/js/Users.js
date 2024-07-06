export class Users {
  constructor(user, messages, domain_origin, roles) {
    console.log("Users has been instantiated.")
    this.messages = messages;
    this.roles = roles;
    this.user = user;
    this.domain_origin = domain_origin;
    this.user_list = [];
    this.new_user = {};
    this.new_user.name = "";
    this.new_user.email = "";
    this.new_user.role = "";
    this.user_to_delete = "";
    this.selected_users = [];
    this.model_name = "User";
    this.role_valid = "";
    this.email_valid = "";
    this.name_valid = "";
    this.password_valid = "";
  }
  api_create_user_db() {
    console.log("inside api_create_user_db")

    // Take a copy then reset object attributes
    let new_user_credentials = this.new_user

    // const keys = Object.keys(this.new_user)
    // for (let index = 0; index < keys.length; index++) {
    //     this.new_user[keys[index]] = ""
    // }

    // get the role that we need for a user 
    const role = this.roles.get_role_from_name(this.new_user.role);
    // add a fake id first so the reactivity can keep track of it
    new_user_credentials.id = this.generate_token()
    new_user_credentials.role_id = role.id
    // first we have to add the pogramme to the local copy 
    this.selected_users.push(new_user_credentials)

    // construct the payload to go with the api
    const payload = {}

    // put the package into data and data into the payload
    payload.new_user_credentials = new_user_credentials

    const request_options = {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.user.session_jwt}`,
      },
      body: JSON.stringify(payload)
    };

    const url = this.domain_origin + "/api/users/"
    fetch(url, request_options)
      .then(response => response.json())
      .then(data => {

        if (data.rc == 0) {
          this.messages.add_message(data.message, "text-success h6")
          // We need to get the temporarily added id and update the id  
          const created_record = data.created_record
          new_user_credentials.id = created_record.id
          this.user_list.push(created_record)
        }
        else {
          this.messages.add_message(data.message, "text-danger h6")
          this.remove_local_selected_user(new_user_credentials.id)
          // The updates have not been applied so we need to get the 
          // correct version of the records directly from the db
        }
      })
      .catch(error => {
        console.log(error)
      });
    return
  }

  api_update_user (user_id, name, form_email, cc_emails, org_objects, is_deleted) {
    return new Promise((resolve, reject) => {
      const org_ids = []
      for (let org_key in org_objects) {
        const org = org_objects[org_key]
        org_ids.push(org.id)
      }
      const payload = {
        org_ids: org_ids,
        name: name,
        cc_emails: cc_emails,
        is_deleted: is_deleted,
        email: form_email
      }

      const request_options = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${this.user.session_jwt}`
        },
        body: JSON.stringify(payload)
      }

      const url = this.domain_origin + `/api/users/${user_id}`
      fetch(url, request_options)
        .then(response => response.json())
        .then(api_object => {
          try {
            if (api_object.rc == 0) {

              resolve(api_object.message)
            } else {
              reject(new Error(api_object.message))
            }
          } catch (error) {
            reject(new Error('Failed to update user'))
          }
        })
        .catch(error => {
          reject(new Error('Failed to update user'))
        })
    })
  }

  delete_user(user_id) {
    console.log("inside delete_user method");

    const user = this.get_selected_user_from_id(user_id)
    user.id = ""

    const payload = {}
    payload.session_jwt = this.user.session_jwt
    payload.model_name = "User"

    const data = {}

    const delete_package = {}
    delete_package.id = user_id

    data.delete_package = delete_package

    payload.data = data
    const request_options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'Authorization': 'Bearer my-token',
      },
      body: JSON.stringify(payload)
    };

    const url = this.domain_origin + "/api_delete_record_db"

    fetch(url, request_options)
      .then(response => response.json())
      .then(data => {
        if (data.rc == 0) {
          this.messages.add_message(data.message, "text-success h6")
          // need to remove the user from this.user_list
          for (let user_index in this.user_list) {
            if (this.user_list[user_index].id == user_id) {
              this.user_list.splice(user_index, 1)
            }
          }
        }
        else {

          // The update was rejected so we need to get a fresh copy of the user data 
          this.messages.add_message(data.message, "text-danger h6")
        }

      })
      .catch(error => {
        console.log(error)
      });
    return
  }

  generate_token(token_length) {
    // generate a token that is random
    if (Number.isFinite(token_length)) {
      token_length = token_length * 1;
    }
    else {
      // default to a length of 12 if not passed or not numeric
      token_length = 12;
    }

    // define the unambiguous characters on the keyboard 
    var token_chars = "aAbBcCdDeEfFgGhHjJkKmMnNpPqQrRsStTuUvVwWxXyYzZ23456789!&-_";

    // initialise the token to nothing
    var token = "£!1Ww"

    // keep adding random characters until done 
    for (var token_index = 0; token_index < token_length; token_index++) {
      var character_index = Math.floor(Math.random() * token_chars.length)
      token = token + token_chars[character_index]
    }
    return token
  }

  remove_local_selected_user(id) {
    // The user was not added so we need to remove it from this temporary list
    for (let index = 0; index < this.selected_users.length; index++) {
      const user = this.selected_users[index]
      if (user.id == id) {
        // This is the entry that needs deleting so do it
        this.selected_users.splice(index, 1)
      }
    }
  }
  populate_user_list() {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-type": "application/json; charset=UTF-8",
        Authorization: `Bearer ${this.user.session_jwt}`,
      },
    };
    const url = this.domain_origin + '/api/users/' 
    fetch(url, requestOptions)
      .then((data) => {
        if (!data.ok) {
          throw Error(data.status);
        }
        return data.json();
      })
      .then((response) => {
        this.user_list = response;
      })
      .catch((error) => {
        console.log(error);
      });
  };

  get_selected_user_from_id(id) {

    for (let index = 0; index < this.selected_users.length; index++) {
      const selected_user = this.selected_users[index]
      if (selected_user.id == id) {
        return selected_user
      }
    }

    return {}

  }

  check_name_valid(name) {
    this.name_valid = "";
    let valid = true;
    var regex = /^[a-zA-Z\s-]+$/;
    const fullname_valid = regex.test(name);
    regex = /^[a-zA-Z\s]+$/;
    const firstname_valid = regex.test(name);
    if (!(fullname_valid) && !(firstname_valid)) {
      valid = false;
    }
    if (valid) {
      this.name_valid = "is-valid";
    } else {
      this.name_valid = "is-invalid"
    }
  }

  check_email_valid(email) {
    this.email_valid = "";
    const regex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
    const valid = regex.test(email);
    if (valid) {
      this.email_valid = "is-valid";
    } else {
      this.email_valid = "is-invalid";
    }
  }

  check_role_valid() {
    this.role_valid = "is-valid";
  }

  check_password_valid(password) {
    this.password_valid = "";
    const valid = this.is_strong_enough(password);
    if (valid) {
      this.password_valid = "is-valid";
    } else {
      this.password_valid = "is-invalid";
    }
  }

  is_strong_enough(password) {
    let strong_enough = true;

    // At least 8 characters long
    if (password.length < 8) {
      strong_enough = false;
    }

    if (password.length > 64) {
      strong_enough = false;
    }

    // Count the occurreences of each character
    let character_dictionary = {};
    for (let character of password) {
      try {
        character_dictionary[character] = character_dictionary[character] + 1;
      } catch {
        character_dictionary[character] = 1;
      }
    }

    // If any character makes up more than half
    for (let character in character_dictionary) {
      let count = character_dictionary[character];
      if (count / password.length > 0.5) {
        strong_enough = false;
      }
    }

    // If there aren't at least 3 different characters
    if (Object.keys(character_dictionary).length < 3) {
      strong_enough = false;
    }

    // Check if it is in the list of bad passwords

    let letters = [
      "a",
      "b",
      "c",
      "d",
      "e",
      "f",
      "g",
      "h",
      "i",
      "j",
      "k",
      "l",
      "m",
      "n",
      "o",
      "p",
      "q",
      "r",
      "s",
      "t",
      "u",
      "v",
      "w",
      "x",
      "y",
      "z",
    ];

    // Check it has at least one uppercase character
    let has_upper_case = false;
    for (let character of password) {
      if (!letters.includes(character.toLowerCase())) {
        continue;
      }
      if (character === character.toUpperCase()) {
        has_upper_case = true;
        break;
      }
    }
    if (!has_upper_case) {
      strong_enough = false;
    }

    // Check it has at least one lowercase character
    let has_lower_case = false;
    for (let character of password) {
      if (!letters.includes(character.toLowerCase())) {
        continue;
      }
      if (character === character.toLowerCase()) {
        has_lower_case = true;
        break;
      }
    }
    if (!has_lower_case) {
      strong_enough = false;
    }

    // Check it has at least one integer
    let has_integer = false;
    for (let character of password) {
      try {
        character = parseInt(character);
        has_integer = true;
        break;
      } catch { }
    }
    if (!has_integer) {
      strong_enough = false;
    }

    // Aa1pch5gthdfw should pass
    // Aa1----- should fail as too many repeats
    // Aa-acbypght- should fail as no digit
    // aa1hlrpdvw should fail as no uppercase
    // AG1PHDRFVSINWP should fail as no lowercase
    // Aa1hlrp should fail as too short aa1hlrpdvw

    return strong_enough;
  }

}