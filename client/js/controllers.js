var solr = "http://localhost:8983/solr/washingtonsalaries/select";

var SearchController = function($http, $location, $routeParams, $scope,
                                $timeout) {
  $scope.years = [2010, 2011, 2012];
  $scope.resultsPerPage = 25;

  var doQuery = function() {
    var config = {
      params: {
        q: $scope.query,
        start: ($scope.page - 1) * $scope.resultsPerPage,
        rows: $scope.resultsPerPage,
        wt: "json",
      },
      cache: true,
    };
    $http.get(solr, config)
      .success(function(data) {
          $scope.response = data.response;
          $scope.error = false;
      })
      .error(function() {
          $scope.response = null;
          $scope.error = true;
      });
  };

  var timer = null;

  $scope.$watch("page", function(newVal, oldVal) {
      if (newVal === oldVal) {
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
  $scope.years = [2010, 2011, 2012];

  var config = {
    params: {
      q: "id:" + $routeParams.employeeId,
      wt: "json",
    },
    cache: true,
  };
  $http.get(solr, config)
    .success(function(data) {
        $scope.response = data.response;
        $scope.error = false;
    })
    .error(function() {
        $scope.response = null;
        $scope.error = true;
    });
};

SearchController.$inject =
  ["$http", "$location", "$routeParams", "$scope", "$timeout"];
EmployeeController.$inject =
  ["$http", "$routeParams", "$scope"];
