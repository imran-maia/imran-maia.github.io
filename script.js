// Java script file: script.js

$(document).ready(function() {
    // Scroll to About section
    $("a[href='#about']").click(function() {
      $('html, body').animate({
        scrollTop: $("#about").offset().top
      }, 800);
    });
  
    // Scroll to Experience section
    $("a[href='#experience']").click(function() {
      $('html, body').animate({
        scrollTop: $("#experience").offset().top
      }, 800);
    });
  
    // Scroll to Education section
    $("a[href='#education']").click(function() {
      $('html, body').animate({
        scrollTop: $("#education").offset().top
      }, 800);
    });
  
    // Scroll to Project section
    $("a[href='#project']").click(function() {
      $('html, body').animate({
        scrollTop: $("#project").offset().top
      }, 800);
    });
  
    // Scroll to Presentation section
    $("a[href='#presentation']").click(function() {
      $('html, body').animate({
        scrollTop: $("#presentation").offset().top
      }, 800);
    });
  });