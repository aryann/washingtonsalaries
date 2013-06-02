angular.module("washingtonsalariesFilters", [])

  // Same as the currency filter except the decimal portion is truncated.
  .filter("salary", function($filter) {
      return function(input) {
        var output = $filter('currency')(input);
        return output.substr(0, output.length - 3);
      };
    });
