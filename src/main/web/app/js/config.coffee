#moment.tz.setDefault("utc")
app = angular.module 'core'
app.config ['$stateProvider', '$urlRouterProvider',
  ($stateProvider, $urlRouterProvider) ->
    $urlRouterProvider.otherwise '/main'
    $stateProvider
    .state 'main', {
      url: '/main'
      templateUrl: 'views/main.html'
    }
]
