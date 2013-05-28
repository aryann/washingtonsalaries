var SearchController = function($scope, $routeParams, $location, $http) {
  $scope.doQuery = function() {
    var config = {
      params: {q: $scope.query},
    };
    $http.get("search", config).success(function(data) {
	$scope.employees = data.items;
      });

  };
  if ($routeParams.query) {
    $scope.query = $routeParams.query;
    $scope.doQuery();
  }
};

var EmployeeController = function($scope, $routeParams, $http) {
  $http.get("employees/" + $routeParams.employeeId).success(function(data) {
      $scope.employees = [data];
    });
};

SearchController.$inject = ["$scope", "$routeParams", "$location", "$http"];
EmployeeController.$inject = ["$scope", "$routeParams", "$http"];
