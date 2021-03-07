var is_load_data = true;
var like_menu_type = 1;
var current_page = 1;
var favorites_dir_or_list = true;
var favorites_dir_id = -1;
var $concern_div = $(".concern-list");
var $favorites_div = $(".favorites");

function like_user(btn, userId, likeOrNot){
    var operate = 0;
    if (btn.innerHTML === "关注"){
        operate = 1;
        likeOrNot = true;
    }else if(btn.innerHTML === "取消关注") {
        operate = 2;
        likeOrNot = false;
    }
    $.ajax({
        url: "/user/like_or_no_user/",
        type: "get",
        dataType: "json",
        data: {userId: userId, operate: operate},
        success:function (data) {
            console.log(data);
            if (data.status === 0){
                if (likeOrNot){
                    btn.innerHTML="取消关注";
                }else {
                    btn.innerHTML="关注";
                }
            } else if (data.status === 1){
                /// todo 弹框
                alert(data.msg)
            } else if (data.status === 10){
                document.location = "/user/login?next=" + document.location.pathname
            }
        },

    })
}

function get_like_user(userId, type, page) {
    if (type === 1 || type === 2 || type === 3){
        like_menu_type = type;
        is_load_data = true;
        current_page = 1;
    } else {
        type = like_menu_type;
    }
    console.log("类型：" + type);
    $.ajax({
        url: "/user/like_list/",
        method: "get",
        dataType: "json",
        data: {userId: userId, type: type, page: page},
        success: function (data) {
            console.log("关注列表的返回值：");
            console.log(data);
            if (data.status === 0){
                if (page === 1){
                    $concern_div.empty();
                }
                if (data.data.length === 0){
                    if (is_load_data){
                        is_load_data = false;
                        bottom_tip = "<p class=\"blog-content-bottom\">已经到底了，没有更多数据了~ QAQ </p>";
                        $concern_div.html($concern_div.html() + bottom_tip);
                    }
                    return;
                }
                var likeOrNotText = "";
                for (i = 0; i < data.data.length; i++) {
                    if (data.data[i].is_focus === 0){
                        likeOrNotText = "关注";
                    } else if (data.data[i].is_focus === 1) {
                        likeOrNotText = "取消关注";
                    }

                    str =
                        "<div class=\"media concern-list-item\">" +
                        "<div class=\"media-left\">" +
                        "<a href='/blog/" + data.data[i].username + "/home/'>" +
                        "<img class=\"media-object blog-avatar img-circle\"" +
                        " src=\"" + data.data[i].avatar + "\" alt=\"用户头像\" title=\"" + data.data[i].user_nick +
                        "(" + data.data[i].username +")\"></a></div>" +
                        "<div class=\"media-body\">" +
                        "<a href='/blog/" + data.data[i].username + "/home/'>" +
                        "<h4 class=\"media-heading\">" + data.data[i].user_nick + "</h4></a>" +
                        "<p>" + data.data[i].user_info + "</p>" +
                        "<span>关注时间：" + data.data[i].focus_time + "</span>" +
                        "</div>" +
                        "<div class=\"concern-operation\">" +
                        "<button class=\"btn btn-primary\" onclick=\"like_user(this, " + data.data[i].id + ")\">" +
                        likeOrNotText + "</button></div></div>";
                    $concern_div.html($concern_div.html() + str);
                }
            } else if (data.status === 1){
                /// todo 弹框
                alert(data.msg)
            } else if (data.status === 10){
                document.location = "/user/login"
            }
        }
    })
}

function get_favorite_dir_list(userId, page) {
    favorites_dir_or_list = true;
    $.ajax({
        url: "/blog/favorite_dir/",
        method: "get",
        dataType: "json",
        data: {userId: userId, page: page},
        success: function (data) {
            if (data.status === 0){
                if (page === 1){
                    $favorites_div.empty();
                    is_load_data = false;
                    for (i = 0; i < data.data.length; i++) {
                        str = "<div class=\"favorites-list\" onclick=\"" +
                            "get_favorite_list(" + userId + "," + data.data[i].id + ",1)\">" +
                            "<div><h4>" + data.data[i].favorite_name + "</h4>" +
                            "<h5>博客数：" + data.data[i].blog_count + "</h5></div>" +
                            "<div class=\"favorites-date\">" +
                            "更新于：" + data.data[i].create_time + "</div></div>";
                        $favorites_div.html($favorites_div.html() + str);
                    }
                }
            }
        }
    });
}

function get_favorite_list(userId, favorite_dir_id, page) {
    favorites_dir_id = favorite_dir_id;
    favorites_dir_or_list = false;
    console.log(1);
    $.ajax({
        url: "/blog/favorite_list/",
        method: "get",
        dataType: "json",
        data: {userId: userId, favoriteDirId: favorite_dir_id, page: page},
        success: function (data) {
            console.log("收藏列表的返回值：");
            console.log(data);
            if (data.status === 0){
                if (page === 1){
                    $favorites_div.empty();
                    is_load_data = true;
                }
                if (data.data.length === 0){
                    if (is_load_data){
                        is_load_data = false;
                        bottom_tip = "<p class=\"blog-content-bottom\">已经到底了，没有更多数据了~ QAQ </p>";
                        $favorites_div.html($favorites_div.html() + bottom_tip);
                    }
                    return;
                }
                for (i = 0; i < data.data.length; i++) {
                        str = "<div class=\"media blog-body-item\">" +
                            "<h3 class=\"media-heading\">" + data.data[i].title + "</h3>" +
                            "<div class=\"media-left\">" +
                            "<a href=\"#\">" +
                            "<img class=\"media-object blog-avatar img-circle\" src=\"" + data.data[i].user.avatar +
                            "\" alt=\"用户头像\" " +
                            "title=\"" + data.data[i].user.user_nick + "(" + data.data[i].user.username + ")\">" +
                            "</a></div>" +
                            "<div class=\"media-body blog-content\">" + data.data[i].content_paragraph + "</div>" +
                            "<div class=\"media-bottom\">" +
                            "<span class=\"text-primary\">" + data.data[i].user.user_nick + "</span>" +
                            "<span>&nbsp;&nbsp;|&nbsp;&nbsp;</span>" +
                            "<span>" + data.data[i].create_date + "</span>" +
                            "<span class=\"pull-right interval-left\">" +
                            "<span class=\"glyphicon glyphicon-eye-open\"></span>&nbsp;" + data.data[i].read_num + "</span>" +
                            "<span class=\"pull-right interval-left\">" +
                            "<span class=\"glyphicon glyphicon-edit\"></span>&nbsp;" + data.data[i].comment_num + "</span>" +
                            "<span class=\"pull-right\">" +
                            "<span class=\"glyphicon glyphicon-thumbs-up\"></span>&nbsp;" + data.data[i].praise_num + "</span>" +
                            "</div>" +
                            "</div>";
                    $favorites_div.html($favorites_div.html() + str);
                }
            }
        }
    })
}