
function overlay(insert_button){
    const common_overlay = `<div class="common_overlay" role="presentation">
                            <div class="window" id="window" style="z-index:2;"></div>
                            <div class="common_overlay_div" role="dialog">
                                <div class="common_overlay_div2">
                                    <div class="common_overlay_items" >
                                        ${insert_button}
                                        <button id="cancel_overlay" class="cancel overlay_button" tabindex="0">Cancel</button>
                                    </div>
                                </div>
                            </div>
                        </div>`;
    return common_overlay;
}

function comment_option_clicked(){
    $('.comment_option').on('click',function(){
        const c_id = $(this).data('id');
        const dlt_button = `<button id="comment_delete" class="dlt overlay_button" data-id="${c_id}" tabindex="0">Delete</button>`
        const oly = overlay(dlt_button);
        $('body').append(oly);
        $("#comment_delete").on("click",function(e){
            e.preventDefault();
            $.ajax({
                type: 'get',
                url : deletecommentlink,
                data: {
                    id: $(this).data("id"),
                },
                success:function(data){
                    $('.common_overlay').remove();
                    $(`#comment-div_${data.id}`).remove();
                },
                error:function(e){
                    console.log(e);
                }
            });
        });
        canceloverlay()
    });
}

function comment_option_mouse_events(){
    $('.post_comment_div').mouseover(function(){
        const id = $(this).data('id');
        $(`#comment_option_${id}`).removeAttr('hidden')
    });

    $('.post_comment_div').mouseleave(function(){
        $('.comment_option').attr('hidden','true');
    });
}

function canceloverlay(){
    $('#cancel_overlay').on('click',function(){
        $('.common_overlay').remove();
    });
}

