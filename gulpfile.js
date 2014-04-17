var argv = require('minimist')(process.argv.slice(2));

var gulp = require("gulp"),
    browserify = require("browserify"),
    rename = require("gulp-rename"),
    uglify = require("gulp-uglify"),
    gulpif = require("gulp-if"),
    source = require("vinyl-source-stream"),
    sass = require('gulp-sass'),
    minifyCSS = require('gulp-minify-css');

gulp.task("css", function() {
    return gulp.src('webapp/styles/style.scss')
        .pipe(sass())
        .pipe(gulpif(argv.production, minifyCSS()))
        .pipe(rename("app.css"))
        .pipe(gulp.dest('static/css/'));
});

gulp.task("js", function() {
    return browserify(
        ['./app.js'],
        {
            extensions: [".js", ".hbs"],
            basedir: "./webapp",
            noParse: [
                "../bower_components/jquery/dist/jquery.js",
                "../bower_components/handlebars/handlebars.js",
                "../bower_components/ember/ember.js"
            ]
        })
        .bundle({insertGlobals: true})
        .pipe(source('app.js'))
        .pipe(gulp.dest('./static/js/'));
});

gulp.task("default", ["js", "css"], function() {


});

gulp.task("watch", ["default"], function() {
    gulp.watch(["gulpfile.js", "webapp/**/*.js", "webapp/**/*.hbs", "webapp/**/*.scss"], ["default"]);
});
