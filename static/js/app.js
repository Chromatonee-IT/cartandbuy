$(function() {
	"use strict";


  new PerfectScrollbar('.cart-list');

// Prevent closing from click inside dropdown

/*$(document).on('click', '.dropdown-menu', function (e) {
  e.stopPropagation();
});*/



 // jquery ready start
 $(document).ready(function() {
  // jQuery code

  $("[data-trigger]").on("click", function(e){
    e.preventDefault();
    e.stopPropagation();
    var offcanvas_id =  $(this).attr('data-trigger');
    $(offcanvas_id).toggleClass("show");
    $('body').toggleClass("offcanvas-active");
    $(".screen-overlay").toggleClass("show");
  }); 

  // Close menu when pressing ESC
  $(document).on('keydown', function(event) {
    if(event.keyCode === 27) {
    $(".mobile-offcanvas").removeClass("show");
    $("body").removeClass("overlay-active");
    }
  });

  $(".btn-close, .screen-overlay").click(function(e){
    $(".screen-overlay").removeClass("show");
    $(".mobile-offcanvas").removeClass("show");
    $("body").removeClass("offcanvas-active");


  }); 


}); // jquery end




$('.dropdown-menu a.dropdown-toggle').on('click', function(e) {
  if (!$(this).next().hasClass('show')) {
    $(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
  }
  var $subMenu = $(this).next(".dropdown-menu");
  $subMenu.toggleClass('show');


  $(this).parents('li.nav-item.dropdown.show').on('hidden.bs.dropdown', function(e) {
    $('.submenu .show').removeClass("show");
  });


  return false;
});





});


