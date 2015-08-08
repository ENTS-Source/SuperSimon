angular.module 'core'
.factory 'sampleService', ['$http',
  ($http) ->
    return {
      getSomething: () ->
        $http.get '/api/something'
    }
]
