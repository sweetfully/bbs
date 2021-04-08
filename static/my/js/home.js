$(function () {
    $("#concern-tab").on("click", function () {
        get_recommend_list(1, $("#concern .recommend-body"));
    });
    $("#article-tab").on("click", function () {
        console.log("1");
        get_recommend_list(2, $("#article .recommend-body"));
    });
    $("#concern-tab").click();

    // 点击左侧导航栏切换选中样式
    $(".home-nav a").on("click", function () {
        $(".home-nav a").each(function(){
            $(this).removeClass("active");
        });
        $(this).addClass("active");
    });

    function get_recommend_list(type, jElement) {
        $.ajax(
            {
                url: '/get_recommend_people/?type=' + type,
                type: 'get',
                dataType: 'json',
                success: function (data) {
                    if (data.status == 0) {
                        if (type == 1) {
                            span_icon = "glyphicon glyphicon-star"
                        } else if (type == 2) {
                            span_icon = "glyphicon glyphicon-list-alt"
                        } else {
                            span_icon = ""
                        }
                        jElement.empty();
                        for (i = 0; i < data.data.length; i++) {
                            str = '<div class="media"><div class="media-left"><a href="/blog/' + data.data[i].username + '/home">' +
                                '<img class="media-object blog-avatar img-circle" src="' + data.data[i].avatar
                                + '" alt="用户头像" title ="' + data.data[i].username + '"></a></div>' +
                                '<div class="media-body">' +
                                '<h4 class="media-heading"><a href="/blog/' + data.data[i].username + '/home">' +
                                data.data[i].user_nick + '</a></h4>' + data.data[i].user_info + '</div>' +
                                '<div class="media-right text-center"><span><span class="' + span_icon + '">' +
                                '</span>' + data.data[i].count + '</span></div></div>';
                            jElement.html(jElement.html() + str);
                        }
                    }
                },
            }
        );
    }
});