angular.module("washingtonsalaries", ["washingtonsalariesFilters"])
  .config(["$routeProvider", function($routeProvider) {
        $routeProvider
          .when("/search",
                {templateUrl: "/static/partials/search.html",
                 controller: SearchController,
                 reloadOnSearch: false})
          .when("/employees/:employeeId",
                {templateUrl: "/static/partials/employees.html",
                 controller: EmployeeController})
          .otherwise({redirectTo: "/search"});
}]);
