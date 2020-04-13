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

     $('.datepicker').datepicker({
       'maxDate': new Date(2007, 01, 01),
       'format':'yyyy-mm-dd',
       'autoClose': false,
       'showClearBtn': true
     });

     $('select').formSelect();

     $('.card').on("DOMSubtreeModified",function(){
      alert('changed');
    });

  });

$(document).click(function(event) {
  $target = $(event.target);
  if(!$target.closest('.datepicker').length &&
  $('.datepicker').is(":visible")) {
  }
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

$('#alert_close').click(function(){
  $( "#alert_box" ).fadeOut( "slow", function() {
  });
});

