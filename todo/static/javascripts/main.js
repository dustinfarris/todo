$(function() {
  $('a').on('click', function() {
    if ($(this).attr('data-confirm')) {
      if (!confirm($(this).attr('data-confirm'))) return false;
    }
    if ($(this).attr('data-method')) {
      csrf_token = $("[name='csrfmiddlewaretoken']").first();
      form = $('<form>').css('display', 'none').attr('action', $(this).attr('href')).attr('method', 'post');
      method = $('<input>').attr('type', 'hidden').attr('value', $(this).attr('data-method')).attr('name', '_method').appendTo(form);
      csrf_token.appendTo(form);
      form.appendTo($('body')).submit();
      return false;
    }
  })
})