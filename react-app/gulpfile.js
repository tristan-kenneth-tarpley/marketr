var gulp = require('gulp');
var uglify = require('gulp-uglify')
var concat = require("gulp-concat");
var cssMin = require('gulp-css')

gulp.task('css', function() {
  gulp.src([
    '/static/assets/css/styles.css',
    '/static/assets/css/jquery-ui.css',
    '/static/assets/template-js/autocomplete/easy-autocomplete.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
  ])
    .pipe(concat('app.css'))
    .pipe(cssMin())
    .pipe(gulp.dest('/static/assets/css'))
});

gulp.task('default', ['css'])

