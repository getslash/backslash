var argv = require('minimist')(process.argv.slice(2));

var gulp = require("gulp"),
    browserify = require("gulp-browserify"),
    rename = require("gulp-rename"),
    uglify = require("gulp-uglify"),
    gulpif = require("gulp-if"),
    sass = require('gulp-sass'),
    minifyCSS = require('gulp-minify-css');
 //   concat = require("gulp-concat-sourcemap");

gulp.task("css", function() {
    return gulp.src('webapp/styles/style.scss')
        .pipe(sass())
        .pipe(gulpif(argv.production, minifyCSS()))
        .pipe(rename("app.css"))
        .pipe(gulp.dest('static/css/'));
});

gulp.task("js", function() {
    return gulp.src(["./webapp/app.js"])
        .pipe(browserify({
            insertGlobals : true,
            extensions: [".js", ".hbs"],
            transform: ['hbsfy'],
            debug: !argv.production,
            shim: {
                jquery: {
                    path: './bower_components/jquery/dist/jquery.min.js',
                    exports: '$'
                },
                Ember: {
                    path: './bower_components/ember/ember.js',
                    exports: 'Ember',
                    depends: {
                        jquery: 'jquery',
                        Handlebars: 'Handlebars'
                    }
                },
                Handlebars: {
                    path: './bower_components/handlebars/handlebars.js',
                    exports: 'Handlebars'
                }
            }}))
        .pipe(rename('app.js'))
        .pipe(gulpif(argv.production, uglify()))
        .pipe(gulp.dest("./static/js"));
});

gulp.task("default", ["js", "css"], function() {


});

gulp.task("watch", ["default"], function() {
    gulp.watch(["gulpfile.js", "webapp/**/*.js", "webapp/**/*.hbs", "webapp/**/*.scss"], ["default"]);
});
