var SearchController = function($scope, $routeParams, $location, $http) {
  $scope.doQuery = function(page) {
    $scope.page = parseInt(page) || 1;
    $location.search("q", $scope.query);
    if (page) {
      $location.search("page", page);
    }
    var config = {
      params: {
        q: $scope.query,
        page: page,
      },
    };
    $http.get("search", config).success(function(result) {
	$scope.result = result;
      });
  };

  if ($routeParams.q) {
    $scope.query = $routeParams.q;
    $scope.doQuery($routeParams.page);
  }
};

var EmployeeController = function($scope, $routeParams, $http) {
  $http.get("employees/" + $routeParams.employeeId).success(function(employeeData) {
      $scope.result = {items: [employeeData]};
    });
};

SearchController.$inject = ["$scope", "$routeParams", "$location", "$http"];
EmployeeController.$inject = ["$scope", "$routeParams", "$http"];
