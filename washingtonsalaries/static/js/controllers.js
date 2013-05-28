var SearchController = function($scope, $http) {
  $scope.doQuery = function() {
    var config = {
      params: {q: $scope.query},
    };
    $http.get("search", config).success(function(data) {
	$scope.employees = data.items;
      });
  };
};

var EmployeeController = function($scope, $routeParams, $http) {
  $http.get("employees/" + $routeParams.employeeId).success(function(data) {
      $scope.employees = [data];
    });
};

SearchController.$inject = ["$scope", "$http"];
EmployeeController.$inject = ["$scope", "$routeParams", "$http"];
