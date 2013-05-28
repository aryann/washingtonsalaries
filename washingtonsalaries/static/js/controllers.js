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

SearchController.$inject = ["$scope", "$http"];
