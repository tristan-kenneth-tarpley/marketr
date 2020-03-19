var gulp = require('gulp');
var uglify = require('gulp-uglify')
var concat = require("gulp-concat");
var cssMin = require('gulp-css')
var concatCss = require('gulp-concat-css');


gulp.task('css', function() {
  gulp.src([
    'static/assets/css/build/font-awesome.min.css',
    'static/assets/css/build/easy-autocomplete.min.css',
    'static/assets/css/build/fonts.css',
    'static/assets/css/build/styles.css',
    'static/assets/css/build/vanilla-dataTables.min.css',
    'static/assets/css/build/bootstrap.min.css',
    'static/assets/css/build/all.css'
  ])
    .pipe(concatCss('app.min.css'))
    .pipe(cssMin())
    .pipe(gulp.dest('static/assets/css'))
});

gulp.task('default', ['css'])

