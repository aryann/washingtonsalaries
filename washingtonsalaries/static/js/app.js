angular.module("washingtonsalaries", ["washingtonsalariesFilters"])
  .config(["$routeProvider", function($routeProvider) {
        $routeProvider
          .when("/search/:query",
                {templateUrl: "/static/partials/search.html",
                 controller: SearchController})
          .when("/employees/:employeeId",
                {templateUrl: "/static/partials/employees.html",
                 controller: EmployeeController})
          .otherwise({redirectTo: "/search/"});
}]);
