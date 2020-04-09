var gulp = require('gulp');
var uglify = require('gulp-uglify')
var concat = require("gulp-concat");
var cssMin = require('gulp-css')

gulp.task('css', function() {
  gulp.src([
    'static/assets/css/src/imports.css',
    'static/assets/css/src/bootstrap.min.css',
    'static/assets/css/src/font-awesome.min.css',
    'static/assets/css/src/all.css',
    'static/assets/css/src/easy-autocomplete.min.css',
    'static/assets/css/src/vanilla-dataTables.min.css',
    'static/assets/css/src/ranger.min.css',
    'static/assets/css/src/fonts.css',
    'static/assets/css/src/styles.css',
  ])
    .pipe(concat('styles.min.css'))
    // .pipe(cssMin())
    .pipe(gulp.dest('static/assets/css/dist'))
});

gulp.task('default', ['css'])




