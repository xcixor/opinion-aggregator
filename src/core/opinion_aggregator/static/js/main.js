$(document).ready(function(){
    $('.sidenav').sidenav();
    $(".dropdown-trigger").dropdown(
        {
          'hover':'false',
          'closeOnClick': false
        }
      );
    $('#close').on('click', function () {
      $('.sidenav').sidenav('close');
      $('.hidden').addClass('hidden');
     });
  });

$('#search').on('focus', function(){
  $('.above-input').css('display', 'none');
});

$('#search').on('focusout', function(){
  $('.above-input').css('display', 'block');
});

$('#dropDownForm').on('click', function () {
  $('.hidden').toggle();
 });
