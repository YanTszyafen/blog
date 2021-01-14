var vm = new Vue({
    el: '#app',
    // Modify the reading syntax of Vue variables to avoid conflicts with django template syntax
    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        is_login:true,
        username:''
    },
    mounted(){
        this.username=getCookie('username');
        this.is_login=getCookie('is_login');
        //this.is_login=true
    },
    methods: {
        //show the menu
        show_menu_click:function(){
            this.show_menu = !this.show_menu ;
        },
    }
});
