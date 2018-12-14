import sys


_OPT_PREFIX = ("--_", "with-elevate-")


# tiny option parser to handle our special --_with-elevate-* opts
def _process_elevate_opts():
    opttest = lambda x, m=True: m == all(
        ["=" in x, x.startswith( "".join(_OPT_PREFIX) )]
    )

    # copy sys.argv (compatibility)
    old_argv = list(sys.argv)
    # prevent user code from seeing elevate's options
    sys.argv = list(filter(lambda x: opttest(x, False), old_argv))
    return dict(map(
        lambda y: y.split("_")[1].split("="), filter(opttest, old_argv)
    ))


def _get_opt(opts, name):
    return opts.get(_OPT_PREFIX[1] + name, False)


def _make_opt(name, param):
    return "".join(_OPT_PREFIX + (name, "=", param))
