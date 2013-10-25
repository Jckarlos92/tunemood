$(document).mouseup(function (e)
        {
            var container = $("#login-panel");
            var login_link = $("#login-link");
            var sign_link = $("#sign-up");
            var sign_up_panel = $("#sign-up-panel");

            if(login_link.is(e.target)){
                $("#login-panel").fadeToggle(100);
                login_link.toggleClass('click-menu-button');
            }

            if(sign_link.is(e.target)){
                $("#sign-up-panel").fadeToggle(100);
                sign_link.toggleClass('click-menu-button');
            }

            if (!container.is(e.target)
              && container.has(e.target).length === 0// if the target of the click isn't the container...
                && !login_link.is(e.target)) // ... nor a descendant of the container
            {
                container.hide();
                e.stopPropagation();
                login_link.removeClass('click-menu-button');
            }

            if (!sign_up_panel.is(e.target)
             && sign_up_panel.has(e.target).length === 0// if the target of the click isn't the container...
                && !sign_link.is(e.target)) // ... nor a descendant of the container
            {
                sign_up_panel.hide();
                e.stopPropagation();
                sign_link.removeClass('click-menu-button');
            }

});

function TestingStuff() {

    $('#signup_form').submit(function(event) {

    var formData = $('#signup_form').serialize();

    $.ajax({
    type: 'POST',
    url: '/signup',
    data: formData,
    success: function(data) {
        alert(data)
        $("input[name=email_up]").val("");
        $("input[name=password_up]").val("");
        $("input[name=re_password_up]").val("");
    },
    error: function() {
        alert("Ajax error")
    }
    });
        return false;
    });

}

