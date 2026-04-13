{
    'name': 'Benchmark Trace',
    'version': '19.0.0.1',
    'category': 'Tools',
    'summary': 'Server-side API call tracing for browser agent benchmarks',
    'description': """
Records all JSON-RPC and HTTP requests during benchmark episodes.
Produces structured trace logs for evaluating browser agent behavior.

Start/stop tracing via XML-RPC:
    object.execute_kw(db, uid, pwd, 'benchmark.trace', 'start_trace', [session_name])
    object.execute_kw(db, uid, pwd, 'benchmark.trace', 'stop_trace', [])
    object.execute_kw(db, uid, pwd, 'benchmark.trace', 'get_trace', [])
    """,
    'depends': ['web'],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
