var TemplateEngine = function(html, options) {
    var re = /<%([^%>]+)?%>/g, reExp = /(^( )?(if|for|else|switch|case|break|{|}))(.*)?/g, code = 'var r=[];\n', cursor = 0;
    var add = function(line, js) {
        js? (code += line.match(reExp) ? line + '\n' : 'r.push(' + line + ');\n') :
            (code += line != '' ? 'r.push("' + line.replace(/"/g, '\\"') + '");\n' : '');
        return add;
    }
    while(match = re.exec(html)) {
        add(html.slice(cursor, match.index))(match[1], true);
        cursor = match.index + match[0].length;
    }
    add(html.substr(cursor, html.length - cursor));
    code += 'return r.join("");';
    return new Function(code.replace(/[\r\t\n]/g, '')).apply(options);
}

var template = '<div class="corgi_feed_well"> \
                  <div class="individual_feed_item"> \
                    <div class="feed_item"> \
                      <div class="feed_body"> \
                        <div class="row"> \
                          <div class="feed_profile_pic"> \
                            <img src="assets/img/nerd_little.jpg" alt="meta image" class="meta_image"> \
                          </div> \
                          <div class="feed_text"> \
                            <p><%this.text%></p> \
                            <p class=date><%this.date%></p> \
                          </div> \
                        </div> \
                      </div> \
                    </div> \
                  </div> \
                </div>',
    page = 0,
    count,
    pages = 0,
    seconds = 25000,
    difference = 0;

function next_page(){
    $.ajax({
        url: '/page',
        type: 'GET',
        dataType: 'json',
        data: {
            page: page,
            difference: difference,
        },
        success: function(data){
            var str = '';
            for (item in data.phrases){
                str += TemplateEngine(template, {text: data.phrases[item].phrase, date: data.phrases[item].created});
            }
            str = $(str).hide()
            $('.items').append(str)
            str.fadeIn('slow')
            page +=1;
            count = data.count;
            pages = data.pages;
        }
    });
};

function update(){
    if (count){
                $.ajax({
            url: '/update',
            type: 'GET',
            dataType: 'json',
            data: {
                count: count,
            },
            success: function(data){
                if (count < data.count){
                    difference += data.count - count;
                    var str = '';
                    for (item in data.phrases){
                        str += TemplateEngine(template, {text: data.phrases[item].phrase, date: data.phrases[item].created});
                    }
                    str = $(str).hide()
                    $('.items').prepend(str)
                    str.fadeIn('slow')
                    count = data.count
                }
                setTimeout(function() {
                    update();
                }, seconds);
            }
        });
    } else {
        setTimeout(function() {
            update();
        }, seconds);
    }

};

$(document).ready(function () {

    //First page
    next_page();
    //Update
    update();
    //next pages
    $(document).scroll(function() {
        if ((page < pages) && ($(document).scrollTop() + $(window).height() + 300 >= $(document).height())){
            next_page();
        }
    });

});