angular.module("washingtonsalaries", ["washingtonsalariesFilters"])
  .config(["$routeProvider", function($routeProvider) {
        $routeProvider
          .when("/search",
                {
                  templateUrl: "partials/search.html",
                  controller: SearchController,
                  reloadOnSearch: false,
                })
          .when("/employees/:employeeId",
                {
                  templateUrl: "partials/employees.html",
                  controller: EmployeeController,
                })
          .otherwise(
                {
                  templateUrl: "partials/home.html",
                  controller: HomeController,
                });
      }])

  .value("solrPath", "/solr/washingtonsalaries/select")
  .value("years", [2010, 2011, 2012])

  .service("queryService", function() {
      var query;
      var page = 1;

      return {
        getQuery: function() {
          return query;
        },

        setQuery: function(value) {
          console.log("query set");
          query = value;
        },

        getPage: function() {
          return page;
        },

        setPage: function(value) {
          page = parseInt(value) || 1;
        },

        incrementPage: function() {
          page++;
        },

        decrementPage: function() {
          page--;
        }
      };
    });
