angular.module 'core.directives'
.directive 'hourGraph', [
  () ->
    return {
      restrict: 'E'
      templateUrl: 'views/directives/hourGraph.html'
      scope: {}
      replace: true
      link: (scope, element, attrs) ->
        scope.primePeriod = -1
        scope.data = []
        for i in [0..23]
          scope.data.push -1
        populate = () ->
          for i in [0..23]
            scope.data[i] = Math.floor(Math.random() * 75)
          scope.primePeriod = 1
          scope.$apply()
        setTimeout populate, 1000
        scope.isPrime = (hour) ->
          idx = -1
          if hour <= 5 then idx = 0
          if hour > 5 and hour <= 11 then idx = 1
          if hour > 11 and hour <= 17 then idx = 2
          if hour > 17 then idx = 3
          return idx == scope.primePeriod
        scope.getHeight = (hour) ->
          if scope.data[hour] < 0 then return 0
          max = _.max scope.data, (item) -> item
          return (scope.data[hour] / max) * 100
    }
]
