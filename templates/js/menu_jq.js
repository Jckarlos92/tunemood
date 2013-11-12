$(document).mouseup(function (e)
        {
            var container = $("#login-panel");
            var login_link = $("#login-link");
            var sign_link = $("#sign-up");
            var sign_up_panel = $("#sign-up-panel");

            $('#happy').click(function() {
                $.ajax({
                type: 'GET',
                data: "tag=happy&song=" + $("#id_song").html(),
                url: '/tag',
                success: function(data) {
                    alert("Tag Succesgful")
                },
                error: function() {
                    alert("Ajax error")
                }
                });
            });

            $('#sad').click(function() {
                $.ajax({
                type: 'GET',
                data: "tag=sad&song=" + $("#id_song").html(),
                url: '/tag',
                success: function() {
                    alert("Tag Succesgful")
                },
                error: function() {
                    alert("Ajax error")
                }
                });
            });

            $('#angry').click(function() {
                $.ajax({
                type: 'GET',
                data: "tag=angry&song=" + $("#id_song").html(),
                url: '/tag',
                success: function() {
                    alert("Tag Succesgful")
                },
                error: function() {
                    alert("Ajax error")
                }
                });
            });

            $('#log-out').click(function() {
                $.ajax({
                type: 'GET',
                url: '/logout',
                success: function() {
                    alert("See you later =)")
                    $("#welcome-label").html("")
                },
                error: function() {
                    alert("Ajax error")
                }
                });
            });

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

function signUp() {

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

function logIn() {

$('#login_form').submit(function(event) {

    var formData = $('#login_form').serialize();

     $.ajax({
    type: 'POST',
    url: '/login',
    data: formData,
    success: function(data) {
        alert(data)
        $("#welcome-label").html(data)
        $("input[name=email]").val("");
        $("input[name=password]").val("");
    },
    error: function() {
        alert("Ajax error")
    }
    });
        return false;
    });

}

$(document).mouseover(function (e){

    var happy = $("#happy");
    var sad = $("#sad");
    var angry = $("#angry");

    if(happy.is(e.target)){
        $('img#happy').attr("src", "css/happy_over.png");
    }
    else
        $('img#happy').attr("src", "css/happy.png");

    if(sad.is(e.target)){
        $('img#sad').attr("src", "css/sad_over.png");
    }
    else
        $('img#sad').attr("src", "css/sad.png");

    if(angry.is(e.target)){
        $('img#angry').attr("src", "css/angry_over.png");
    }
    else
        $('img#angry').attr("src", "css/angry.png");
});



