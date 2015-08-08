angular.module 'core'
.controller 'NavController', ['$scope', '$state',
  ($scope, $state) ->
    $scope.$state = $state
]
