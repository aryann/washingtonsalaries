var HomeController = function($location, $scope, queryService) {
  $scope.queryService = queryService;

  $scope.$watch("queryService.getQuery()", function(newVal, oldVal) {
      if (newVal === oldVal) {
        return;
      }
      $location.path("/search");
      $location.search("q", queryService.getQuery());
    });
};

var SearchController = function($http, $location, $routeParams, $scope,
                                $timeout, queryService, solrPath, years) {

  $scope.years = years;
  $scope.resultsPerPage = 25;

  var doQuery = function() {
    var config = {
      params: {
        q: queryService.getQuery(),
        start: (queryService.getPage() - 1) * $scope.resultsPerPage,
        rows: $scope.resultsPerPage,
        wt: "json",
      },
      cache: true,
    };
    $http.get(solrPath, config)
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

  $scope.$watch("queryService.getPage()", function(newVal, oldVal) {
      if (newVal === oldVal) {
        return;
      }
      if (timer) {
        $timeout.cancel(timer);
      }
      $location.search("page", newVal === 1 ? null : newVal);
      doQuery();
  });

  $scope.$watch("queryService.getQuery()", function(newVal, oldVal) {
      if (newVal === oldVal) {
        return;
      }
      if (timer) {
        $timeout.cancel(timer);
      }
      timer = $timeout(function() {
          $scope.page = 1;
          $location.search("page", null);
          $location.search("q", queryService.getQuery());
          doQuery();
      }, 200);
  });

  $scope.queryService = queryService;
  queryService.setPage($routeParams.page);
  if ($routeParams.q) {
    queryService.setQuery($routeParams.q);
    doQuery();
  }

  $scope.query = queryService.getQuery();
};

var EmployeeController = function($http, $routeParams, $scope, solrPath,
                                  years) {
  $scope.years = years;

  var config = {
    params: {
      q: "id:" + $routeParams.employeeId,
      wt: "json",
    },
    cache: true,
  };
  $http.get(solrPath, config)
    .success(function(data) {
        $scope.response = data.response;
        $scope.error = false;
    })
    .error(function() {
        $scope.response = null;
        $scope.error = true;
    });
};

HomeController.$inject =
  ["$location", "$scope", "queryService"];
SearchController.$inject =
  ["$http", "$location", "$routeParams", "$scope", "$timeout", "queryService",
   "solrPath", "years"];
EmployeeController.$inject =
  ["$http", "$routeParams", "$scope", "solrPath", "years"];

