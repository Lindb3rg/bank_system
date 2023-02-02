$(document).ready(function(){

    $('.checkoption').click(function() {
       $('.checkoption').not(this).prop('checked', false);
    });

 });
