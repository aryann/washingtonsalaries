var SearchController = function($http, $location, $routeParams, $scope,
                                $timeout) {
  var doQuery = function() {
    var config = {
      params: {
        q: $scope.query,
        page: $scope.page,
      },
      cache: true,
    };
    $http.get("search", config).success(function(result) {
	$scope.result = result;
    });
  };

  var timer = null;

  $scope.$watch("page", function(newVal, oldVal) {
      if (newVal == oldVal) {
        return;
      }
      if (timer) {
        $timeout.cancel(timer);
      }
      $location.search("page", $scope.page === 1 ? null : $scope.page);
      doQuery();
  });

  $scope.$watch("query", function(newVal, oldVal) {
      if (newVal === oldVal) {
        return;
      }
      if (timer) {
        $timeout.cancel(timer);
      }
      timer = $timeout(function() {
          $scope.page = 1;
          $location.search("page", null);
          $location.search("q", $scope.query);
          doQuery();
      }, 200);
  });

  $scope.page = parseInt($routeParams.page) || 1;
  if ($routeParams.q) {
    $scope.query = $routeParams.q;
    doQuery();
  }
};

var EmployeeController = function($http, $routeParams, $scope) {
  $http.get("employees/" + $routeParams.employeeId).success(function(employeeData) {
      $scope.result = {items: [employeeData]};
    });
};

SearchController.$inject =
  ["$http", "$location", "$routeParams", "$scope", "$timeout"];
EmployeeController.$inject =
  ["$http", "$routeParams", "$scope"];
