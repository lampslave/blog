jQuery(function($) {
    form = $('.comment-form').clone();
    reply = $('.comment-reply-link');
    cancel = $('.comment-reply-cancel-link');
    cancel.hide();

    reply.click(function(e) {
        e.preventDefault();
        reply.show(); // show previous comment's reply link
        cancel.hide(); // hide previous comment's cancel link
        comment = $(this).parents('.comment-wrapper');
        comment.find(cancel).show();
        $(this).hide();
        $('.comment-form').remove();
        form.clone().appendTo(comment);
        $('#id_parent').val($(this).data('id'));
        initPagedown();
    });

    cancel.click(function(e) {
        e.preventDefault();
        comment = $(this).parents('.comment-wrapper');
        comment.find(reply).show();
        $(this).hide();
        $('.comment-form').remove();
        form.clone().appendTo('.comment-form-container');
        initPagedown();
    });
});