$(function(){
    dropmenu('post_details')
    dropmenuhide('post_details')

    
    comment_option_mouse_events();
    
    comment_option_clicked();

    canceloverlay();

    $('textarea').keyup(function (e) {
        if(e.shiftKey && e.which==13){
            e.preventDefault()
            $('.comment_post_button').removeAttr('disabled')
        }else if(e.which==8||(this.value.length && e.which!=13)){
            if(this.value.length){
                e.preventDefault()
                $('.comment_post_button').removeAttr('disabled')
            }else{
                $('.comment_post_button').attr('disabled','enabled')
            }
        }else if(this.value.length && e.which==13){
            if($('.comment_post_button').attr('disabled')){
                this.value=""
            }
            else{
                $('.comment_post_button').click()
            }
        }else
            $('.comment_post_button').attr('disabled','enabled')
    });

    $("#comment_form").on("submit",function(e){
        e.preventDefault();
        $.ajax({
            type:   "post",
            url:    addcommentlink,
            data:{
                comment : $("#comment").val(),
                post_id : postid,
                csrfmiddlewaretoken : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(response){
                $("#comment_form").trigger("reset");
                $('.comment_post_button').attr('disabled','true')
                newcomment(response);
                
            },
            error: function(e){
                console.log(e);
            }
        });
    });


    const unlike = `<span class="love-span2">
                        <svg aria-label="Unlike" id="love" class="icon" fill="#ed4956" height="24" viewBox="0 0 48 48" width="24">
                            <path d="M34.6 3.1c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 
                            10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5s1.1-.2 1.6-.5c1-.6 2.8-2.2 
                            7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path>
                        </svg>
                    </span>`;
    const like   = `<span class="love-span2">
                        <svg class="icon" id="love" aria-label="Like" fill="#262626" height="24" viewBox="0 0 48 48" width="24">
                            <path d="M34.6 6.1c5.7 0 10.4  5.2 10.4 11.5 0 6.8-5.9 11-11.5 16S25 41.3 24 
                            41.9c-1.1-.7-4.7-4-9.5-8.3-5.7-5-11.5-9.2-11.5-16C3 11.3 7.7 6.1 13.4 6.1c4.2 0 6.5 2 8.1 4.3 
                            1.9 2.6 2.2 3.9 2.5 3.9.3 0 .6-1.3 2.5-3.9 1.6-2.3 3.9-4.3 8.1-4.3m0-3c-4.5 0-7.9 1.8-10.6 
                            5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 
                            2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5.6 0 1.1-.2 1.6-.5 1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 
                            1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path>
                        </svg>
                    </span>`;

    $("#icon-love").on("click",function(e){
        e.preventDefault();
        $.ajax({
            type: 'get',
            url : editlikelink,
            data: {
                id: postid,
                event: $("#love").attr('aria-label')
            },
            success:function(data){
                $('#love-div').empty();
                if(data.button==='Like')
                    $('#love-div').append(like);
                else
                    $('#love-div').append(unlike);
                like_button_response(data);
            },
            error:function(e){
                console.log(e);
            }
        });
    });

    function like_button_response(data){
        if(data.total_likes==0)
            $('section.post_likes').remove();
        else if(data.total_likes==1){
            $('section.post_likes').remove();
            const wholikesit = `<section class="post_likes">
                                    <div class="post_likes_div">
                                        <div class="first_liker_propic_div">
                                            <div class="first_liker_propic_div2">
                                                <span class="first_liker_propic_span">
                                                    <img class="first_liker_propic" src="${data.last_liker_propic}" alt="${data.last_liker_name}'s propic"/>
                                                </span>
                                            </div>
                                        </div>
                                        <div class="who_likes_it">Liked by <span class="first_liker_span"><a class="first_liker_prolink" href="/${data.last_liker_name}/">${data.last_liker_name}</a></span></div>
                                    </div>
                                </section>`
            $('.pd_post_likecomment').append(wholikesit);
        }else{
            if(data.total_likes>2 || data.button==='Like')
                $('.total_liker_button').html(`<span>${data.total_likes-1}</span> other${data.total_likes-1 > 1 ? "s" : ""}`);
            else
                $('.who_likes_it').append(` and <button class="total_liker_button"><span>${data.total_likes-1}</span> other</button>`);
        }
    }

    function newcomment(data){
        id = data.id
        name = data.name;
        propic = data.propic;
        profileurl = profilelink.replace('name',name);
        comment = data.comment;
        const d = new Date();
        const month = ['Jan.','Feb.','Mar.', 'Apr.','May.','Jun.','Jul.','Aug.','Sept.','Oct.','Nov.','Dec.'];
        const m = month[d.getMonth()];
        const dd = d.getDate();
        const y = d.getFullYear();
        const newcomment = `<div id="comment-div_${id}" data-id="${id}" class="post_comment_div">
                                <li class="comment_li">
                                    <div class="post_comment_div2">
                                        <div class="main_comment_div">
                                            <div class="pd_header_propic_div" style="margin: 0 18px 0 0;">
                                                <canvas height="42" style="position: absolute; top: -5px; left: -5px; width: 42px; height: 42px;user-select: none;" width="42"></canvas>
                                                <a class="header_propiclink" href="${profileurl}">
                                                    <img class="header_propic" src="${propic}" alt="${name}'s propic">
                                                </a>
                                            </div>
                                            <div class="comment_and_commenter_div">
                                                <h3 class="commenter_header" >
                                                    <div class="commenter_div">
                                                        <span class="commenter_span">
                                                            <a class="header_usernamelink" href="${profileurl}">${name}</a>
                                                        </span>
                                                    </div>
                                                </h3>
                                                <span>${comment}</span>
                                                <div class="comment_time_and_reply">
                                                    <span class="comment_time_span">
                                                        <time class="comment_time" datetime="${d}" title="${m} ${dd}, ${y}" >${m} ${dd}, ${y}</time>
                                                    </span>
                                                    <button class="comment_reply">Reply</button>
                                                </div>
                                            </div>
                                        </div>
                                        <div id="comment_option_${id}" data-id="${id}" class="comment_option" style="height: 32px;" hidden>
                                            <button class="comment_option_button">
                                                <div class="comment_option_div">
                                                    <svg aria-label="Comment Options" class="icon" fill="#8e8e8e" height="16" viewBox="0 0 48 48" width="16">
                                                        <circle clip-rule="evenodd" cx="8" cy="24" fill-rule="evenodd" r="4.5"></circle>
                                                        <circle clip-rule="evenodd" cx="24" cy="24" fill-rule="evenodd" r="4.5"></circle>
                                                        <circle clip-rule="evenodd" cx="40" cy="24" fill-rule="evenodd" r="4.5"></circle>
                                                    </svg>
                                                </div>
                                            </button>
                                        </div>
                                    </div>
                                </li>
                            </div>`;
        $(".post_comment_ul").append(newcomment);
        comment_option_mouse_events();
        comment_option_clicked();
    }

    $('#icon-comment,.comment_reply').on('click',function(){
        $('.comment_textarea').focus();
    });

});