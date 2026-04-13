"""Intercepts /web/dataset/* calls to record benchmark traces.

Inherits Odoo's DataSet controller and wraps call_kw / call_button
to record model, method, and args before passing through to the
original implementation.

Also hooks into ir.http._dispatch to capture non-dataset routes
(e.g. /website/form/*, custom JSON-RPC controllers).
"""

import logging

from odoo import models
from odoo.http import request, route, Controller
from odoo.addons.web.controllers.dataset import DataSet

from ..models.benchmark_trace import is_active, record_call

_logger = logging.getLogger(__name__)


class BenchmarkDataSet(DataSet):
    """Wraps DataSet to trace call_kw and call_button."""

    @route()
    def call_kw(self, model, method, args, kwargs, path=None):
        raised = False
        try:
            result = super().call_kw(model, method, args, kwargs, path=path)
        except Exception:
            raised = True
            raise
        finally:
            if is_active():
                uid = request.env.uid if request.env else None
                record_call(
                    route="/web/dataset/call_kw",
                    model=model,
                    method=method,
                    uid=uid,
                    raised=raised,
                    args_summary=repr(args)[:256] if args else "",
                )
        return result

    @route()
    def call_button(self, model, method, args, kwargs, path=None):
        raised = False
        try:
            result = super().call_button(model, method, args, kwargs, path=path)
        except Exception:
            raised = True
            raise
        finally:
            if is_active():
                uid = request.env.uid if request.env else None
                record_call(
                    route="/web/dataset/call_button",
                    model=model,
                    method=method,
                    uid=uid,
                    raised=raised,
                    args_summary=repr(args)[:256] if args else "",
                )
        return result


class BenchmarkIrHttp(models.AbstractModel):
    """Hooks into ir.http to capture non-dataset HTTP routes."""
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls, endpoint):
        """Wrap dispatch to capture custom JSON-RPC/HTTP routes."""
        route_path = request.httprequest.path if request.httprequest else ""

        # Skip dataset routes — already captured by BenchmarkDataSet above
        if "/web/dataset/" in route_path:
            return super()._dispatch(endpoint)

        # Skip framework routes that are always noise
        if any(route_path.startswith(p) for p in (
            "/web/static/", "/web/assets/", "/web/image/",
            "/web/content/", "/bus/", "/longpolling/",
            "/web/bundle/", "/web/service-worker",
            "/web/manifest", "/web/offline",
            "/xmlrpc/",  # our own eval RPC calls
        )):
            return super()._dispatch(endpoint)

        raised = False
        try:
            result = super()._dispatch(endpoint)
        except Exception:
            raised = True
            raise
        finally:
            if is_active() and route_path:
                uid = request.env.uid if hasattr(request, 'env') and request.env else None
                # Try to extract model info from the route
                model = ""
                method = ""
                # For routes like /website/form/hr.applicant
                if "/website/form/" in route_path:
                    parts = route_path.split("/website/form/")
                    if len(parts) > 1:
                        model = parts[1].split("/")[0]
                        method = "create"

                http_method = request.httprequest.method if request.httprequest else ""
                record_call(
                    route=route_path,
                    model=model,
                    method=method,
                    uid=uid,
                    raised=raised,
                    http_method=http_method,
                )

        return result
