import itertools

__version__ = '0.2.3'

def xrepr(arg):
    if isinstance(arg, str):
        return "'%s'" % arg
    else:
        return repr(arg)

def generated_warning(php, os, variant):
    return """\
#############################################################################
# NOTE: FILE GENERATED AUTOMATICALLY, DO NOT EDIT!!!
#############################################################################
"""

def php_params(php, os, variant):
    """Configuration parameters for php with their default values"""

    params = dict()
    if variant == 'cli':
        params.update({
            'PHP_UID': 1000,
            'PHP_GID': 1000
        })

    return params


def php_env_defaults_str(php, os, variant):
    items = php_params(php, os, variant).items()
    return '\n'.join(("DEFAULT_%s=%s" % (k, xrepr(v)) for k, v in items))


def php_env_settings_str(php, os, variant):
    params = list(php_params(php, os, variant))
    return '\n'.join(('%s=${%s-$DEFAULT_%s}' % (k, k, k) for k in params))


def docker_php_args_str(php, os, variant):
    items = php_params(php, os, variant).items()
    if len(items) == 0: return ''
    return '\n'.join(('ARG %s=%s' % (k, xrepr(v)) for k, v in items))


def docker_php_env_str(php, os, variant):
    params = list(php_params(php, os, variant))
    if len(params) == 0: return ''
    return 'ENV ' + ' \\\n    '.join(('%s=$%s' % (k, k) for k in params))


def context_dir(php, os, variant, sep='/'):
    return sep.join([php, os, variant])


def context_tag(php, os, variant, sep='-'):
    return sep.join([php, variant, os])


def context_files(php, os, variant):
    return {'Dockerfile.%s' % variant: 'Dockerfile',
            'hooks/build.in': 'hooks/build'}


def context_subst(php, os, variant):
    return dict({'GENERATED_WARNING': generated_warning(php, os, variant),
                 'PHP_ENV_DEFAULTS': php_env_defaults_str(php, os, variant),
                 'PHP_ENV_SETTINGS': php_env_settings_str(php, os, variant),
                 'DOCKER_FROM_TAG': context_tag(php, os, variant),
                 'DOCKER_PHP_ARGS': docker_php_args_str(php, os, variant),
                 'DOCKER_PHP_ENV': docker_php_env_str(php, os, variant),
                 'VERSION': __version__}, **php_params(php, os, variant))


def context(php, os, variant):
    return {'dir': context_dir(php, os, variant),
            'files': context_files(php, os, variant),
            'subst': context_subst(php, os, variant)}


phps = [ '7.0', '7.1', '7.2', '7.3' ]
oses = [ 'jessie', 'stretch', 'buster' ]
variants = [ 'cli', 'apache' ]


def excluded(t):
    exclusions = [
            ('7.0', 'stretch'),
            ('7.0', 'buster'),
            ('7.1', 'stretch'),
            ('7.1', 'buster'),
            ('7.2', 'jessie'),
            ('7.3', 'jessie'),
    ]
    return len(set([t[:1], t[:2], t]) & set(exclusions)) > 0

prod = [t for t in itertools.product(phps, oses, variants) if not excluded(t)]
contexts = [context(php, os, variant) for (php, os, variant) in prod]

del phps
del oses
del variants
