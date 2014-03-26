var gulp = require("gulp"),
    es6 = require("gulp-es6-module-transpiler"),
    handlebars = require("gulp-ember-handlebars"),
    concat = require("gulp-concat-sourcemap");


gulp.task("javascripts", function() {
    return gulp.src("./webapp/**/*.js")
        .pipe(es6({
            type: "amd"
        }))
        .pipe(concat("app.js"))
        .pipe(gulp.dest("static/js/_build/"));
});

gulp.task('templates', function(){
  return gulp.src(['./webapp/templates/*.hbs'])
    .pipe(handlebars({
        templateRoot: "templates",
        outputType: 'amd'
     }))
    .pipe(concat('templates.js'))
    .pipe(gulp.dest('static/js/_build/'));
});

gulp.task("default", ["javascripts", "templates"], function() {
    gulp.src([
        "bower_components/requirejs/require.js",
        "bower_components/jquery/jquery.js",
        "bower_components/handlebars/handlebars.js",
        "bower_components/ember/ember.js",
        "static/js/_build/templates.js",
        "static/js/_build/app.js"
    ])
        .pipe(concat("app.js", {sourceRoot: "/"}))
        .pipe(gulp.dest("static/js"));
    });

gulp.task("watch", ["default"], function() {
    gulp.watch(["gulpfile.js", "webapp/**/*.js", "webapp/**/*.hbs"], ["default"]);
});
