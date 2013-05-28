angular.module("washingtonsalaries", ["washingtonsalariesFilters"])
  .config(["$routeProvider", function($routeProvider) {
        $routeProvider
          .when("/",
                {templateUrl: "/static/partials/search.html",
                 controller: SearchController})
          .when("/employees/:employeeId",
                {templateUrl: "/static/partials/employees.html",
                 controller: EmployeeController})
          .otherwise({redirectTo: "/"});
}]);
