document.addEventListener('keydown', (k) => {
    if (k.keyCode == 13) {
        k.preventDefault();
        return false;
    }
});

let cancel_handler = (post, form, comment, cancel) => {
    post.removeChild(form);
    cancel.classList.add("hidden");
    comment.classList.remove("hidden");
};

let comment_box = (comment) => {
    let post_meta = comment.parentNode;
    let post = post_meta.parentNode;
    let post_id = post.id;
    let form = document.createElement('form');
    let div = document.createElement('div');
    let author = document.createElement('input');
    let input = document.createElement('textarea');
    let submit = document.createElement('input');
    let cancel = document.createElement('span');

    cancel.classList.add("comment");
    cancel.innerText = "Cancel";
    form.action = "/comment?postid=" + post_id;
    form.method = "post";
    form.id = "comment";
    author.type = "text";
    author.id = "author";
    author.name = "author";
    author.placeholder = "Username";
    input.placeholder = "Comment...";
    input.rows = "5";
    input.cols = "75";
    input.id = "comment";
    input.name = "comment";
    submit.type = "submit";
    submit.value = ">>";
    submit.classList.add("submit");
    comment.classList.add("hidden");

    div.append(author);
    div.append(input);
    form.append(div);
    form.append(submit);
    post.append(form);
    post_meta.append(cancel);

    cancel.addEventListener('click', () => {cancel_handler(post, form, comment, cancel)});
};

document.querySelectorAll('#comment').forEach( comment => {
    comment.addEventListener('click', () => {comment_box(comment)});
});

