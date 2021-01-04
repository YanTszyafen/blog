var vm = new Vue({
    el: '#app',
    //Modify the reading syntax of Vue variables to avoid conflicts with django template syntax
    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        mobile:'',
        mobile_error:false,
        mobile_error_message:'Phone number error',
        password:'',
        password_error:false,
        password_error_message:'wrong password',
        password2:'',
        password2_error:false,
        password2_error_message:'Inconsistent passwords',
        uuid:'',
        image_code:'',
        image_code_error:false,
        image_code_error_message:'Image verification code error',
        sms_code:'',
        sms_code_error:false,
        sms_code_error_message:'SMS verification code error',
        sms_code_message:'Click for authentication code',
        sending_flag:false,
        image_code_url:''
    },
    mounted(){
        this.generate_image_code()
    },
    methods: {
        //Show drop-down menu
        show_menu_click:function(){
            this.show_menu = !this.show_menu ;
        },
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
        // Generate an image verification code number, and set the src attribute of the image verification code img tag on the page
        generate_image_code: function () {
            // Generate a number: Use uuid more strictly to ensure that the number is unique. If it is not very strict, you can also use a timestamp
            this.uuid = this.generateUUID();
            // Set the src attribute of the image verification code img tag in the page
            this.image_code_url = this.host + "/imagecode/?uuid=" + this.uuid;
        },
        //Check mobile number
        check_mobile: function(){
            var re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.mobile_error = false;
            } else {
                this.mobile_error = true;
            }
        },
        //Check password
        check_password:function () {
            var re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.password_error = false;
            } else {
                this.password_error = true;
            }

        },
        //Check confirm password
        check_password2:function () {
            if (this.password != this.password2) {
                this.password2_error = true;
            } else {
                this.password2_error = false;
            }
        },
        //Check the verification code
        check_image_code:function () {
            if (!this.image_code) {
                this.image_code_error = true;
            } else {
                this.image_code_error = false;
            }
        },
        //Check SMS verification code
        check_sms_code:function () {
            if (!this.sms_code) {
                this.sms_code_error = true;
            } else {
                this.sms_code_error = false;
            }
        },
        //Send SMS verification code
        send_sms_code:function () {
            if (this.sending_flag == true) {
                return;
            }
            this.sending_flag = true;

            // Check the parameters to ensure that the input box has data
            this.check_mobile();
            this.check_image_code();

            if (this.mobile_error == true || this.image_code_error == true) {
                this.sending_flag = false;
                return;
            }

            // Send a request to the back-end interface to send the back-end SMS verification code
            var url = this.host + '/smscode/?mobile=' + this.mobile + '&image_code=' + this.image_code + '&uuid=' + this.uuid;
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    // Indicates that the backend sent SMS successfully
                    if (response.data.code == '0') {
                        // Countdown 60 seconds, after 60 seconds, the user is allowed to click the button to send the SMS verification code again
                        var num = 60;
                        // Set a timer
                        var t = setInterval(() => {
                            if (num == 1) {
                                // If the timer reaches the end, clear the timer object
                                clearInterval(t);
                                // Reply the text displayed by clicking the button to obtain the verification code into the original text
                                this.sms_code_message = 'get SMS verification code';
                                // Restore the onclick event function of the clicked button back
                                this.sending_flag = false;
                            } else {
                                num -= 1;
                                // Show countdown information
                                this.sms_code_message = num + 's';
                            }
                        }, 1000, 60)
                    } else {
                        if (response.data.code == '4001') {
                            //Image verification code error
                            this.image_code_error = true;
                        }
                        this.sms_code_error = true;
                        this.generate_image_code();
                        this.sending_flag = false;
                    }
                })
                .catch(error => {
                    console.log(error.response);
                    this.sending_flag = false;
                })
        },
        //submit
        on_submit:function () {
            this.check_mobile();
            this.check_password();
            this.check_password2();
            this.check_sms_code();

            if (this.mobile_error == true || this.password_error == true || this.password2_error == true
                || this.image_code_error == true || this.sms_code_error == true) {
                // Does not meet the registration conditions: disable the form
                window.event.returnValue = false;
            }
        }
    }
});
