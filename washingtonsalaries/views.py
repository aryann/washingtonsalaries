import json
import models

from django import http
from django.core import paginator

MAX_RESULTS_PER_PAGE = 25


def search(request):

    def emit_search_result(employee):
        return {
            'name': employee.name,
            'title': employee.title,
            'agency': employee.agency.name,
            'earnings': [
                {'year': record.year,
                 'amount': record.salary}
                for record in employee.annualsalary_set.order_by('year').all()
                ],
            }

    query = request.GET.get('q')
    if query is None:
        return http.HttpResponseBadRequest('Missing query parameter q.')

    all_matches = models.Employee.objects.filter(name__search=query)
    pager = paginator.Paginator(all_matches, MAX_RESULTS_PER_PAGE)

    try:
        matches = pager.page(request.GET.get('page', 1))
    except paginator.EmptyPage:
        return http.HttpResponseBadRequest(
            'GET parameter page must be in range [{0}, {1}].'.format(
                1, pager.num_pages))
    except paginator.PageNotAnInteger:
        return http.HttpResponseBadRequest(
            'GET parameter page must be an integer.')

    items = [emit_search_result(match) for match in matches]
    result = {
        'total_results': pager.count,
        'total_pages': pager.num_pages,
        'page': matches.number,
        'items': items
        }

    return http.HttpResponse(json.dumps(result, indent=4),
                             content_type='application/json')
