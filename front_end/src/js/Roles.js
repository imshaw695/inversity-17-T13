
class Roles {
    // class methods
    constructor(domain_origin, user) {
        this.objectName = "Roles"
        this.model_name = "Role"
        this.domain_origin = domain_origin
        this.user = user

        this.roles = []

        this.test = "hey there from Roles"

        this.counter = 0

    }

    get_roles_from_api() {
        const url = this.domain_origin + "/api/users/roles"

        const requestOptions = {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.user.session_jwt}`,
            },
          };

        fetch(url, requestOptions)
            .then(response => response.json())
            .then(response_package => {
                if (response_package.rc==0){
                    this.roles = response_package.records
                }
            })
            .catch(error => {
                console.log(error)
            });

        return

    }

    get_roles() {
        return this.roles
    }


    get_role_from_id(id) {

        for (let role_index = 0; role_index < this.roles.length; role_index++) {
            const role = this.roles[role_index]
            if (role.id == id) {
                return role
            }
        }

        return {}
    }

    get_role_from_name(name) {

        for (let role_index = 0; role_index < this.roles.length; role_index++) {
            const role = this.roles[role_index]
            if (role.name == name) {
                return role
            }
        }

        return {}
    }

}

export default Roles