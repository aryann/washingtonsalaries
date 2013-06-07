import json
import models

from django import http
from django import shortcuts
from django.core import paginator

MAX_RESULTS_PER_PAGE = 25


def emit_search_result(employee):
    """
    Stiches the given employee with his or her salary information and
    agency. The result will be a JSON-serializable object suitable for
    client consumption.
    """
    return {
        'id': employee.pk,
        'name': employee.name,
        'title': employee.title,
        'agency': {
            'id': employee.agency.id,
            'name': employee.agency.name,
            },
        'earnings': [
            {'id': record.pk,
             'year': record.year,
             'amount': record.salary}
            for record in employee.annualsalary_set.order_by('year').all()
            ],
        }


def json_response(obj):
    """
    Returns an HttpResponse constructed from JSON serializing obj.
    """
    return http.HttpResponse(json.dumps(obj, indent=4),
                             content_type='application/json')


def search(request):
    """
    Handles searches. This handler accepts a GET parameter q for the
    search query and an optional parameter page that allows the client
    to page through the results.
    """
    query = request.GET.get('q')
    if query is None:
        return http.HttpResponseBadRequest('Missing query parameter q.')

    all_matches = models.Employee.objects.filter(name__search=query)

    print all_matches.query

    pager = paginator.Paginator(all_matches, MAX_RESULTS_PER_PAGE)

    try:
        matches = pager.page(request.GET.get('page', 1))
    except paginator.EmptyPage:
        return http.HttpResponseBadRequest(
            'GET parameter page must be in range [1, {0}].'.format(
                pager.num_pages))
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

    return json_response(result)


def employee(request, id):
    """
    Handles querying of a single employee.
    """
    return json_response(emit_search_result(models.Employee.objects.get(pk=id)))


def index(request):
    return shortcuts.render(request, 'index.html', {})
