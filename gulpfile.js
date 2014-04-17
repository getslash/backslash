var argv = require('minimist')(process.argv.slice(2));

var gulp = require("gulp"),
    browserify = require("browserify"),
    rename = require("gulp-rename"),
    uglify = require("gulp-uglify"),
    gulpif = require("gulp-if"),
    source = require("vinyl-source-stream"),
    streamify = require("gulp-streamify"),
    sass = require('gulp-sass'),
    concat = require('gulp-concat'),
    minifyCSS = require('gulp-minify-css');

gulp.task("css", function() {
    return gulp.src('webapp/styles/style.scss')
        .pipe(sass())
        .pipe(gulpif(argv.production, minifyCSS()))
        .pipe(rename("app.css"))
        .pipe(gulp.dest('static/css/'));
});

gulp.task("vendor", function() {

    var deps = [
        "./bower_components/jquery/dist/jquery.js",
        "./bower_components/handlebars/handlebars.js"
    ];

    if (argv.production) {
        deps.push("./bower_components/ember/ember.prod.js");
    } else {
        deps.push("./bower_components/ember/ember.js");
    }

    gulp.src(deps)
    .pipe(concat('vendor.js'))
    .pipe(gulpif(argv.production, streamify(uglify())))
    .pipe(gulp.dest("static/js"));

    gulp.src("bower_components/font-awesome/fonts/*")
    .pipe(gulp.dest("static/fonts"));

});

gulp.task("app", function() {

    return browserify(
        ['./webapp/app.js'],
        {
            extensions: [".js", ".hbs"]
        })
        .bundle({insertGlobals: true, debug: !argv.production, detectGlobals: false})
        .pipe(source('app.js'))
        .pipe(gulpif(argv.production, streamify(uglify())))
        .pipe(gulp.dest('./static/js/'));
});

gulp.task("default", ["app", "vendor", "css"], function() {


});

gulp.task("watch", ["default"], function() {
    gulp.watch(["gulpfile.js", "webapp/**/*.js", "webapp/**/*.hbs", "webapp/**/*.scss"], ["default"]);
});
