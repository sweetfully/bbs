$(function () {
    var label_li = [];
    var blog_title;
    var blog_content;
    var blog_text;   // 截取前150个字来做博客的简单内容
    var notyf = new Notyf({delay:3000});
    //配置编辑器
    const E = window.wangEditor;
    const editor = new E("#toolbar-container", "#blog-text-container");
    editor.config.showFullScreen = true;
    editor.config.pasteFilterStyle = false;
    editor.create();

    //博客的推荐类别，点击可以直接输入
    $(".blog-publish-alert .alert-body span.blog-type").on("click", function () {
        //$("#blog-type").attr({"value": $(this).text()});
        $("#blog-type").val($(this).text());
    });

    //标签根据输入长度来更新输入框长度
    $(".alert-body").on("input", ".variable-length-div .variable-length-input", function () {
        var width = textWidth($(this).val()) + 2;
        $(this).width(width)
    });

    //获取文本宽度
    var textWidth = function(text){
        var sensor = $('<pre>'+ text +'</pre>').css({display: 'none'});
        $('body').append(sensor);
        var width = sensor.width();
        sensor.remove();
        return width;
    };

    //博客标签点击关闭，隐藏输入框
    $(".alert-body").on("click", ".variable-length-close",  function () {
        $(this).parent().remove();
    });

    $(".alert-body .add-label").on("click", function () {
        //清空标签列表
        label_li.length = 0;
        var add_input_frame = true;
        $(".variable-length-div .variable-length-input").each(function () {
            var values = $(this).val();
            if (values.trim().length === 0){
                //如何有空的弹框，则不去增加新的弹框
                add_input_frame = false;
            }
            label_li.push(values);
        });
        //如果有空的标签没有输入，那么就不再增加新的标签
        if (!add_input_frame){
            return;
        }
        if (label_li.length < 3){
            $(this).siblings(":first").before("<div class=\"variable-length-div\">" +
            "<input type=\"text\" maxlength=\"10\" class=\"variable-length-input\"/>" +
            "<span class=\"variable-length-close\">&times;</span></div>");
        }
    });
    

    function open_alert() {
        $(".blog-publish-overlay").css("display", "block");
        $(".blog-publish-alert").css("display", "block");
    }
    function close_alert() {
        $(".blog-publish-overlay").css("display", "none");
        $(".blog-publish-alert").css("display", "none");
    }
    $(".publish-btn").on("click", function () {
        blog_content = editor.txt.html();
        blog_text = editor.txt.text().substring(0, 150);   // 截取前150个字来做博客的简单内容
        blog_title = $(".blog-title-input").val();
        if(blog_title === ""){
            alert("博客标题不能为空！");
            return;
        }
        if(blog_content === ""){
            alert("博客内容不能为空！");
            return;
        }
        open_alert();
    });
    $(".close-alert").on("click", close_alert);
    $(".close-alert-btn").on("click", close_alert);

    $(".publish-sure-btn").on("click", function () {
        var blog_type = $("#blog-type").val();
        if (blog_type.length === 0){
            alert("请输入博客类别！");
            return;
        }
        label_li.length = 0;
        $(".variable-length-div .variable-length-input").each(function () {
            var values = $(this).val();
            if (values.trim().length !== 0){
                label_li.push(values);
            }
        });
        if (label_li.length === 0){
            alert("至少要为博客增加一个标签！");
            return;
        }

        var formData = new FormData();
        formData.append("blog_title", blog_title);
        formData.append("blog_content", blog_content);
        formData.append("blog_paragraph", blog_text);
        formData.append("blog_type", blog_type);
        formData.append("blog_label", label_li.join("%|%"));
        $.ajax({
                url: "/blog/write_blog/",
                type: "post",
                dataType: "json",
                processData: false,
                contentType: false,
                data: formData,
                success: function (data) {
                    console.log(data, typeof(data.msg));
                    if (data.status === 0){
                        close_alert();
                        // 进入一个发布成功的页面
                        notyf.confirm("文章发布成功！");
                    }else {
                        notyf.alert(data.msg);
                    }
                }
            });
    });
});