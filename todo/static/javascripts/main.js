$(function() {
  $('a').on('click', function() {
    if ($(this).attr('data-method')) {
      form = $('<form>').css('display', 'none').attr('action', $(this).attr('href')).attr('method', 'post');
      method = $('<input>').attr('type', 'hidden').attr('value', $(this).attr('data-method')).attr('name', '_method').appendTo(form);
      form.appendTo($('body')).submit();
      return false;
    }
  })
})