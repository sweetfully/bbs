from django import template  # 导入包

# 创建注册器 变量名必须为register
register = template.Library()


@register.inclusion_tag('page.html')
def page(total_num, current_num, url_prefix, page_max_num=9):
    '''
        total_num  总页数
        current_num 当前页数
        url_prefix  链接前缀
        page_max_num  展示页数（默认展示9页）
    '''
    # 用于标签拼接
    page_list = []
    # 判断总页数和固定页数大小关系，如果总页数小于固定展示页数，固定页复制为总页数
    page_max_num = page_max_num if page_max_num < total_num else total_num
    # 定义一个中间变量用于当前页居中
    half_num = page_max_num // 2

    # 计算开始页
    start_num = current_num - half_num
    # 计算结束页
    end_num = current_num + half_num
    # 异常赋值，如url手动把page值改为0.5等负数情况
    if start_num < 1:
        start_num = 1
        end_num = page_max_num
    if end_num > total_num:
        end_num = total_num
        start_num = total_num - page_max_num + 1

    # 生成页面
    if current_num == 1:
        page_list.append(
            '<li class="disabled"><span aria-label="Previous">首页</span></li>'
        )
        page_list.append(
            '<li class="disabled"><span aria-label="Previous">&laquo;</span></li>'
        )
    else:
        page_list.append(
            '<li><a href="{}?page={}" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'.format(
                url_prefix, 1)
        )
        page_list.append(
            '<li><a href="{}?page={}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                url_prefix, current_num - 1)
        )
    for i in range(start_num, end_num + 1):
        if i == current_num:
            page_list.append(
                ' <li class="active"><a href="#">{}</a></li>'.format(i)
            )
        else:
            page_list.append(
                ' <li><a href="{}?page={}">{}</a></li>'.format(url_prefix, i, i)
            )
    if current_num == total_num:
        page_list.append(
            '<li class="disabled"><span aria-label="Next">&raquo;</span></li>'
        )
        page_list.append(
            '<li class="disabled"><span aria-label="Next">尾页</span></li>'
        )
    else:
        page_list.append(
            '<li><a href="{}?page={}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                url_prefix, total_num)
        )
        page_list.append(
            '<li ><a href="{}?page={}" aria-label="Previous"><span aria-hidden="true">尾页</span></a></li>'.format(
                url_prefix, total_num)
        )
    page_list_str = "".join(page_list)

    return {'page_list': page_list_str}
