var vm = new Vue({
    el: '#app',
    
    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        username:'',
        is_login:false
    },
    mounted(){
        this.username=getCookie('username');
        this.is_login=getCookie('is_login');
    },
    methods: {
        
        show_menu_click:function(){
            this.show_menu = !this.show_menu ;
        }
    }
});
