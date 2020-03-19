var gulp = require('gulp');
var uglify = require('gulp-uglify')
var concat = require("gulp-concat");
var cssMin = require('gulp-css')


gulp.task('css', function() {
  gulp.src([
    'static/assets/icons/all.min.css',
    "static/assets/css/fonts.css",
    'static/assets/css/jquery-ui.css',
    'static/assets/template-js/autocomplete/easy-autocomplete.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    'https://fonts.googleapis.com/css?family=Montserrat:400,700,200',
    'https://use.fontawesome.com/releases/v5.0.6/css/all.css',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/vanilla-datatables@v1.6.16/dist/vanilla-dataTables.min.css',
    'static/assets/css/styles.css'
  ])
    .pipe(concat('app.css'))
    .pipe(cssMin())
    .pipe(gulp.dest('static/assets/css'))
});

gulp.task('default', ['css'])

