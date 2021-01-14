var vm = new Vue({
    el: '#app',

    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        username:'',
        username_error:false,
        username_error_message:'Username error',
        password:'',
        password_error:false,
        password_error_message:'Wrong password',
        password2:'',
        password2_error:false,
        password2_error_message:'Inconsistent passwords',
        uuid:'',
        image_code:'',
        image_code_error:false,
        image_code_error_message:'Image verification code error',
        image_code_url:''
    },
    mounted(){
        this.generate_image_code()
    },
    methods: {
        generateUUID: function () {
            var d = new Date().getTime();
            if (window.performance && typeof window.performance.now === "function") {
                d += performance.now(); //use high-precision timer if available
            }
            var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
                var r = (d + Math.random() * 16) % 16 | 0;
                d = Math.floor(d / 16);
                return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
            });
            return uuid;
        },

        generate_image_code: function () {

            this.uuid = this.generateUUID();

            this.image_code_url = this.host + "/imagecode/?uuid=" + this.uuid;
        },

        check_username: function(){
            var re = /^[0-9A-Za-z]{4,15}$/;
            if (re.test(this.username)) {
                this.username_error = false;
            } else {
                this.username_error = true;
            }
        },

        check_password:function () {
            var re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.password_error = false;
            } else {
                this.password_error = true;
            }
        },

        check_password2:function () {
            if (this.password != this.password2) {
                this.password2_error = true;
            } else {
                this.password2_error = false;
            }
        },

        check_image_code:function () {
            if (!this.image_code) {
                this.image_code_error = true;
            } else {
                this.image_code_error = false;
            }
        },

        on_submit:function () {
            this.check_username();
            this.check_password();
            this.check_password2();

            if (this.username_error == true || this.password_error == true || this.password2_error == true
                || this.image_code_error == true) {

                window.returnValue = false;
            }
        }
    }
});
