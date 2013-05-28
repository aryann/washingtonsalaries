angular.module("washingtonsalariesFilters", [])

  // Adds a $ sign and commas to the given numeric input.
  .filter("salary", function() {
      return function(input) {
        input = input.toString();
        var res = [input.substr(0, input.length %3)];
        for (var i = input.length % 3; i < input.length; i += 3) {
          res.push(input.substr(i, i + 3))
        }
        return "$" + res.join(",");
      };
    });
