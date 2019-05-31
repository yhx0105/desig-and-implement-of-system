from flask import render_template, redirect, \
    url_for, abort, flash, request, current_app
from flask_login import current_user, login_required
from . import main
from .forms import EditPorfileForm, PostForm, CommentForm, CourserForm, EditProfileAdminForm
from .. import db
from ..models import User, Permission, Post, Comment, Course
from sqlalchemy import or_


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_POST) and form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config[
        'FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    courses = user.courses
    if user is None:
        abort(404)
    return render_template('user.html', user=user, courses=courses)


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditPorfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.position = form.position.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('您的个人简介已更新')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.about_me.data = current_user.about_me
    form.position = current_user.position
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.name = form.name.data
        user.about_me = form.about_me.data
        user.position = form.position.data
        db.session.add(user)
        db.session.commit()
        flash('个人简介已更新~')
        return redirect(url_for('main.user', username=user.username))
    form.username.data = user.username
    form.name.data = user.name
    form.about_me.data = user.about_me
    form.position.data = user.position
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())

        db.session.add(comment)
        db.session.commit()
        flash('评论发表成功~')
        return redirect(url_for('main.post', id=post.id))
    post_model = Post.query.filter(Post.id == id).first()
    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    return render_template('post.html', post=post_model, form=form, comments=comments)


# 管理员发布课程
@main.route('/course', methods=['GET', 'POST'])
@login_required
def course():
    form = CourserForm()
    if form.validate_on_submit():
        course = Course(coursename=form.couresename.data,
                        time=form.time.data)
        db.session.add(course)
        db.session.commit()
        flash('课程发布成功~')
        return redirect(url_for('main.course'))
    courses = Course.query.order_by(Course.timestamp.desc()).all()
    return render_template('course.html', form=form, courses=courses)


# 管理员删除课程
@main.route('/admin_delete_course/<coursename>', methods=['GET', 'POST'])
def admin_delete_course(coursename):
    courses = Course.query.filter_by(coursename=coursename).first()
    if courses:
        db.session.delete(courses)
        db.session.commit()
    return redirect(url_for('main.course', coursename=coursename))


@main.route('/choose/<coursename>')
@login_required
def choose(coursename):
    courses = Course.query.filter_by(coursename=coursename).first()
    if current_user.get_course(courses):
        flash('您已选择了这门课程哦~')
        return redirect(url_for('main.course'))
    current_user.choose_course(courses)
    flash('恭喜您成功选课%s' % courses)
    return redirect(url_for('main.course', coursename=coursename))


@main.route('/unchoose/<coursename>')
@login_required
def unchoose(coursename):
    courses = Course.query.filter_by(coursename=coursename).first()
    if not current_user.get_course(courses):
        flash('您还没选这门课哦~')
        return redirect(url_for('main.course'))
    current_user.delete_course(courses)
    flash('恭喜您退课选课%s' % course)
    return redirect(url_for('main.course', coursename=coursename))


# 查询字符串的方式（？**=**），不需要额外传入参数
@main.route('/search/')
def search():
    q = request.args.get('q')
    condition = or_(Post.title.contains(q), Post.body.contains(q))
    posts = Post.query.filter(condition).all()
    return render_template('index.html', posts=posts)
