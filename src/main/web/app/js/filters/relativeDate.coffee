angular.module 'core.directives'
.filter 'relativeDate', () -> (input) ->
  return moment(input).calendar()
