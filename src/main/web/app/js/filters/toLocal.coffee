angular.module 'core.directives'
.filter 'toLocal', () -> (input) ->
  return moment(input)
