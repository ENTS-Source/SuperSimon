module.exports = (grunt) ->
  grunt.initConfig
    pkg: grunt.file.readJSON 'package.json'
    clean:
      precompile:
        options:
          force: true
        src: ['build', 'dest']
    copy:
      dist:
        expand: true
        cwd: 'build/app'
        src: ['**']
        dest: 'dest'
      web:
        expand: true
        cwd: 'app'
        src: [
          '**/*.html'
          '**/*.css'
          '**/*.js'
          '**/img/*'
          '**/fonts/*'
        ]
        dest: 'build/app'
      fonts:
        files: [
          {
            expand: true
            dot: true
            cwd: 'bower_components/bootstrap/dist'
            src: ['fonts/*.*']
            dest: 'build/app'
          }
          {
            expand: true
            dot: true
            cwd: 'bower_components/font-awesome'
            src: ['fonts/*.*']
            dest: 'build/app'
          }
        ]
    coffee:
      web:
        options:
          bare: true
        expand: true
        cwd: 'app'
        src: ['**/*.coffee']
        dest: 'build/app'
        ext: '.js'
    useminPrepare:
      html: 'app/**/*.html'
      options:
        dest: 'build/app'
        root: 'build'
        flow:
          steps:
            js: ['concat']
            css: ['concat']
          post: {}
    usemin:
      html: ['build/**/*.html']

  grunt.loadNpmTasks 'grunt-usemin'
  grunt.loadNpmTasks 'grunt-contrib-clean'
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-copy'
  grunt.loadNpmTasks 'grunt-contrib-concat'

  grunt.registerTask 'default', [
    'clean:precompile'
    'web'
    'copy:dist'
  ]
  grunt.registerTask 'web', [
    'copy:web'
    'copy:fonts'
    'coffee:web'
    'useminPrepare'
    'concat'
    'usemin'
  ]
