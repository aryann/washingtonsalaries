angular.module("washingtonsalaries", [])
  .config(["$routeProvider", function($routeProvider) {
        $routeProvider
          .when("/",
                {templateUrl: "/static/partials/search.html",
                 controller: SearchController})
          .when("/employees/:employeeId",
                {templateUrl: "/static/partials/employee.html",
                 controller: EmployeeController})
          .otherwise({redirectTo: "/"});
}]);
